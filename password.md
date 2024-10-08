# Recovering the Aesthedes 2 system password

# Analyzing the disk image file

Since the Aesthedes runs over Microware OS-9, the hard disk image may contain a compatible filesystem.

With [ToolShed](https://sourceforge.net/p/toolshed/code/ci/default/tree/doc/ToolShed.md#de_linux), it is possible to read the image. Or at least the root directory. Here’s the output of `os9 dir HD10_256.hda,`:

```
Directory of HD10_256.hda,.
ANONYMOUS       CMDS            COMP            POSTSCRIPT      SYS
TEMP            TMP_ETHER       VAX_EGTS        CDS.00004       load738
JUNK            startup         CDS.a0004       CDS.b0004       CDS.c0004
```

With `mkdir mnt; cocofuse HD10_256.hda mnt` one can navigate the filesystem with the regular Unix commands. Here’s the output of `ls -l mnt`:

```
drwx---rwx 1 enrico enrico       6208 dec  1  1923 ANONYMOUS
-r-------x 1 enrico enrico 1768711470 nov 17  2017 CDS.00004
-rwx------ 1 enrico enrico  876738049 mei  2  1954 CDS.a0004
drwx---rwx 1 enrico enrico   15869920 sep 28  1999 CDS.b0004
-rw----rw- 1 enrico enrico       1572 jan 21  1988 CDS.c0004
drwx---rwx 1 enrico enrico      10304 dec  1  1923 CMDS
-r-x------ 1 enrico enrico       5888 jul  4  1989 COMP
?????????? ? ?      ?               ?            ? JUNK
?????????? ? ?      ?               ?            ? load738
drwx---rwx 1 enrico enrico 1565422913 apr 20  1916 POSTSCRIPT
-r-x------ 1 enrico enrico     242926 sep 27  1991 startup
-r-x------ 1 enrico enrico       4250 mei  4  1989 SYS
?????????? ? ?      ?               ?            ? TEMP
?????????? ? ?      ?               ?            ? TMP_ETHER
?????????? ? ?      ?               ?            ? VAX_EGTS
```

Given the “impossible” file sizes and the question marks, there is a problem in reading the image. Either the tools are not fully compatible with the image, or the image is somewhat damaged.

Running `os9 dcheck HD10_256.hda` shows several errors. Many sectors “previously allocated” and many errors related to the `PLOTPARAM.HP` file.

The `CMDS` directory contains several executable files; looks similar to Unix’s `/bin`. The file dates ranges from 1987 to 1991.

I guess the directory/file structure can be better understood with the OS-9 manual at [https://www.roug.org/retrocomputing/os/os9/os9guide.pdf](https://www.roug.org/retrocomputing/os/os9/os9guide.pdf). More technical info, including system calls list, can be found at [http://www.icdia.co.uk/microware/tech/](http://www.icdia.co.uk/microware/tech/).

At offset 0x09e000 of the RBF image, there is the file description of what looks a batch script file. Maybe it’s the real `startup` file?

# Finding the password

The objective is to find the system password, which should be located at `/SYS/password`, but `/SYS` is inaccessible because ToolShed thinks it’s a regular file. Then, let’s search for the password by looking directly at the filesystem image data.

With the command `strings -tx HD10_256.hda` one can navigate through all the strings in the image, and obtain the offset in hex. Because the sectors are 256 bytes large, the last two hex digits are the offset within the sector, the rest are the sector number.

Somewhere, a sector will contain data for the directory containing the `password` file. The RBF format specifies that each file is represented in ASCII and the last character has the highest bit set. `strings` does not know about this format, so we’ll search for `passwor` and skip any matches of `password` (there must be a regex for this).

A string like `passwor` could be found at offset 0x1768200. It is part of a directory listing that seems to begin at 0x17680000 (that’s where the file descriptor is; the actual directory data begins at 0x1768100). The password file entry mentions sector 0x17780, so the password might be at byte offset 0x1778000, with data at 0x1778100.

The file is referred as “validation file” in the [OS-9 guide](https://www.roug.org/retrocomputing/os/os9/os9guide.pdf) and is described at page 72. Here are the first bytes of the validation file:

```
01778100  65 74 68 65 72 2c 65 74  68 65 72 2c 30 2e 30 2c  |ether,ether,0.0,|
01778110  31 32 38 2c 2f 48 30 2f  43 4d 44 53 2c 2f 48 30  |128,/H0/CMDS,/H0|
01778120  2f 41 4e 4f 4e 59 4d 4f  55 53 2c 73 68 65 6c 6c  |/ANONYMOUS,shell|
01778130  0d 00 00 50 00 00 01 a0  00 00 0f fc 00 01 4c 00  |...P..........L.|
01778140  00 00 65 26 00 00 65 e6  73 63 61 6e 32 72 6c 00  |..e&..e.scan2rl.|
01778150  2d 46 80 10 2d 46 80 14  3d 43 80 18 08 2b 00 05  |-F..-F..=C...+..|
```

It seems only the first 48 bytes are valid ASCII data, the rest is binary stuff. Maybe there’s another valid copy somewhere else in the filesystem? But there are no other matches of `ether,ether`as in this fragment.

By looking at its file descriptor (and comparing with its structure described [here](https://www.roug.org/soren/6809/os9sysprog.html#AEN802)), one sector above, it seems the size is 0x31 bytes. So the validation file is really all there. Maybe the password is actually `ether`? Its work directory is `/H0/ANONYMOUS` and that’s where the user files actually are. At this point, there’s no option left than just try 🙂

I also tried with [bgrep](https://github.com/tmbinc/bgrep) to look for another directory entry for a password file, but 0x1768200 was the only match.

## Backcheck

If I was able to manually find the password file, how come Toolshed had so much trouble reading the filesystem?

The file descriptor of the directory list containing `password` is at 0x1768000. Given that directory should be `/SYS`, there must by another directory list containing that LSN i.e. the byte sequence `01 76 80` should be at the end of a 32-byte file entry block.

Such an entry can be found at 0x14d0 for a `SYS` directory (like the root directory), and again at 0x3cd2a90. Is it possible that this image actually contains two partitions?

After some step-debugging on ToolShed code, it seems that for every non-root directory it was reading at the wrong file offsets in the image. That explained why directories were seen as files. Turns out, the code was implying that the track 0 was 16384 bytes long instead of 64. After patching the image to set the corresponding field back to 64, the utils started reading everything correctly. A full copy is still not possible (`cocofuse` freezes mid-copy), and the DCHECK utility still finds errors.

It seems that there are two versions of ToolShed available: one hosted in SourceForge, one hosted in Github. Their codebases have diverged and they behave differently. In particular, GitHub’s one does not honor the first track size and is able to read our image straight away, without patches.

# Juicy directory at 0x3cd2a90

There are many directory entries around that file offset, with names like `pms310`, `pms311` and so on. Also `okt101g` and `jun120c`. They are not reachable by ToolShed, so maybe there is some more issue. It might be interesting to recover them, since they might possibly be old project files of the last owner, that deleted them before decommissioning the machine.

The file descriptor of that directory may be at offset 0x3cd1f00, but the first byte does not identify a directory. The directory data at 0x3cd2000 might be a segment of a multi-segment directory file. Segments are described in a file descriptor as 5-byte fields. But unfortunately, a `bgrep`on the sequence `03 cd 20` led to nothing resembling a list of 5-byte items.

# Repairing the filesystem

Running dcheck on GitHub’s ToolShed still shows errors, although less than the previous run. There are still a lot of “previously allocated sector” errors. Because the tool detects errors but doesn't fix them, I'll manually check what's going on.

Some background: in the RBF filesystem, the sectors holding a file’s data (let’s call them “payload sectors”) are preceded by a sector called file descriptor. The payload is usually in a single segment, but it can be split into multiple segments. The FD contains the list of segment, described as sector number + number of segments. One can assume that the first segment always starts one sector after the FD.

It seems that for several files, this does not hold true. And if dcheck ignores that segment start and assumes the first segment starts one sector after the FD, most of the allocation-related errors go away.

Other errors:

- `ANONYMOUS/p.hell` has an FD that is identical to `ANONYMOUS/p.rd_ct2t` . Actually, sectors from 0x2A0 to 0x2FF seem to have an exact copy 96 sectors later, from 0x320 to 0x37F. And the latter data seem more consistent. Therefore, all data on files in the second group is effectively lost and the directory entries should be deleted.
- Other errors I didn’t bother describing. See below.

Based on the dcheck output I decided to simply mark the affected files as deleted, by setting the first byte of the name to 0x00. I saved the patched image to a different file, so to be able to eventually come back and do further investigation. Now, the other os9 utilities and `cocofuse` are able to read the remaining files without a hinch. So I created a file tree in my work PC.

## A look at the files

There is `/startup` that looks like a script.

# Finding the password, again

I asked Bart to try `ether`, but the system didn't accept it. So the search for that password must continue.

I grepped for `password` across all executable files in the recovered file tree (full command: `find -type f -executable -print -exec sh -c "strings {} | grep -i password" \; | less`); among many occurrences related to OS-9's user management, one immediately jumped out at me:

```bash
Enter PassWord or CANCEL :
```

Not only for the unusual capitalization, but especially because that's exactly the prompt the Aesthedes showed on one of its control screens when Bart attempted to enter that security area. The string is located in `CMDS/fcontrol`.

Armed with the Ghidra disassembler, I tried to see how that string is used. If I'm lucky enough, the code showing that screen would be waiting for the user input, then compare it with the expected password.

Before doing that, I needed to setup Ghidra: although it does disassemble 68k executable code, it has no idea what an OS-9 executable looks like. Luckily there is an extension for that: https://github.com/roysmeding/ghidra-os9. But it stops with a Java exception when run, due to https://github.com/roysmeding/ghidra-os9/issues/3. After some debugging, I figured out why it was failing and made a quick fix: https://github.com/roysmeding/ghidra-os9/pull/4. Then I could finally open `fcontrol` in Ghidra.

After some search/browsing/decompiling, it seems that the password is actually hard-coded in the executable, and it is `SysteM`. I'm now waiting for Bart to confirm if that works.

Update: it does!

[https://www.facebook.com/100063545500371/posts/pfbid0bk8VymRxdF5ePxnRpf4bnBYwidmagEtbNy9Q7wq9TCiErnJdKPUfmvFb6pGpdrsul/?app=fbl](https://www.facebook.com/100063545500371/posts/pfbid0bk8VymRxdF5ePxnRpf4bnBYwidmagEtbNy9Q7wq9TCiErnJdKPUfmvFb6pGpdrsul/?app=fbl)