The bootloader (`boortom`) is trying to read the CF regs, then complains with the error `CF: not a supported drive type`.

Such string is defined at `os9-m68k-ports/ports/CB030/ROM_CBOOT/io_cf.c` line 150. And it's located in the binary (`romimage.dev`) at offset 0xbb6. Let's find out which part of the bootloader code reads that string at 0xfe000bb6 in the system memory.

Although it's possible to set a tracepoint in MAME and stop there, we'd actually end up in the middle of the `outstr` function that is common across all printing functions in the bootloader. Walking up the stack trace to see which function invoked it, is no easy feat.

Instead, let's figure out what is the address of the function that prints that string, i.e. `cf_iniz`. With that, we can set a breakpoint in MAME and see exactly where things go wrong. One way to do this is to obtain the linkage map i.e. the start addresses of all C functions. It can be found at `os9-builder/os9-m68k-ports/ports/CB030/CMDS/BOOTOBJS/NOBUG/romboot.map`.

Alas, `cf_iniz` is missing because it is file-static and the linker doesn't know anything about it. Let's fix this by removing the `static` keyword and rebuilding the ROM image. After the change, we can see that it was located at address `fe000c16`.
