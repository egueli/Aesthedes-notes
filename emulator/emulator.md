# Emulating Aesthedes in MAME

# Simulating an Aesthedes

Let's see if we can somehow run the AES2 software on a modern PC.

The OS-9 technical manual may come useful to understand and fix issues: 

[The New International CD-i Association](http://www.icdia.co.uk/microware/tech/)

[www.roug.org](https://www.roug.org/retrocomputing/os/os9/os9guide.pdf)

First, I cloned the sources from Biappi's os9exec to a Linux x86 machine: https://github.com/biappi/os9exec

Then, I run: 

```bash
cmake .
make
ln -s <path-to-aesthedes-system-disk-root> dd
./os9exec
```

But…

```bash
enrico@enrico-aesthedes-sre:~/os9exec$ ./os9exec

# OS9exec V3.39:     OS-9  User Runtime Emulator
# Copyright (C) 2007 Lukas Zeller / Beat Forster
# This program is distributed under the terms of
#        the GNU General Public License
#
# Platform: 'Linux - PC' (x86)
# - Linux XTerm Version
# - Using 68k-Emulator from UAE - Un*x Amiga Emulator (c) 1995 B. Schmidt
# Building CPU table for configuration: 68020/881
#     1852 CPU functions
# Building CPU function table (3 0 0).

# Emulation could not start due to OS-9 error #000:214 (E_FNA): 'shell'
#   File Not Accessible

# OS-9 emulation ends here.
```

(lots of bugfixes omitted)

## Memory corruption bug

`shell`  crashes in various, random ways.

### Case 1

In one case, the 96424th instruction wrote to instruction memory. It wrote `5ab9ea2a`. The instruction 0x4896 bytes after the entry point was equal to `2f08` (last run as 97277th), then it became `ea2a` (as 97289th), that’s when all hell broke loose.

### Case 2

Like case 1, instruction at offset 0x489a is overwritten. Original opcode was `4e55`:

```bash
 41652 0x000262 41fa (0x55dfe6a45e80)
 41653 0x000264 2008 (0x55dfe6a45e82)
sixtyfour_lput e6a45e86 0x55dfe6a4aa12
 41654 0x004896 6100 (0x55dfe6a4a4b4)
 41655 0x00489a 4e55 (0x55dfe6a4a4b8)
```

Then, it became `0000`:

```bash
 93068 0x004896 6100 (0x55dfe6a4a4b4)
 93069 0x00489a 0000 (0x55dfe6a4a4b8)
 93070 0x00489c 5d02 (0x55dfe6a4a4ba)
 93071 0x0048a0 0000 (0x55dfe6a4a4be)
 93072 0x0048a4 0000 (0x55dfe6a4a4c2)
[...]
Illegal instruction: ba0e at 4ec0b4c4
```

This was caused by a possibly spurious write:

```bash
 93049 0x0000e0 2f2e (0x55dfe6a45cfe)
sixtyfour_lput e6a45d02 0x55dfe6a4a4b6
```

That is a BSR.W instruction i.e. a subroutine call. It is writing the next PC on the stack. So it seems that the stack went down into the instruction area?

SP was `e6a4a4ba` when instr #93049 was executed.

- Where is the instruction section supposed to stay in memory?
- Where is the stack section supposed to stay in memory?
- Maybe the loader fucked up the placement of the various sections?

### Case 3

```bash
    20 0x0042e8 6710 (0x55c8c6d8ef06)
default_xlate called, no no no! a=(nil)    21 0xffffaa37392753e2 4ed5 ((nil))
```

### Memory map

Ghidra reports this memory map:

![Untitled](Untitled.png)

## Main executable? `app`

At startup, OS-9 executes `CMDS/shell`. In turns, that seems to execute the `/startup` script. That one performs some initialization, then executes `appmon` which in turns starts (and restarts if it exits) `app`.

At the moment, running `app` with os9exec outputs the following and exits:

```bash
F$SetSys: unimplemented 08A6 (size=2)

Wildcard match failed for command 'del'

<ESC>&j@<ESC>[0m<ESC>[2J<ESC>[1;1H

```

This happens in a sort of infinite loop, presumably because `appmon` is trying to restart `app` forever.

The first line comes from os9exec: the app called F$SetSys (documented at page 51 of [http://www.icdia.co.uk/microware/tech/tech_call_1.pdf](http://www.icdia.co.uk/microware/tech/tech_call_1.pdf)) to set some system setting.

The second line comes from the app. Weird, because there is a `CMDS/del`.

The third line looks like a sequence ANSI escape codes. The first is unknown, the second resets all styles, the third clears the screen, the fourth moves the cursor to position 1,1. This means that the OS supports some ANSI control on the terminal(s).

The executable is supposed to run for a long time: it should not exit that soon.

Given that the last line is working on the terminal, I can assume everything was kinda OK up to that point. Maybe something wrong happened after that, and exits without printing an error.

I tried investigating, with notes in link below:

[Make `os9exec` print process address on syscall enter](os9exec-syscall.md)

Then https://github.com/biappi figured it out: the process wanted to compute the percentage of free space on disk, the OS reported zero bytes, then the process did divide-by-zero for which there was no trap handler, then the OS decided to kill it. He fixed this by patching the process binary i.e. `NOP`-ping the divide instructions:

![Untitled](Untitled%201.png)

The patch is recorder in this commit: https://github.com/egueli/AES2-HCM-HD10/commit/f02b62a5c00b0be1dbdbd45bb04139dcbd59afea

After patching an OS-9 binary, the CRC has to be re-computed. This can be done with the `fixmod` utility, which fortunately also works inside os9exec:

![Untitled](Untitled%202.png)

After this, `app`seems to finally work as it should:

![Untitled](Untitled%203.png)

It looks like a task management app. Maybe for handling a large set of concurrent tasks? And, it doesn’t seem to launch anything else by itself.

I know for sure that `fcontrol`, reverse-engineered to [find the system password](../Aesthedes%202%2085f7fd7209474298b3528148e30837ca.md), is eventually run by the physical Aesthedes. Somehow there must be a relation, direct or indirect, between `app` and `fcontrol` . Either the emulator fails to load something that `app` expects (and it just can’t handle the error and does nothing else except handling the user interaction), or `app` is actually not involved at all i.e. the physical system actually runs some other startup script.

Walking down the second option. Going backwards from `fcontrol`, I see (with `strings -f * | grep fcontrol | less -S)`) that the only “significant” program that invokes it is `main`. The latter seems to reveal more about the software architecture. It seems to launch three components:

- `m2dispsys` as the “DS”, associated with `/r0/dispout`;
- `m2gsys` as the “GS”, associated with `/r0/gsout`;
- the aforementioned `fcontrol` as the “CS”, associated with `/r0/csout`;

The paths associated with each component may be drivers, or may be something else. Gotta find out what `/r0` is.

I ran `strings -f * | grep main | less -S` on the `CMDS` directory to see if other programs reference `main`, and found `startup_gs`. Should look into that one as well.

By the way, `fcontrol` contains *a lot*  of interesting strings. It seems to coordinate the entire user interface, including graphics commands. 

## `fcontrol`

When started directly via os9exec, it crashes:

```bash
Process   Pid: 2, fcontrol, edition 501
    Exit code: E_BUSERR(102) bus error TRAP 2 occurred
  Directories: Current   - /app/dd
               Execution - /app/dd/CMDS
        Files: 00 fCons /term
               01 fCons /term
               02 fCons /term
               03 fCons /term [w]
               04 fCons /term [w]
 Last syscall: I$Write (0x008a)
    Registers: Dn=04FC9030 00000000 F79FF0B6 F7A2E48C 
                  DDDDDDD4 00000022 0002F480 00000000 
               An=04FC9030 5799056A F7A2E484 F7A2F058 
                  F7A2E488 F7A2E3AE F7A07010 F7A2E3A2 
               PC=F7A2F326 SR=0000       USP=F7A2E22C
 Executing: -->f7a2f326: 61ff 0001 584a 61ff 0000 BSR.L #$0001584a == f7a44b72
               f7a2f32c: 61ff 0000 b324 61ff 0000 BSR.L #$0000b324 == f7a3a652
       Memory: Static    -     F79FF010 - F7A2E490  193664 bytes
               Allocated - 000 F79FF010 - F7A2E490  193664 bytes
                           001 579953F0 - 57997570    8576 bytes
 Trap handler: 13 #44 cio, edition 6
```

It seems it tried to execute instructions at `f7a44b72`: is that valid memory?

That crash report is misleading! It reports an instruction that is NOT the last one (attempted to be) executed. The crashing one is at Ghidra offset `000b9f90`, a `CLR.B` instruction that tries to write to the absolute address `04fc9035`, which is not mapped in memory. Could it be a memory-mapped I/O device? In fact, that function (beginning at `000b9efc`) seems to write to different memory locations in the surroundings. It might be code that initializes a device.

That absolute address comes from reading Ghidra address `28c38`, which seems to be a global constant.

Ghidra disassembles that function this way: (I’ve labeled `hardware_base_address = 0x04fc0000; &hardware_base_address = 0x28c38`)

```c
void FUN_000b9efc(void)

{
  hardware_thing_1_base = hardware_base_address + 0x9020;
  hardware_thing_2_base = hardware_base_address + 0x9028;
  hardware_thing_3_base = hardware_base_address + 0x9030;
  if (DAT_0000b71e != 0) {
    *(undefined *)(hardware_base_address + 0x9027) = 0;
    *(undefined *)(hardware_thing_1_base + 3) = 0;
    *(undefined *)(hardware_thing_1_base + 7) = 4;
  }
                    /* crash here! */
  *(undefined *)(hardware_thing_3_base + 5) = 0;
  *(undefined *)(hardware_thing_3_base + 1) = 0;
  *(undefined *)(hardware_thing_3_base + 5) = 4;
  *(undefined *)(hardware_thing_3_base + 7) = 0;
  *(undefined *)(hardware_thing_3_base + 3) = 0;
  *(undefined *)(hardware_thing_3_base + 7) = 4;
  if (DAT_0000b726 != 0) {
    *(undefined *)(hardware_thing_2_base + 5) = 0;
    *(undefined *)(hardware_thing_2_base + 1) = 0xff;
    *(undefined *)(hardware_thing_2_base + 5) = 0x2c;
    *(undefined *)(hardware_thing_2_base + 7) = 0;
    *(undefined *)(hardware_thing_2_base + 3) = 0xff;
    *(undefined *)(hardware_thing_2_base + 7) = 0x2c;
  }
  return;
}

```

The first `if`is not hit, so it crashes when writing 0 at `hardware_thing_3_base + 5` .

Solved by patching the emulator sources so that it does dump any writes to /dev/null: https://github.com/biappi/os9exec/commit/c0eedd80e895a7034e8103d5599d71fc09d9bf51

### Fixing file read with null buffer

After the patch above, it crashes again. This time it’s an assertion failure on the I$Read system call because fcontrol gave a null buffer address to write to.

The offending instruction is not in the program memory, but in data memory. Maybe it loaded some external program (overlay)?

The last program instruction before going into data is at around Ghidra address `0xb38c6` (in `FUN_000b3772`). That’s where the subroutine `FUN_000bf63e` is called, that calls trap `0xD` with code `0x23`. This subroutine has many callers, so it may be important for something.

The last thing written to the console before this code is `Initialising file system ...`. By looking at the call graph, the root function may be `init_filesystem_1()`.

Trap 0xD is a user trap, installed via the T$Link system call. T$Link is documented [here](http://www.icdia.co.uk/microware/tech/tech_call_1.pdf) at page 65. I could see that earlier in the execution, `fcontrol` calls T$Link with the `cio` argument. (Console I/O? Common I/O?)

Note: in order to analyze `cio` with Ghidra, one should import it with the option “Register entrypoints” disabled. It is enabled by default, but it causes an import error when the file is not an executable with an entry point; trap handlers do not have an entry point.

### Null address backtracking

- The crash happened at instruction count #861155 due to A0 being zero.
- #861152 sets A0=D1
- #861129 (`G0xb38be`) sets D1=(A7+4) i.e. the content of 0xf79ee290. Ghidra calls that `local_86` in `FUN_000b3772` .
- `local_86` is the return value of `FUN_000be13c` , presumably a `malloc` -like function. Debug strings say it’s “MMALLOC”
- #861117 sets D0=0. Did the allocation fail?
- By looking at the other invocations of MMALLOC (i.e. by dumping the processor state whenever `G0xbe13c` is hit), this is the first one where D0=0. Is the caller trying to allocate zero bytes? Then of course it didn’t work.
- D0 was filled by a file I/O read at `G0xb380e` (Ghidra calls that `local_6a`).
- Those I/O reads are from `/h0@` i.e. the hard disk in physical mode. But the emulator doesn’t work with a raw RBF image and returns all zeros. This can be seen by looking at the debug output with emulator options `-d 0x202 -d2 0x202` (show normal and detailed information about syscalls and file operations) That’s why D0=0 and everything goes crazy later.

This has been fixed with a crude workaround, that fills the buffer with non-zero values when reading doing that critical read:

https://github.com/biappi/os9exec/commit/54ac0ae40eb7176266af1d36c010cacd4211e984#diff-98da83c946e20b0983647b2ba23cab3cb2a561a8359caf92bbf20a011a6ff63aR473-R478

A better fix would be to provide a more realistic RBF header. But my attempts so far (using the `RAM_zero` array (https://github.com/biappi/os9exec/blob/6e2269ea5527c72fa6573a1fd910d2d45a20ac30/Source/OS9exec_core/file_rbf.c#L208) or the first sector from the Aesthedes image) have been unsuccessful as the program crashes while reading bogus address 0x00000005.

Anyway the workaround above makes `fcontrol` continue. Now it hangs at “Initializing color system”. It seems to wait for an event coming from a module called `DM_DISPSYS`. We cannot find it in the filesystem, so it might be in the Aesthedes ROMs.

# Dumping the ROMs

We want to have a fully working Aesthedes 2 in an emulated environment. OS9exec is not enough, because it doesn't know anything about the video cards and other peripherals. We should use an emulation platform that supports hardware emulation as well, like MAME.

For this, an essential step is to obtain the peripheral drivers, in particular the video drivers (like `DM_DISPSYS` above). To maximize compatibility, they should be obtained from the machine itself.

The drivers can be downloaded either by physically reading the ROM chips (risky) or by reading the data from a live machine. The latter is a software-only solution that should be feasible because the 68020 has no MMU, therefore any program can read everything on the system memory.

We need to write a program that runs on the system and writes data from memory to a file. For this, we need an SDK to write/build programs, and the OS to run it.

The following seems to be a suitable SDK:

[https://github.com/HoldcroftJ/os9_68k_sdk_v12](https://github.com/HoldcroftJ/os9_68k_sdk_v12)

The SDK is for Windows. Hopefully it works with Windows XP, installed on VirtualBox. Or maybe via Wine?

(I tried with Windows 98. It's extremely sluggish and there are no Guest Additions)

[Windows XP Professional SP3 x86 : Microsoft](https://archive.org/details/WinXPProSP3x86)

Serial: `MRX3F-47B9T-2487J-KWKMF-RPWBY`

Although, running Windows XP from VirtualBox is a bit inconvenient. It takes a lot of CPU and storage for my meager Macbook. So, I'll try Wine, and resorting to XP in case something doesn't run as expected.

## Compiling a C program for OS-9 68k via the OS-9 SDK under Wine

Assuming there's a C source file called `main.c` in the SDK root.

From the SDK root, on a Linux or Mac terminal (tested on Mac):

```bash
ln -s $(pwd) ~/.wine/dosdevices/m:
export MWOS="M:\\"
(cd DOS/BIN && wine xcc.exe -mode=c89 -o ../../main ../../main.c)
```

Where:

- `xcc.exe` is the Microware UltraC compiler
- `-mode=c89` is to set to C89 executive mode. This allows to set the output file name with `-o`.

It's important that xcc.exe is launched from its own directory, otherwise you'll get the (very cryptic) error “executive received argument list length error while forking…”.

Once the executable (`main`) is created, it can be tested with os9exec. Just move it into `CMDS` then run `os9exec main`.

# MAME

It could be possible to emulate an Aesthedes 2 with MAME. After all, it can emulate:

- systems with multiple screens, e.g. [Ninja Warriors](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=ninjaw&back_games=ninjawj;&search_id=0) (`ninjaw`) ([ROMs](https://wowroms.com/en/roms/mame-0.139u1/download-the-ninja-warriors-world/5642.html))
- systems with the 68k processor family, e.g. CD-i
- systems with a hard-drive (all games that need a CHD file, incl. CD-i)
- systems with the EF9365 video chip (i.e. same as the Aesthedes), e.g. [Apollo 7 Squale](http://hxc2001.free.fr/Squale/) ([other link](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=squale))
- systems with non-trivial keyboard, e.g. [VeriFone Tranz 330](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=tranz330&lang=en) ([ROMs](https://wowroms.com/en/roms/mame/download-tranz-330/109258.html)). The MAME technical docs mention `tranz330.lay` as an [example MAME layout file](https://docs.mamedev.org/techspecs/layout_files.html#example-layout-files) with clickable buttons.

## Building MAME on Windows

Remember to set `video` to `opengl`: default on Windows is `d3d` that doesn’t work.

## Running MAME on Windows

Run in my desktop PC:

`C:\Users\ris8a\Documents\dev\Aesthedes\mamedev\msys64\win32env.bat`

Then in the prompt:

```c
cd ..\..\..\mame
mame
```

## Building MAME on Mac


```
make -j5 TOOLS=1 SOURCES=src/mame/uilli/fake68.cpp SUBTARGET=fake68 REGENIE=1
```

## Running MAME on Mac

```
./fake68 fake68
# Or, run with debugger:
./fake68 fake68 -debug 
```

Note: if it crashes with segmentation fault, it might be the configuration being corrupted. Try with
```
rm cfg/fake68.cfg
```

## Running a CD-i title in MAME

We need CD-i BIOS ROMs first: [https://archive.org/details/cdibios](https://archive.org/details/cdibios)

Then, the image of a CD-i title like Hotel Mario: https://romsfun.com/download/hotel-mario-122391/4

Then, follow the steps described in [https://www.youtube.com/watch?v=bmq_uifhYVc](https://www.youtube.com/watch?v=bmq_uifhYVc)

## Emulating an Aesthedes2-like machine on MAME

While we wait for the Aesthedes ROMs to be dumped, we're going to emulate a machine that is a close as possible to the real Aesthedes. And see if it can boot OS-9, mount the AES2 image and run `fcontrol`; in other words, to get at the same level as we did with `os9exec`.

Let's start from OS-9 itself. Can an OS-9 kernel run into MAME? Theoretically we know we do, because CD-i runs OS-9 under the hood. But how about OS-9 on a hardware we control?

Fortunately there's [os9-m68k-ports](https://github.com/John-Titor/os9-m68k-ports), a GitHub repo with ports of OS-9 to various 68K systems. One of them is the [CB030](https://www.retrobrewcomputers.org/doku.php?id=builderpages:plasmo:cb030), a homebrew retrocomputer project. 

It is somehow possible to emulate the CB030's hardware in MAME, then run OS-9 on top of it. In [this MAME fork](https://github.com/biappi/mame) there is a new machine, `fake68`, that aims to emulate a CB030.

os9-m68k-ports require the [OS-9 SDK v1.2 repo](https://github.com/John-Titor/os9_68k_sdk_v12) to be checked out in a sibling directory. And several other changes were required to make it build correctly. The contents have been copied as a subdirectory of our [os9-builder](https://github.com/biappi/os9-builder) repo, and the OS9-SDK has been linked as a submodule. To obtain it, remember to `git clone` it incl. submodules:

```bash
git clone --recurse-submodules git@github.com:biappi/os9-builder.git
```

From this repo, one can follow the instructions as in [`os9-m68k-ports/README.md`](https://github.com/biappi/os9-builder/tree/master/os9-m68k-ports#building) to build the SDK. They seem to work on Mac.
To set up the M: drive, one can type this from the `os9-builder` directory:

```bash
os9_builder_root=$PWD; (cd ~/.wine/dosdevices/; rm -f m:; ln -s $os9_builder_root m:)
```

Then, start the build:

```bash
cd os9-m68k-ports/ports/CB030
../make.sh build
```

The output file that is relevant to us, i.e. the OS-9 ROM image that can run on a CB030, is in `os9-m68k-ports/ports/CB030/CMDS/BOOTOBJS/ROMBUG/romimage.dev`. It can be copied in the MAME source tree in the `roms/fake68` directory of our MAME fork.

Before running the emulator, you may need to edit the ROM table `src/mame/uilli/fake68.cpp` so it has the right file size. The CRC and tha SHA values may be all-zeros, e.g.:

```c
    ROM_LOAD("romimage.dev", 0x000000, 399910, CRC(00000000) SHA1(0000000000000000000000000000000000000000))
```

This is how one can rebuild and run MAME on Mac OS:

```sh
make -j5 TOOLS=1 SOURCES=src/mame/uilli/fake68.cpp SUBTARGET=fake68
./fake68 -window fake68
```

While the emulator is running, it takes full control of the keyboard. Hit the Del key to enable the UI controls to e.g. exit.

The emulator starts with the boot ROM, and drop us into the RomBug prompt. Type `g` to start booting: OS-9 should start. It shows the error `pd: can't open current directory`, then the OS-9 shell prompt (`$`). With `mdir` one can see which commands are supported.

But, OS-9 doesn't seem to know how to access external storage via CF. So it wouldn't be able to read an RBF image.

The hardware provides CF registers at 0xffffe000 to 0xffffefff. Let's see if, at a minimum, OS-9 does actually try to read/write on these registers.

The MAME debugger command for watchpoints is

```
wpset ffffe000,1000,rw
```

After some debugging, it looks like OS-9 doesn't read the CF registers itself. I thought it needed assistance from the bootloader (and [I tried to debug that](bootrom-cfide.md)), but it just doesn't read anything automatically. Biappi noticed that it does when typing this to the OS-9 prompt:

```
dir /c0_fmt
```

But it fails with `error #000:244`.


## Storage driver 

Trying to make the compact flash storage layer in the CB030 port is proving a
bit difficult, as the custom drivers written in the port (which are not
originally from Microware, but from the port's authors) seem to have bitrotten
a bit.

One solution to quickly get some storage in the mame emulator, is trying to use
a big ramdisk, so we don't need to bother with unrelated hardware controllers,
and we could use MAME's nvram machinery to save and persist the ramdisk.

The ramdisk is mapped at `0xa000_0000` and is maxed out to what the OS9 ramdisk
can support: about 16MBs, as the ramdisk size is defined by an uint16_t numbers
of sectors, that by default are 256 bytes, so:

    >>> (0xffff * 256) / 1024 / 1024
    15.999755859375

When the OS9 kernel will boot, if the ramdisk is empty (e.g. the first time
starting a version of the emulator with the ramdisk support) it will be
automatically formatted as an RBF filesystem.

The file can be found in `mame/nvram/fake69/nvram` and it's just the raw dump
of the memory region. As such, it can be used with `os9-toolshed` to be
inspected or to copy files from and to the image.

For example:

    willy@Hitagi mame master$ export OS9_TOOLSHED="../../../../os9-toolshed/build/unix/os9/"
    willy@Hitagi mame master$ export AE_DD="../../../../os9exec-git_code/dd/"
    willy@Hitagi mame master$ export PATH="$OS9_TOOLSHED:$PATH"

    willy@Hitagi fake68 master$ os9 dir nvram/fake68/nvram
                               Directory of nvram/fake68/nvram
    CMDS            xx              
    willy@Hitagi fake68 master$ 

I also managed to copy the Aestedes `CMDS` directory from the expanded image I
used with `os9exec`.

    willy@Hitagi mame master$ os9 dsave -e $AE_DD/CMDS nvram/fake68/nvram,CMDS
    os9 copy '../../../../os9exec-git_code/dd/CMDS/scitextape' 'nvram,CMDS/scitextape'  -b=32768
    os9 copy '../../../../os9exec-git_code/dd/CMDS/comld' 'nvram,CMDS/comld'  -b=32768
    os9 copy '../../../../os9exec-git_code/dd/CMDS/pd' 'nvram,CMDS/pd'  -b=32768
    [..]

Unfortunately the copied binaries seem to not immediately run, and they all
result in the error

    'command' found as module relative to data directory

whatever the current directories changed with `chx` and `chd` are.

Here's why: OS-9 has the concepts of "data directory" and "execution
directory". Both can be set with `chd` and `chx` respectively. It seems that if
the data directory contains `CMDS` and the execution directory is not properly
configured, then the above error appears. This can be fixed with:

```
chx /r0/CMDS
```

. After this, simple executables like `echo` can be run, provided there is also
the `cio` library, here's how:

1. using Toolshed, copy `echo` and `cio` into `CMDS`:

```sh
os9 makdir mame/nvram/fake68/nvram,CMDS
os9 copy ../../HD10/HD10/CMDS/cio mame/nvram/fake68/nvram,CMDS
os9 copy ../../HD10/HD10/CMDS/echo mame/nvram/fake68/nvram,CMDS
```

2. Start the emulator, set the execution directory, then run the command:

```
...
pd: can't open current directory. $ chx /r0/CMDS
$ echo "hello world!"
hello world!
```


### Check permissions

The command files need to be marked as executables in the OS9/RBF filesystem. In
some cases, Toolshed can copy files without that permission. In this case, that's
the error

    $ fcontrol
    mshell: can't execute "fcontrol"  - Error #000:214

Check the file permissions:

    $ dir -e CMDS
                               Directory of CMDS 24:00:00
     Owner    Last modified  Attributes Sector Bytecount Name
    -------   -------------  ---------- ------ --------- ----
      0.0     24/06/16 0355   ----r-wr      25     20192 cio
      0.0     24/06/16 0355   ----r-wr      75    658492 fcontrol

Those are **incorrect**, so fix them:

    $ attr fcontrol -pe -e
    --e-rewr  fcontrol
    $ attr cio -pe -e
    --e-rewr  cio

The **working** permissions are:

    $ dir -e
                                Directory of . 24:00:00
     Owner    Last modified  Attributes Sector Bytecount Name
    -------   -------------  ---------- ------ --------- ----
      0.0     24/06/16 0355   --e-rewr      25     20192 cio
      0.0     24/06/16 0355   --e-rewr      75    658492 fcontrol


## Running `fcontrol`

Now that we've figured out how to run simple executables, let's see if `fcontrol` also works:

```
chx /r0/CMDS
fcontrol
```

... and magically, it starts up! We can see the ANSI/ASCII art of the startup sequence, just like when it was running on os9exec. It still hangs at "Initializing color system", but I'm positively surprised that it reaches that point without all the issues we had to fix in os9exec.

The reason it hangs at that point is IMO the same: it's waiting for a signal from a driver that doesn't exist in the system because the original ROMs are not yet dumped and handled by MAME.

## Remap `c0` and `h0` to `r0`

The NVRAM mechanism showed effective at letting the OS-9 manage a virtual
storage device in MAME's emulated environment. There are some issues left:

* The kernel (ported for CB030) tries to mount `c0` at startup i.e. the
  CompactFlash, that is buggy. The current workaround is typing `chx /r0/CMDS`
  and `chd /r0` just after startup.
* Aesthedes' `fcontrol` attempts to open `h0` in raw mode. The name is
  hardcoded. Luckily, the program doesn't seem to be bothered that the device is
  missing in the CB030 kernel. At least at startup.
* Storage is currently limited to 16MB.

To address the first two issues at once, we may try setting up aliases so that
`c0` and `h0` become equivalent to `r0`.

The CB030 README states that `/dd` aliased to `/c0`. This is done in
`cfide_descriptors.make`, that builds the `dd` descriptor with the same linker
arguments as another descriptor (was `c0` then later changed to `r0`) but with a
different output file name.

By deleting the existing targets about `c0`, and replacing them with a target
that makes the alias to `r0`, the system seems to work correctly. Adding another
alias for `h0` is a no-brainer.

### Emulating storage with original ROMs

The HDD image contains the `main` executable that starts `fcontrol`. The
original ROMs will likely start up the system by running this executable. As
described in the notes above, `main` also launches two executables that reside
in `r0` (see notes above), or are somehow linked to files in `r0`. This means
that the actual system will work with sepatate storage devices `r0` and `h0`. As
an educated guess, `r0` could be a RAM disk for temporary files.

Therefore it is important that the HDD image we have, is accessible in a way
that is compatible to what the OS-9 in the ROMs expect. This means some sort of
SCSI device: after all, we know that the HDD image was extracted by a 256-byte
SCSI HDD.

Alas we (currently) have no details on e.g. which SCSI controller is been used.
From [Youtube videos](https://youtu.be/aVfmSLoi2Wg?si=wGnEy56MvtuNh5NJ&t=559),
we see SCSI controller chips such as the NCR 5386 and NCR 53C90A on some of the
Aesthedes PCBs. Alas these two chips don't seem to be emulated (yet) in MAME.
But the HDD image seems to include several SCSI drivers in `CMDS/BOOTOBJS`,
including the OMTI 5100 that is emulated in MAME. It could then be a candidate
device to be included in the emulated hardware description in MAME.

Bitsavers has an [extremely useful technical manual](http://www.bitsavers.org/pdf/sms/omti_5x00/OMTI_5x00.pdf)
that confirms the OMTI5100 referenced in the MAME source code is basically
the same as the OMTI5400 referenced in OS-9.


## Running `main`

Unlike what was stated before, it's not actually true that `fcontrol` requires
an executable that is present in the (currently unavailable) ROMs. The other two
executables launched by `main`, `m2dispsys` and `m2gsys`, seem to provide what
`fcontrol` is waiting for during its startup sequence. So, by running `main` we
may be able to launch `fcontrol` successfully even without the ROMs.

`main`, when launched, stops almost immediately due to it failing to launch a
module called `AE_CONFIG`. By creating a mock executable (commit f00f0b9) with
the same name and does nothing, and installing it into `CMDS`, it can continue
running.

After that, it stops with `Cant Fork GS : 205` (205 is `E_BMID`, Bad Module ID).
"GS" hints at `m2gsys`. Running that executable from the shell leads to the
error `mshell: can't execute "J"  - Error #000:216` (216 is `E_PNNF`, Path Name
Not Found).

The above happened with the MAME emulation. When trying the same with os9exec,
there are different failures: `main` shows error 214 (`E_FNA`, File Not
Accessible) and the shell shows the following:

```
# Emulation could not start due to OS-9 error #000:214 (E_FNA): 'm2gsys'
#   File Not Accessible
```

There is definitely something wrong with `m2gsys`, or the OS-9 kernels we're
using aren't compatible with it somehow.

Running it again with `os9exec -d 0x20` to log module loading, reveals the
following:

```
# load_module: loaded 655361 bytes from module's file
# load_module: (found) mid=3, theModuleP=7FE78BD27000, ^theModuleP=4AFC0001
# load_module: bad size: 831324>655361, E_BMID
```

(os9exec seems to hide the actual error code `E_BMID`. That would make it
consistent with OS-9 on MAME).

It looks like `m2gsys` is truncated. Indeed its size is an odd number of bytes,
which is weird for a 68k executable. In fact, several executables in `CMDS` seem
to have the same issue. Could it be a side-effect of running `dcheck` on the HDD
image when I was trying to get the password?

Luckily, `os9 copy` can work on the original HDD image and copy the file in its
entirety.

After installing the correct `m2gsys` into MAME's NVRAM, `main` doesn't show
that error anymore... but it clears the screen and seems to enter an infinite
loop. os9exec also clears the screen but shows a crash (null-pointer exception)
preceded by `GS terminated with 208` (208 is `E_UNKSVC`, Unknown Service Code).
I can't tell if both emulators are misbehaving for the same underlying cause, or
os9exec has some emulation bug. 

The problem is actually not in `main` but in `fcontrol`. If `fcontrol` is
launched via the shell, it hangs as well. It looks like the mock `AE_CONFIG`
causes it to hang; probably because it expects some event to be delivered. If
`AE_CONFIG` is removed, `fcontrol` starts normally, and hangs at "Initializing
color system" as before.

## Running `fcontrol` with mock `AE_CONFIG`

So, what does fcontrol need from AE_CONFIG to start correctly?

`load_configuration` (function 0x3a65a in Ghidra) calls T$Link to load
AE_CONFIG; it reads some data from it, sets a few global variables, calls some
functions, then unloads it. Some of these steps makes it hang; hopefully it's
just one step. So we may use the MAME debugger to skip parts of that function to
find the culprit, e.g. by live-patching the function with NOPs.

Beware that the MAME debugger does not always work as expected: in particular,
Step Into, Step Next and Run to Cursor may cause weird side-effects if an OS9
syscall happens in-between, and make it look like the CPU goes into infinite
loop inside the kernel. On the other hand, by adding a breakpoint on the next
instruction it works correctly. It's recommended to use the state-save (`ss`)
and state-load (`sl`) commands to revert to a known good state if things go
awry.

### A crash in the middle of an iteration

Thanks to this new knowledge, it seems that `load_configuration` actually runs
fine but the system hangs later. Here's a pseudo-stacktrace:

* somewhere in function 0xb697a (named `fill_screen_with_stuff` in Ghidra)
* invoked by function 0x3b0c2 at 0x3b1e4 (note: it's the second invocation)
* invoked by `main` function (0x30272) at 0x30310.

Function 0xb697a handles 80-byte arrays filled with value 0x20, and has a loop
that is supposed to run 20 (0x14) times. If 80x20 is the character size of the
text screens, then this function may have to do with text output. Actually the
screens have 25 lines, but it seems that only the first 20 are used in the
startup texts.

The loop has an iterator that starts at 20 (or 21) and should end at 40, but the
hang begins when it reaches 37, i.e. the 17th iteration. A stack overflow
triggered by an invalid configuration value, maybe?

The last instruction in application code before the hang was at 0xb9610 (`bsr.l
0xbf646`), that calls the CIO function to print a null-terminated string.

fcontrol Ghidra offset: 0xE01DB0

Tracing info:

MAME debugger commands:
```
sl after_config_6
trace hang.tr,,noloop,{tracelog "A7=%08x D0=%08x ", A7, D0}
g
[wait until frame0=~7030]
trace off
```

Analyzer commandline:
```sh
cat mame/hang.tr | nl -w8 -ba |perl -n -e '/(.{33})(.{8})(.*)/ && (printf "%s%18s%s\n", $1, (hex($2) >= 0xE31DB0 && hex($2) < (0xE31DB0 + 0xA0C3C)) ? sprintf("fcontrol+%06x", hex($2)-0xE01DB0) : $2, $3) || print' >  hang_trace.txt
```

The first execution of b69f2 is at line 20377. Last-but-one (16th iteration) is
at 95462, last (17th iteration) is at 100475.

At the 17th iteration, at line 105140, a `bcc` branches differently between the
two iterations. That instruction is at memory address 0x13d60, that is allocated
to the `sc68681` driver (module base at 0x139f8; it seems that the kernel loads
this driver at the same location at every startup, so one can set a breakpoint
at the absolute address). Maybe the emulated hardware is buggy? Or the driver
itself is?

We have sources for the driver: `MWOS/OS9/SRC/IO/SCF/DRVR/sc68681.a` and the
branch is at around line 1072 (`bhs` is a synonym for `bcc`):

```
Write: move.w sr,d6 save current IRQ status
 move.w IRQMask(a2),sr mask IRQs
 move.w OutCount(a2),d2 get output buffer data count
 cmpi.w #OutSiz,d2 room for more data?
 bhs.s Write00 ..no; wait for room
```

A possible explanation is that the transmit buffer for the serial port used to
send those characters, is never emptied and it gets eventually full.

A debugger command can print transmit buffer level after each write to any
serial port:

```
bpset 13d60,1,{ printf "port@%06x count=%d", a2, w@(a2 + 0x72); g }
```

(0x72 is the offset from the start of the variables section for the driver,
which is held in A2. That offset is calculated by the linker as the sum of 0x56
i.e. the space required by other object files linked in, and 0x1c that is
`OutCount` in `sc68681`)

With this, one can see that two serial ports are used overall: one at address
0xfc9390 (the one with the OS-9 prompt), one at 0xffde70 (where some ANSI codes
are printed when running `main` or `fcontrol`). Before launching `main` and
shortly after that, the levels are arouns 10 and never higher than 60; after
some point, the second one reaches 140 and that's where the system hangs. I
guess that `fcontrol` may reconfigure the driver in a way that it doesn't
transmit anymore. It could be the enabling of some flow control, but changing
the serial port setting in MAME to RTS leads to no change; moreover, the are no
reports of system calls that could enable the flow control. And, none of the
driver's variables seem to change significantly. The only exception seems to be
the parity configuration byte, sometimes changing from 0 to 2 for a couple
characters then back to 0 (note that `sc68681.a` probably has a typo in line 840
since 3 is not a value that can be contained in two bits), but this happened a
few times before the hang. Moreover it doesn't seem to reflect a register write
to the DUART.

So my attention is going to focus on the emulated MC68681. Maybe it is behaving
incorrectly?

I enabled `VERBOSE` in `mc68681.cpp` to see what happens at MAME side. When
sending a byte (`53` hex in this example, followed by `59`) from the output
buffer that is partially full, this is what is being logged:

```
[:duart] Writing 68681 (:duart) reg 3 (THRA) with 53 
[:duart] Interrupt line not active (IMR & ISR = 00) 
[:duart] Interrupt line active (IMR & ISR = 01) 
[:duart] Reading 68681 (:duart) reg 5 (ISR) 
[:duart] returned 09
[:duart] Writing 68681 (:duart) reg 3 (THRA) with 59 
[:duart] Interrupt line not active (IMR & ISR = 00) 
...
```

The OS-9 driver writes the byte to THRA. The emulated chip deasserts the
interrupt, sends the byte, then asserts it. The driver looks at the ISR, sees
that bit 0 (TxRDYA) is asserted, and proceeds to send the next byte in the
buffer.

But at some point, this chain reaction breaks:

```
[:duart] Reading 68681 (:duart) reg 5 (ISR) 
[:duart] returned 09 
[:duart] Writing 68681 (:duart) reg 3 (THRA) with 5b 
[:duart] Interrupt line not active (IMR & ISR = 00) 
[:duart] Interrupt line active (IMR & ISR = 01) 
[:duart] Reading 68681 (:duart) reg 5 (ISR) 
[:duart] returned 09 
[:duart] Reading 68681 (:duart) reg 5 (ISR) 
[:duart] returned 09 
[:duart] Reading 68681 (:duart) reg 5 (ISR) 
[:duart] returned 09 
...
```
It looks like the driver reads the ISR in an infinite loop?

Is this triggered by something OS-9 did? To answer this, I dumped all the
driver's registers once again. The MAME log now has logs for both the driver and
the port. I wrote a Python script (`mc68681_tracker.py`) to see if this change
in behavior happened with some change in the driver state but nothing relevant
came up.

Let's debug the interrupt service routine. It starts at `MPSIRQEx` (whose
address should be 0x13f6a, by looking at the output of `irqs`). At 0x13fac (line
1453 in driver source) it checks if there is anything to handle; during the hang
it seems to branch and return early from the interrupt. So, why does the port
trigger an interrupt with no events?

With verbose port logging, I see this:

```
[:duart] Reading 68681 (:duart) reg 5 (ISR)
[:duart] returned 09
[:duart] Writing 68681 (:duart) reg 3 (THRA) with 5b
[:duart] Interrupt line not active (IMR & ISR = 00)
[:duart1] Interrupt line active (IMR & ISR = 01)
[:duart1] Reading 68681 (:duart1) reg 5 (ISR)
[:duart1] returned 01
[:duart1] Writing 68681 (:duart1) reg 3 (THRA) with 48
[:duart1] Interrupt line not active (IMR & ISR = 00)
[:duart1] Writing 68681 (:duart1) reg 5 (IMR) with 02
[:duart] Interrupt line active (IMR & ISR = 01)
[:duart] Reading 68681 (:duart) reg 5 (ISR)
[:duart] returned 09
```

It looks like everything stopped when somehow IMR was written a different value
*from a different port*. Why was `duart` also affected? And why the interrupt
mask was changed anyway?

(by the way, it looks like the DUART driver is used as an example SCF driver in
[OS-9 Insights An Advanced Programmers Guide to
OS-9](http://www.icdia.co.uk/books_os9/os9insights_ed3.pdf), chapter 29)

It looks like the driver uses a shadow copy of IMR in memory. This is required
because the driver has to know which interrupt types were masked out, but IMR
cannot be read from the 68681 directly (reading that register will load ISR
instead). For *reasons*, this shadow resides into a "OEM globals" area (see
chapter 29.5 in the book, page 401 (pdf:421)). Is it possible that both
instances are mistakenly reading/writing into the same address?

The first port that is initialized (at base addr A2=0xffde70, A1=0x0141dc)
* global mask offset is 0x70;
* offset to the global pair for this device is 0;
* entry of the pair in the OEM_Globals is 0x7c4;
* this is saved to Globl(a2) = 0xffdee6.

The second port that is initialized (at base addr A2=0xfc9490, A1=0x0142d6)
* global mask offset is 0x70;
* offset to the global pair for this device is 0;
* entry of the pair in the OEM_Globals is 0x7c4;
* this is saved to Globl(a2) = 0xfc9506.

Is the same offset saved to two separate locations? Really?

Now let's look at the next-occurring serial interrupt
(at base addr A2=0xfc9490, A1=0xfc9600):
* Globl(a2) = 0xfc9506;
* offset to the pair in the OEM_Globals is 0x7c4...

So they're all reading and writing to the same offset 0x7c4! Of course they'd
eventually crash into each other...

It seems that the "offset to the global pair" (defined as `DevCon` (Device
Constants) in the book) should be 0 for the first device, 2 for the second etc.
(it should increment by 2 because sc68681 needs two shadow bytes). But in
`systype.d` it was set to 0 for all 4 ports (`TERM`, `CRT80`, `CRT81` and
`CRT82`). A quick fix made them finally work independently from each other.

### Trying to make GS not terminate

Now that the serial ports are disentangled, fcontrol seems move forward. But,
now we get a "GS terminated with " followed by a seemingly random number, and
the system becomes unresponsive.

Firing up Ghidra again, I try to see (1) how does it get the termination code
(and why is it broken) and (2) why does GS gets prematurely terminated. It might
also be that it crashes when trying to run some action triggered by `main` or
`fcontrol`.

Some reverse-engineering reveals another secret: the unresponsiveness is caused
by an infinite loop, that happens only if some global variable is set. And that
is set if `main` is invoked with the `-t` option. That same variable also
triggers the printing of `STARTING SYSTEM WITH DEBUG-OPTIONS` so it's safe to
assume it's about some debug mode. With that option, `main` exits to the prompt,
removing the need of resetting the machine. It also prints the output (stdout?)
of CS, DS and GS to `/r0/csout`, `/r0/dsout` and `/r0/gsout` respectively, but
so far these files, although created, contain zero bytes.

The "GS" (Graphics System?) mentioned in the error should be the `m2gsys`
executable. When it is launched from the shell, I see it running for a while
with no output, then waits with the `stop` 68K instruction. I can return to the
prompt with a Ctrl-C. Therefore `main` might be calling it in a different way,
that makes it end prematurely. Alas there are no other error messages, so one
way to figure out what's wrong is to debug `m2gsys` and see where it exits.

(0xefc100 in MAME is 0x30270 in Ghidra -> offset = 0xecbe90)

Tracing the point where the app crashes:
* m2gsys's `main()` is at 0x30270 in Ghidra.
* It calls the function at 0x5f6c6 at 0x302f2.
* In turns, it calls the function at 0x3b5ee at 0x5f79c.
* (`m2gsys_2`) In turns, it calls the function at 0x31294 at 0x3b622.
* (`m2gsys_3`) In turns, it calls the function at 0xea132 at 0x312ae.
* (`m2gsys_4`) In turns, it calls the function at 0xea436 at 0xea18c.
* In turns, it calls the function at 0xea338 at 0xea46c.
* (`m2gsys_5`) In turns, it calls the function at 0xebaae at 0xea358.
* In turns, it calls OS-9's F$Exit, causing the program to stop.

So there's no crash, but an expected exit. Why does it exit then? 
The answer is in the function at 0xea436: it calls 0xeb7b8 which calls F$Event,
but it seems to fail. This is reported as a -1 value, which causes 0xea338 to be
called.

0xeb7b8 is called with D0=0x20001 and D1=2. It eventually calls F$Event with
D1=0xA (that means Ev$Set), D0 (signal ID) = 0x20001 and D2 (new event value) =
2. The system call returns with D1=0xFFFFFFFF, signaling an error. Which is
weird, because the documentation says the only possible error is 0xa7
(E$EvntID). A different error then?

Maybe the system call was misused? Here's the list of last syscalls performed:

```
OS9 syscall: m2gsys+000eb72a  F$Event       (Ev_Link) D0: 00efcc6e, D1: 0000, D2: 48d6, D3: bc50, A0: 00efcc6e (CS_GS) 
Now loaded: CS_GS@00e2f9c0 
OS9 syscall: m2gsys+000eb72a  F$Event       (Ev_Creat) D0: 000003e7, D1: 0002, D2: ffff, D3: 0000, A0: 00efcc6e (CS_GS) 
OS9 syscall: m2gsys+000eb7d0  F$Event       (Ev_Set) D0: 00010000, D1: 000a, D2: 0000, D3: bc50, A0: 00efcc6e (CS_GS) 
OS9 syscall: m2gsys+000eb72a  F$Event       (Ev_Link) D0: 00efbb16, D1: 0000, D2: 48d6, D3: bc50, A0: 00efbb16 (EV_DISPSYS) 
OS9 syscall: m2gsys+000eb72a  F$Event       (Ev_Creat) D0: 000003e7, D1: 0002, D2: ffff, D3: 0000, A0: 00efbb16 (EV_DISPSYS) 
OS9 syscall: m2gsys+000eb82a  F$Link        D0: 0000, A0: bac6 (DM_DISPSYS) 
OS9 syscall: m2gsys+000eb650  F$DatMod      D0: 00000400, D1: 8000, D2: 0003, D3: bc50, A0: bac6 (DM_DISPSYS) 
OS9 syscall: m2gsys+000eba3e  F$ID           
Now loaded: DM_DISPSYS@00e2f570 
(3)
OS9 syscall: m2gsys+000eb7f6  F$Event       (Ev_Wait) D0: 00020001, D1: 0004, D2: 0000, D3: 0000, A0: 00ef0dc2 
OS9 syscall: m2dispsys+00042510  F$Sleep       D0: 8000000a 
OS9 syscall: m2dispsys+00042510  F$Sleep       D0: 8000000a 
OS9 syscall: m2dispsys+00042510  F$Sleep       D0: 8000000a 
OS9 syscall: m2dispsys+00042510  F$Sleep       D0: 8000000a 
(4)
OS9 syscall: m2dispsys+00042678  F$Event       (Ev_Link) D0: 00fd1912, D1: 0000, D2: a93a, D3: 1a0e, A0: 00fd1912 (EV_DISPSYS) 
OS9 syscall: m2dispsys+00042778  F$Link        D0: 0000, A0: 18c2 (DM_DISPSYS) 
(5)
OS9 syscall: m2dispsys+0004271e  F$Event       (Ev_Set) D0: 00020001, D1: 000a, D2: 0000, D3: 1a0e, A0: 00fd18c2 (DM_DISPSYS) 
OS9 syscall: m2dispsys+00042744  F$Event       (Ev_Wait) D0: 00020001, D1: 0004, D2: 0002, D3: 0002, A0: 00fd1970 
(6)
OS9 syscall: m2gsys+000eb7d0  F$Event       (Ev_Set) D0: 00020001, D1: 000a, D2: 0002, D3: bc50, A0: 00ef0dc2 
OS9 syscall: cio+0003498a  I$Close       D0: 0000 
OS9 syscall: scf+00030238  I$Detach      A2: 00ffe350 
OS9 syscall: cio+0003498a  I$Close       D0: 0001 
OS9 syscall: cio+0003498a  I$Close       D0: 0002 
OS9 syscall: m2gsys+000ebac6  F$Exit        D1: 00dd 
```

I fixed the OS-9 call tracing (events are now displayed with the relevant
register and their sizes), here's the new trace:

```
OS9 syscall: m2gsys+000eb72a  F$Event       (Ev_Link) A0: 00efe66e (CS_GS) 
OS9 syscall: m2gsys+000eb72a  F$Event       (Ev_Creat) D0: 000003e7, D2: ffff, D3: 0000 
OS9 syscall: m2gsys+000eb7d0  F$Event       (Ev_Set) D0: 00010000, D1: 000a, D2: 00000000 
(1)
OS9 syscall: m2gsys+000eb72a  F$Event       (Ev_Link) A0: 00efbb16 (EV_DISPSYS) 
(2)
OS9 syscall: m2gsys+000eb72a  F$Event       (Ev_Creat) D0: 000003e7, D2: ffff, D3: 0000 
OS9 syscall: m2gsys+000eb82a  F$Link        D0: 0000, A0: bac6 (DM_DISPSYS) 
OS9 syscall: m2gsys+000eb650  F$DatMod      D0: 00000400, D1: 8000, D2: 0003, D3: bc50, A0: bac6 (DM_DISPSYS) 
OS9 syscall: m2gsys+000eba3e  F$ID           
(3)
OS9 syscall: m2gsys+000eb7f6  F$Event       (Ev_Wait) D0: 00020001, D2: 00000000, D3: 00000000 
OS9 syscall: m2dispsys+00042510  F$Sleep       D0: 8000000a 
(4)
OS9 syscall: m2dispsys+00042678  F$Event       (Ev_Link) A0: 00fd1912 (EV_DISPSYS) 
OS9 syscall: m2dispsys+00042778  F$Link        D0: 0000, A0: 18c2 (DM_DISPSYS) 
(5)
OS9 syscall: m2dispsys+0004271e  F$Event       (Ev_Set) D0: 00020001, D1: 000a, D2: 00000000 
OS9 syscall: m2dispsys+00042744  F$Event       (Ev_Wait) D0: 00020001, D2: 00000002, D3: 00000002 
(6)
OS9 syscall: m2gsys+000eb7d0  F$Event       (Ev_Set) D0: 00020001, D1: 000a, D2: 00000002 
OS9 syscall: cio+0003498a  I$Close       D0: 0000 
OS9 syscall: scf+00030238  I$Detach      A2: 00ffe350 
OS9 syscall: cio+0003498a  I$Close       D0: 0001 
OS9 syscall: cio+0003498a  I$Close       D0: 0002 
OS9 syscall: m2gsys+000ebac6  F$Exit        D1: 00dd 
```

There is some IPC going on. It looks like m2gsys wants to start m2dispsys and
wait for it to be ready. To do so, it creates an event called `EV_DISPSYS` with
initial value -1 (1), then loads the executable (2) (note: it asks for
`DM_DISPSYS` but the actual executable is called `m2dispsys`?), then waits for
the event to become 0 (3). m2dispsys starts, sleeps a bit, then links to the
same event (4), sets it to 0 (5) and waits. Now that `EV_DISPSYS` is 0, m2gsys
wakes up and attempts to set it to 2 (6), but OS-9 returns with an error.

This might call for an in-kernel debugging, of which we have no sources.

I also noted that the system acually fails in two different modes - which one
happens, it's random. The error number may be a hint: it may be 221 or 168. In
the crashes above, the number was 221. Maybe they have the same root cause and
the 168 failure is easier to troubleshoot?




[Dockerfile](https://gist.github.com/biappi/a7538e38bbdd7f1ea7d33c54112aa22f)
