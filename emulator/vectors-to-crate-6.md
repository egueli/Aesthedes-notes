When loading `ebt`, m2dispsys traverses $87D94A0 when it sends the command to the right monitor's EF9365 to draw a line.

A similar command should have been sent to the center (multilevel) monitor as well, i.e. to the 68K. This should be done by sending bytes via card 516, but there is no traffic.

My theory is that m2dispsys draws each shape twice, once to the 9365, once to the 68K. And it does so before proceeding to the next shape.

Let's see what does m2dispsys do when drawing a shape. My theory is that at some point it skips drawing to the 68K for some reason.

Going to trace execution:

```
trace draw_vector.log,,logerror|noloop,{tracelog "PC=%08X SR=%04X SP=%08X D0=%08X D1=%08X D2=%08X D3=%08X D4=%08X D5=%08X D6=%08X D7=%08X A0=%08X A1=%08X A2=%08X A3=%08X A4=%08X A5=%08X A6=%08X\n",pc,sr,a7,d0,d1,d2,d3,d4,d5,d6,d7,a0,a1,a2,a3,a4,a5,a6}
```

We got an almost 370K line file, mostly with alternating logs and CPU instructions, and some logs in between.

Looks like 21269 instructions are executed in 6.7 ms to draw a full shape outline (one square):

```
 86448  0048.035,269,120 [:crate5:08:aesthedes2_gpu:ef9365] ':crate5:04:pme6822:maincpu' (087D94A0): EF9365 draw_vector : Start=(191,257) End=(133,257)
 86659  0048.035,304,240 [:crate5:08:aesthedes2_gpu:ef9365] ':crate5:04:pme6822:maincpu' (087D94A0): EF9365 draw_vector : Start=(133,257) End=(133,316)
 86874  0048.035,339,960 [:crate5:08:aesthedes2_gpu:ef9365] ':crate5:04:pme6822:maincpu' (087D94A0): EF9365 draw_vector : Start=(133,316) End=(191,316)
 87089  0048.035,375,040 [:crate5:08:aesthedes2_gpu:ef9365] ':crate5:04:pme6822:maincpu' (087D94A0): EF9365 draw_vector : Start=(191,316) End=(191,257)
128987  0048.041,990,360 [:crate5:08:aesthedes2_gpu:ef9365] ':crate5:04:pme6822:maincpu' (087D94A0): EF9365 draw_vector : Start=(254,257) End=(195,257)
129202  0048.042,026,080 [:crate5:08:aesthedes2_gpu:ef9365] ':crate5:04:pme6822:maincpu' (087D94A0): EF9365 draw_vector : Start=(195,257) End=(195,316)
129417  0048.042,061,800 [:crate5:08:aesthedes2_gpu:ef9365] ':crate5:04:pme6822:maincpu' (087D94A0): EF9365 draw_vector : Start=(195,316) End=(254,316)
129636  0048.042,097,480 [:crate5:08:aesthedes2_gpu:ef9365] ':crate5:04:pme6822:maincpu' (087D94A0): EF9365 draw_vector : Start=(254,316) End=(254,257)
```

Of which, 20949 between the end of the last segment and the next shape's first segment.

Somwehere in these instructions the CPU figures out what to draw next, the list of segments, and whether to drive the multilevel monitor or not.

-----

Among the functions that are called during this trace, one receives opcodes from `fcontrol` and calls many other functions depending on the opcode. At least one of those functions talks to the 68K. Therefore, it might be that `fcontrol` itself decides what to draw to each monitor. Let's use some breakpoints to inspect the traffic between the two processes.

This is the [protocol](fcontrol_m2dispsys.md) as found by the stochastic parrot.

The following MAME debugger commands must be entered for `:crate5:04:pme6822:maincpu` (press F6 to switch CPU) after the app is loaded, before entering the load command:

```
print d@0802caf0
(should print 8708140; if not, change the occurrence below)

bpset 0x086f6988,1,{ printf "F$Event Ev$Set id=%08X value=%08X payload: %04X/%04X argc=%d %04X %08X %08X %08X %08X %08X %08X",d0,d2,w@8708140,w@8708142,w@8708144,w@87081446,d@8708148,d@870814C,d@8708150,d@8708154,d@8708158,d@870815C ; g }
```

