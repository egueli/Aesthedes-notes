# Recovering design files from Aesthedes filesystem

# Finding deleted project files

It would be great to recover as many designs/projects as possible that were created on this machine. Alas, there is not much 

I can imagine two ways to recover deleted files:

- by recursively scanning the directory tree for directory entries starting with 0x00, reconstructing the name and check if sector/LSN number points to a valid file descriptor; when the FD is of a directory, scan those entries too.
- by scanning the entire image for sectors that look like file descriptors (for either files or directories)

Interesting: 0x4b860/00, referenced by directory file at 0x3cd35/20 (file `kosep`), it looks like a project file like `ebt` and `PLOTTERTEST`.

Given we already have a track to follow i.e. the directory listing at sector 0x3cd20, I can make a small utility that tries to read directory entries at any given sector, check if the corresponding FD sector is a valid FD, then dump the file data to a file in the host filesystem. The latter can be done by the utility itself via standard I/O calls, or by forging a directory entry into the root directory of that image (requires writing), or by printing data for binary patching.

There are directory entries between 0x3cd20 and 0x3cd5f.

I made new os9 command “dirrec” to recover files from a sector containing directory entries. The command will read the files’ FD including segments, and write to files (on host filesystem) sector by sector. I considered the option to relink the files to an existing directory, but that means writing to the RBF image with potential data loss.

Running this on the interesting sectors above shows some interesting text files. Text files seem to use CR (0d) as line ending, while Linux/Mac uses LF (0a)

```bash
cat planten.txt | tr '\r' '\n'

Ingredi/u416nten: plantaardige oli/u416n en vetten,
water, dextrose, emulgator (E471,
E322), voedingszuur (E330), conserveermiddel (E202), geur- en
smaakstof, kleurstof (E160a, E160b), vitamine A: 20 I.E. per gram,
vitamine D3: 3 I.E. per gram. Bevat 80% oli/u416n en vetten.
Voedingswaarde
per 100 gram produkt: Energie: 3190 kJ (790 kcal), vet: 84 gram,
waarvan
34
gram m.o.v. en 26 gram v.v., eiwit: 0 gram, koolhydraten: 0 gram,
waarvan 0
gram dex-
.newline
trose en 0 gram lactose, zout: 0 gram. ----------------------
```

It looks like a list of ingredients and nutritional facts of an industrial food product. 

I also made another os9 command “dirscan” that scans through a whole RBF image looking for sectors that contain directory entries, and print their LSNs. It does so by reading each sector's data and check if it follows certain rules, e.g. all null bytes after a file name and before a file's LSN. Running this command on an image will output also regular directories, so one should manually select what's interesting.

By combining these two commands I'm able to recover any file found in an image. The whole command chain looks like:

```bash
os9 dirscan HD10_256_fixed.hda > dirsectors
(for lsn in $(cat dirsectors); do echo; echo "# $lsn"; os9 dirrec -n HD10_256_fixed.hda $lsn; done) > recovered_files.txt
```

As expected, the 0x3cd20..0x3cd5f sectors pop up as well. The output is something like:

```bash
# 0x3cd33
pms484
pms487
pms488
pms489
pms490

# 0x3cd34
pms499

# 0x3cd35
pms500
kosep
pms501
b008003.dkh
b008003.ikh
b008004.dkh
```

# Investigation around `planten.txt`

Back to `planten.txt`: if it’s present in the system, and the system is made to create graphic layouts, then it must be somehow referenced by a design file.

Let’s do a full search across strings in the HD image. Running `strings -tx HD10_256_fixed.hda | less -S` and searching for `planten.txt` we see:

```
4928380 H007004
49283a0 g006013
49283c0 g006017
49283e0 G006016
4928400 planten.txt
4928420 layout
4928440 textc
4928466 @6ff@L
492849a text_default
```

That’s the only occurrence. Note that it’s not part of a directory: because strings are encoded with the MSB of the last character set, the corresponding directory would have been found with `planten.tx`.

