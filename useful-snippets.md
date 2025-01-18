# Useful snippets


## Text Encoding

The OS9 version used in the Aestedes seems to use old Macitosh line ending
encodings.

To make vim reinterpret the buffer after opening:

    :e ++ff=mac


## MAME emulator conveniences

In the root of the `os9-builder` repo, there is a `Makefile` with some PHONY
targets intended to be shortcuts for quick building iterations. They assume the
submodules are correctly checked out (possibly with a depth of one) and
`Makefile.conf` is properly configured.

Currently the following "scripts" are available, and can be run in any order.
    
    - `make romimage` -- will compile the CB030 romimage and copy the rom to
      the MAME rom directory.
    - `make make-cfcard` -- will create a zeroed raw image for the mame CF
      emulation
    - `make mame` -- will compile a `fake86` mame emulator with a single
      machine
    - `make run` -- will start a windowed mame emulator with the debugger and
      the card inserted.


## Bitbanged serial terminal

Since the terminal emulator in MAME is pretty basic, doesn't support scrollback
nor copy/paste, it could be convenient to use the regular terminal. This is
possible using the bigbanged serial implementation of mame, that allows to
connect an emulated RS232 to an TCP socket.

To get the full details refer to the `Makefile`, but it should be sufficient to
do, in a terminal
    - `make listen-term` -- will open and continuosly listen to a port, and redirect it
    to stdin/out: i haven't investigated much the the translation between the os9
    console and modern unix terminals, but the `stty` command in the pipe is an hint on
    where to configure translations between terminal escape codes and the likes
    - `make run-term` -- will open mame with the console rs232 redirected to the open
    port that `listen-term` listens to.

I don't remember if i had to use the MAME on-screen UI (that continues to
appear with the debugger and the second terminal) to configure the emulated
baud rate of the bitbanged interface, or the `listen-term` will appear like a
real baud mismatch.

Also, sometimes MAME gets confused with the keyboard assignments between the
two terminals... if the keyboard does not work, it's possible to change in
which of the two terminals (or both) the keystrokes go, in the Input Settings
section of the "Tab" menu.


## Easily extract an entire OS9 image

I didn't immediately find how to unpack a raw os9 RBF filesystem image using
toolshed.

Turns out the best way is using the `dsave` command in this way -- note the
comma after the filename is for toolshed to "get into" the image and not copy
the image file itself:

    willy@Hitagi os9-toolshed main$ ./build/unix/os9/os9 dsave ~/Downloads/quanterra.iso, /tmp/qt

This command will not actually copy files, but output to stdout a sequence of
copy commands to extract the image. By default it will simply dry-run and offer
a chance to check what files will go where.

To actually do the copy, add the `-e` parameter, but this will require having
the `os9` toolshed executable in the current `$PATH`, because `dsave` will
simply do a `system` to invoke the `copy` command.


## LUA mame

Getting an handle on the memory space

    mem = manager.machine.devices[":maincpu"].spaces['program']

Printing the content of a memory address

    print(string.format("%x", mem:read_u32(0)))

Useful addresses

    sys_glob = mem:read_u32(0)
    module_dir_start = mem:read_u32(sys_glob + 0x3c)
    module_dir_end = mem:read_u32(sys_glob + 0x40)

It is possible to continuously import a file in the lua REPL like so:

    loadfile('../file.lua')()

A breakpoint command (not lua) to break on OS9 syscalls

    bpset 52c,1,{ print w@(d@(a7 + 2)) }

## Intercept OS-9 system calls

1. Run MAME with `-console -debug`.
2. In the console used to run it, type

    loadfile('../mame-os9.lua')()

3. In the debugging console, type `go`.
4. Start the OS and/or the program to debug.
5. In the console, type

    trace_syscalls()

(note: it will slow down execution quite a bit)
6. You will see OS-9 system call details in the other console.

## OS-9 debugging tools

This returns the address of PC, adjusted for Ghidra i.e. it can be searched with
Ghidra's `G` shortcut:

    pc_ghidra()

This adds a breakpoint on a OS-9 process (`fcontrol` in this case), given its
Ghidra-adjusted address:

    os9_break('fcontrol', 0x30052)

Note that the process must be already loaded in memory.

## Debugging session

1. start MAME:

```sh
make run-term
```

2. start debugger with `g`
3. type init commands in serial terminal; type the last command but DO NOT press
enter:
```
chd /r0
chx /r0/CMDS
main
```
3. enable debugging:

```lua
loadfile('../mame-os9.lua')()
trace_syscalls()
import_comments_from_ghidra('fcontrol', '/tmp/fcontrol-uilli.txt')

-- break fcontrol just before load_configuration
os9_break('fcontrol', 0x302e0)

-- break main just before loading AE_CONFIG
os9_break('main', 0x3043a)

-- break fcontrol just before it kernel-hangs
os9_break('fcontrol', 0x3b1e4)
```
4. press enter on serial terminal.

## Trace loop iterations

Example:

Breakpoint inside an iteration block, assuming `i` is at D0, and the limit in
the stack at offset 0xa0:
```
bpset eb87c0,1,{ printf "i=%d limit=%d", d@(a7+0xa0), d0 }
```

## Monitor serial transmit buffer count

Note: to paste text onto the debugger window, right-click on the text-box then
"Paste". If you see nothing, hit Backspace once and the text should appear.

```
bpset 13d60,1,{ printf "port@%06x count=%d", a2, w@(a2 + 72); g }
```

Break:
```
bpset 13d60, sr&1, { printf "port@%06x count=%d", a2, w@(a2 + 72) }
```

Dump some variables of `sc68681` driver when transmitting a character (in D0),
just before deciding if send immediately or queue it:

```
bpset 13d60,1,{ printf "port@%06x D0.b=%02x BaseAddr=%08x OutCount=%3d ChanelNo=%02x BaudRate=%02x Parity=%02x InHalt=%02x OutHalt=%02x Otpt_On=%02x Otpt_Off=%02x RTSmode=%02x RTSstate=%02x TXmode=%02x", a2, d0, d@(a2+0x56+0x18), w@(a2+0x56+0x1c), b@(a2+0x56+0x2a), b@(a2+0x56+0x2b), b@(a2+0x56+0x2c), b@(a2+0x56+0x2d), b@(a2+0x56+0x2e), b@(a2+0x56+0x2f), b@(a2+0x56+0x30), b@(a2+0x56+0x31), b@(a2+0x56+0x32), b@(a2+0x56+0x33); g }
```

For the full list of variables, edit `scf_68681.make` and add `-s` to `RFLAGS`,
this enables listing generation. In the generated `scf_sc68681.lst` look for
definitions in `vsect` and add those offsets to `a2+0x56`.

