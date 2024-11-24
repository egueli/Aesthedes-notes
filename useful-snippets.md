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