These are sent at startup, before loading the drawing:

```
F$Event Ev$Set id=00020001 value=00000002 payload: 0007/0362 argc=0 0000 000100FD 00010000 00000000 0001003F 00010001 00010001
F$Event Ev$Set id=00020001 value=00000000 payload: 0007/0065 argc=0 0000 000100FD 00010000 00000000 0001003F 00010001 00010001
F$Event Ev$Set id=00010000 value=00000002 payload: 0007/0065 argc=0 0000 000100FD 00010000 00000000 0001003F 00010001 00010001
F$Event Ev$Set id=00010000 value=00000000 payload: 0006/0065 argc=0 0000 0001001F 00010000 00000000 0001003F 00010001 00010001
F$Event Ev$Set id=00010000 value=00000002 payload: 0006/0065 argc=0 0000 0001001F 00010000 00000000 0001003F 00010001 00010001
F$Event Ev$Set id=00010000 value=00000000 payload: 0006/0065 argc=0 0000 00020000 00000002 00000000 0001003F 00010001 00010001
```

At loading:

```
F$Event Ev$Set id=00020001 value=00000002 payload: 0007/0321 argc=4 0000 00010000 00010000 00010000 00010000 00010001 00010001
F$Event Ev$Set id=00020001 value=00000000 payload: 0007/0065 argc=0 0000 00010000 00010000 00010000 00010000 00010001 00010001
F$Event Ev$Set id=00020001 value=00000002 payload: 0007/0321 argc=4 0000 00010001 000100FF 000100FF 000100FF 00010001 00010001
F$Event Ev$Set id=00020001 value=00000000 payload: 0007/0065 argc=0 0000 00010001 000100FF 000100FF 000100FF 00010001 00010001
F$Event Ev$Set id=00020001 value=00000002 payload: 0007/0321 argc=4 0000 00010002 00010005 00010005 00010005 00010001 00010001
F$Event Ev$Set id=00020001 value=00000000 payload: 0007/0065 argc=0 0000 00010002 00010005 00010005 00010005 00010001 00010001
...
F$Event Ev$Set id=00020001 value=00000002 payload: 0007/0321 argc=4 0000 0001003F 000100FF 000100FF 000100FF 00010001 00010001
F$Event Ev$Set id=00020001 value=00000000 payload: 0007/0065 argc=0 0000 0001003F 000100FF 000100FF 000100FF 00010001 00010001
```

The only opcodes seen are the one to set the level colors (0007/0321, see protocol doc), and 0007/0065 with no arguments. No trace of vectors or shapes. Which is surprising, because `m2dispys` drives the EF9365 with shapes and those must come from somewhere. A separate communication channel maybe?

Or maybe the shared data area is used in different ways than with events? Let's add a watchpoint on any writes:

```
wpset 8708140:crate5:04:pme6822:maincpu,4,w
```

The first write by userspace is by 087C46F0, which Ghidra doesn't recognize as neither `fcontrol` nor `m2dispsys`?

Going to find out which module it is. I search for the OS-9 header in the vicinity:
```
find 8600000:crate5:04:pme6822:maincpu,1C46F0,w.4afc,w.0001
```
Closest match is at 870A710. From the memory view, a string pops up: `m2gsys`. Maybe that's the module that actually handles the graphic vectors, while `m2dispsys` is the low-level interface to the displays?

Later we'll try loading `m2gsys` into Ghidra and analyzing it; but first, let's which other writes are done and let's match them with the Ev$Sets done by `fcontrol` (especially, see which ones _don't_ match):

```
wpset 8708140:crate5:04:pme6822:maincpu,20,w,1,{ printf "write @ %08X: %04X (PC=%08X)",wpaddr,wpdata,PC ; g }
bpset 86f6988:crate5:04:pme6822:maincpu,1,{ printf "F$Event Ev$Set id=%08X value=%08X",d0,d2 ; g }
```

We do see writes to the data area without a related F$Event; those may be issued by `m2gsys`. Most interestingly, we see the EF9365 being driven just after those writes. Is it possible that `m2gsys` is only sending draw commands for the side display and not for the multilevel? And how to let it send those commands? A disassembly is in order.