Which file refers to `planten.txt`? By looking at the output of `hexdump -Cv HD10_256_fixed.hda | less -S` (note the `-v` is necessary to not skip empty bytes so `less` can work better) it seems that it’s in a file whose descriptor is at sector 0x49260. What’s its name? With search command `/04 92 60  |` we can search for a 16-byte sequence that ends with these three bytes, giving us the second half of an LSN pointing to that file. Alas, no directory file could be found with that LSN so we probably need to “resurface” this file manually, and make up a name.

What about the “siblings” of planten.txt mentioned in that same file? If we want to recover this design, and it requires the presence of planten.txt, then the siblings must be present too.

# Remia

I saw the [Remia](https://www.remiaprofessioneel.nl/remia/speciaalsauzen) brand some time ago (August 2023) in the recovered files, but I didn’t remember anymore.

So I’m going to search again.

With `strings -tx HD10_256_fixed.hda | grep -i remia` I see it’s present several times in the image:

```
3ab0136 Remia Halvanaise met komkommer is een zachte frisse saus op basis van 
3ab02af Remia Halvanaise bevat 75% minder calorieen dan mayonaise. 
3ab02eb Tip: probeer ook eens Remia Halvanaise Naturel.
40c02e3 Produced by Remia Holland
40c0306 from N.V. REMIA BELGIUM S.A.,
45aa22c Producido por: Remia C.V., W. Arntszlaan 71-77
45ae22c Producido por: Remia C.V., W. Arntszlaan 71-77
46744de Produced by: Remia C.V.
47f8118 VERSTANDIG MET REMIA
5150103 de Remia Speciaal Slasauzen met yoghurt, tuinkruiden of knoflook.
622026c Remia Halvanaise bevat 75% minder calorieen dan mayonaise.
62202a7 Tip: probeer ook eens Remia Halvanaise met komkommer.
6902251 Produced by Remia Holland for: N.V. Remia Belgium S.A. H.R.//R.C. St.
```

# “Not an AES vector-file”

I casually stumbled upon this string while running `strings` on files recovered by dirscan/dirrec. It might be related to code meant to parse design files.

I’ve found two occurrences of it: at 0xf63672 and 0x1359668, of which the second was in one of the recovered files. Can we disassemble at least one of them and see if there’s vector-file-parsing logic? Then we can reverse-engineer that to search for design files in the HD image.

Both files contain `dxfout` somewhere in their header.

Dxfout is an utility like many others in the Aesthedes’ `CMDS` directory. With Ghidra I can see it seems to run via command line, it takes the name of a possible AES file as first command line argument, and reads/parses it. Its file descriptor is at LSN 00F620. The `dxfout` string is located at image file offset 00F62148.

Further reverse-engineering can be time consuming, and maybe not really needed. If there were an emulator of OS-9 and 68k, maybe the program could run directly over possible design files.

## OS-9/68k emulators

[os9exec -  os9 emulator](https://sourceforge.net/projects/os9exec/)

`os9exec` is a little hard to compile, because it requires four header files (errno.h, sgstat.h, procid.h, module.h) that are missing due to copyright.

But the SF website publishes executables for Windows and OS X. The Windows executable works:

- the `os9app.exe` should be alongside a directory called `dd`, this directory must contain the `CMDS` directory from the RBF image.
- In that same directory I added the `ANONYMOUS` directory with the two known-good design files `ebt` and `PLOTTERTEST`.
- I ran the emulator and the dxfout utility within: `.\os9app.exe dxfout ANONYMOUS/ebt ebt.dxf` and it successfully converted that file into `dd/ebt.dxf`.

I managed to run dxfout over all the files in `ANONYMOUS`, i.e. that are currently readable by the live Aesthedes system.

# Directory file listing as text

Offset 0x176f000 contains a dir listing.

# Flat image recovery

By scanning the image from beginning to end, one can find file descriptors and save all file contents in the host file system.

The file descriptors contain all but the name. So an hypothetical utility (`fscan`) could save with a file name template like `lsn_AABBCC.file`. It should take care that 1- the descriptor is valid (we have an algorithm for that already) 2- all the file sectors are not taken by another file. In that case it might still assign the same sectors but mark both files as potentially corrupt, saving the relevant info on a different file.

Directory files may need a double representation: as file with the raw entries, and as directory on the host filesystem (`lsn_AABBCC.dir`) whose contents are symlinks to the respective files.

Worth looking at the implementation of `dcheck` since it may also do a full image scan.

`dirscan` scans all sectors of an RBF image looking for one that resembles a list of directory entries. In our case, we want to look for a sector looking like a file descriptor.

`fscan` would be very “low level” and not even distinguish between files and directories: in fact, a directory is a file with a specific bit set in its file descriptor and whose content is a file listing. It would just use that bit to use the right file name template (`.file` or `.dir`).

Another utility, `ftree`, can scan the root dir for such files and make directories and symlinks to all the recovered files.

Such a directory structure could be versioned with Git, so one can keep records of manual changes e.g. resolved file/sector mappings.

Note that this would only recover directories complete with their file descriptor; “orphan” directories like [Juicy directory at 0x3cd2a90](Recovering%20the%20Aesthedes%202%20system%20password%20110a44a734f0807e8569ef2a64937ea3.md) wouldn’t come up. The output of `dirscan` would still be useful to give a name to the recovered files.

# A brand new disk image

The image we got has lots of filesystem errors, that are too hard to fix manually. Better make a new image from scratch, put all the original files there, then add the recovered ones.

We can use the `os9 format` utility in Toolshed to create a new image. It’s important that the filesystem has the same structure as the old one, as we don’t know if the Aesthedes will be able to read it.

```python
os9 format -c32 -e -n205_IO -l1173120 AES2_HCM_EG.hda
```

The resulting image does not have the same properties as `HD10_256.hda:`

- The former has a size of 285020160 bytes vs. 299581440 (14220kiB, or 14561280, or 0xde3000, less bytes). Weirdly enough, `os9 id` shows the same number of sectors, 1173120. Both sizes seem incorrect though, as 1173120 * 256 = 300318720. Hmm.
- The new image has 4 sectors per track, the old one has 64. Hopefully the OS can deal with that. I could not find an option in `os9 format` to change that.

I proceed to copy all files from the old image to the new. `os9 copy` doesn’t seem to support recursion into directory (it hung with a huge file called `ANONYMOUS`), so we might need the help of the Unix file utilities.

Assuming that all the files and directories have been extracted to `HD10`:

```bash
cd HD10
for dir in $(find . -mindepth 1 -type d); do os9 makdir ../AES2_HCM_EG.hda,${dir:2}; done
for file in $(find . -type f); do os9 copy $file ../AES2_HCM_EG.hda,${file:2}; done
```

Bart confirms that an image constructed this way is able to start up the Aesthedes. Success!

## Adding the recovered files to the image

I saved the listing of DXF files created by dxfout (see [OS-9/68k emulators](Recovering%20design%20files%20from%20Aesthedes%20filesystem%20110a44a734f080d582ede1e4f50f5207.md) ) to `dxflist`.

Adding recovered files to the image:

```bash
mkdir image_with_recovered
cd image_with_recovered/
cut -d'.' -f1 < dxflist > filelist
sed 's/[^^]/[&]/g; s/\^/\\^/g' filelist | sed 's:^\(.*\)$:/\1(\\..+)?$:' > patterns
for file in $(find | grep -E -f ~/aesthedes/image_with_recovered/patterns); do destfile=${file/^/_}; destfile=rec_${destfile:2}; os9 copy ${file:2} ../../AES2_HCM_EG_v2.hda,ANONYMOUS/${destfile}; done
```

Make list of files to check, ordered by size (decreasing):

```bash
os9 dir -e AES2_HCM_EG_v2.hda,ANONYMOUS |tail -n +5 | sort -n -k6 -r | cut -c56- | grep rec_ > image_with_recovered/to_check
```