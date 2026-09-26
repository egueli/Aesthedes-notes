After loading `ebt` and loaded all the layers' colors, the system hangs.

The logs show that an unidentified OS-9 process does some seemengly random reads and writes, then starts scanning the entire memory:

```
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DD37E): unmapped program memory read from 0003FFFC & FFFFFFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DD380): unmapped program memory write to 00000000 = FFFFFFFF & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DD390): unmapped program memory read from 0003FFFC & FFFFFFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DB9FC): unmapped program memory write to 00000000 = 00000000 & 0000FF00
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA04): unmapped program memory write to 00000008 = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA04): unmapped program memory write to 0000000C = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA0A): unmapped program memory write to 00000004 = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA0A): unmapped program memory write to 00000008 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA10): unmapped program memory write to 00000004 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA16): unmapped program memory write to 0000001C = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA16): unmapped program memory write to 00000020 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA1C): unmapped program memory write to 00000020 = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA1C): unmapped program memory write to 00000024 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA22): unmapped program memory write to 00000024 = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA22): unmapped program memory write to 00000028 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA28): unmapped program memory write to 00000028 = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA28): unmapped program memory write to 0000002C = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DD3C8): unmapped program memory read from 0003FFFC & FFFFFFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5A7A): unmapped program memory write to 00000004 = DA58DA58 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5A7A): unmapped program memory write to 00000008 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5A88): unmapped program memory write to 00000008 = DA58DA58 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5A88): unmapped program memory write to 0000000C = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5A96): unmapped program memory write to 00000004 = 00010001 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5AAE): unmapped program memory write to 00000000 = 18181818 & 0000FF00
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5AD4): unmapped program memory write to 00000000 = 14141414 & 0000FF00
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B08): unmapped program memory write to 00000000 = 10101010 & 0000FF00
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E8C86): unmapped program memory read from 004607FC & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E8C86): unmapped program memory read from 00460800 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E8C94): unmapped program memory read from 004607FC & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E8C94): unmapped program memory read from 00460800 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9328): unmapped program memory write to 00460800 = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9328): unmapped program memory write to 00460804 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E8C86): unmapped program memory read from 005007FC & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E8C86): unmapped program memory read from 00500800 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E8C94): unmapped program memory read from 005007FC & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E8C94): unmapped program memory read from 00500800 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E92B4): unmapped program memory read from 00460800 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E92B4): unmapped program memory read from 00460804 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E92D2): unmapped program memory read from 004607FC & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E92D2): unmapped program memory read from 00460800 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E930C): unmapped program memory write to 00500800 = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E930C): unmapped program memory write to 00500804 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9316): unmapped program memory write to 00460800 = 00500050 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9316): unmapped program memory write to 00460804 = 07FE07FE & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBB1C): unmapped program memory write to 0000001C = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBB1C): unmapped program memory write to 00000020 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBB22): unmapped program memory write to 00000020 = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBB22): unmapped program memory write to 00000024 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBB28): unmapped program memory write to 00000024 = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBB28): unmapped program memory write to 00000028 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBB2E): unmapped program memory write to 00000028 = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBB2E): unmapped program memory write to 0000002C = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA66): unmapped program memory write to 00000020 = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA66): unmapped program memory write to 00000024 = 00060006 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9076): unmapped program memory read from 004607FC & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9076): unmapped program memory read from 00460800 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9088): unmapped program memory read from 00460800 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9088): unmapped program memory read from 00460804 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E92B4): unmapped program memory read from 00460800 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E92B4): unmapped program memory read from 00460804 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E92D2): unmapped program memory read from 004607FC & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E92D2): unmapped program memory read from 00460800 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9316): unmapped program memory write to 00460800 = 085A085A & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9316): unmapped program memory write to 00460804 = 34583458 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA82): unmapped program memory write to 00000024 = 085A085A & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBA82): unmapped program memory write to 00000028 = 34243424 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9076): unmapped program memory read from 004607FC & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9076): unmapped program memory read from 00460800 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9088): unmapped program memory read from 00460800 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9088): unmapped program memory read from 00460804 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E92B4): unmapped program memory read from 00460800 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E92B4): unmapped program memory read from 00460804 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E92D2): unmapped program memory read from 004607FC & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E92D2): unmapped program memory read from 00460800 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9316): unmapped program memory write to 00460800 = 08560856 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E9316): unmapped program memory write to 00460804 = 34303430 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBAAC): unmapped program memory write to 00000028 = 08560856 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DBAAC): unmapped program memory write to 0000002C = 34243424 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B2A): unmapped program memory write to 0000001C = 00000000 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B2A): unmapped program memory write to 00000020 = 00040004 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B56): unmapped program memory write to 00500800 = 01010101 & 0000FF00
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B68): unmapped program memory write to 00460800 = E059E059 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B68): unmapped program memory write to 00460804 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B7A): unmapped program memory write to 00460804 = 2F472F47 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B7A): unmapped program memory write to 00460808 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B56): unmapped program memory write to 00500800 = 01010101 & 000000FF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B68): unmapped program memory write to 00460808 = D1A9D1A9 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B68): unmapped program memory write to 0046080C = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B7A): unmapped program memory write to 0046080C = 2F472F47 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B7A): unmapped program memory write to 00460810 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B56): unmapped program memory write to 00500804 = 01010101 & FF000000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B68): unmapped program memory write to 00460810 = D1A9D1A9 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B68): unmapped program memory write to 00460814 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B7A): unmapped program memory write to 00460814 = 3DF73DF7 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B7A): unmapped program memory write to 00460818 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B56): unmapped program memory write to 00500804 = 01010101 & 00FF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B68): unmapped program memory write to 00460818 = E059E059 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B68): unmapped program memory write to 0046081C = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B7A): unmapped program memory write to 0046081C = 3DF73DF7 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087E5B7A): unmapped program memory write to 00460820 = 00000000 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DC9BE): unmapped program memory read from 00460800 & 0000FFFF
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DC9BE): unmapped program memory read from 00460804 & FFFF0000
[:crate5:04:pme6822:maincpu] ':crate5:04:pme6822:maincpu' (087DC9CE): unmapped program memory read from 00460804 & 0000FFFF
...
```

May need some OS-9 tracking to see which process it is, then use Ghidra to disasemble it, map it to the right memory location, then see which code does these accesses.

Instead of tracking OS-9, a simpler method is to have a breakpoint where the process is known to run, then open a Memory View in MAME pointing at that same address, then scroll up manually until some 4AFC0001 magic number is found. The process name should be a few bytes later.

In this case the base offset is $87D7DF0, the size is $13574 and the process name is `m2dispsys`. 

Saving the module from MAME to disk:
```
save m2dispsys@504@load-ebt.bin,87D7DF0,13574
```

The (static) data area starts at the value of A6 (minus $8000) and is $26AC bytes large, so to save it to disk:
```
save m2dispsys@504@load-ebt.data.bin,A6-8000,26AC
```

We also need to know the actual data area start address:
```
print A6-8000
802A7D0
```

Now we can load them both in Ghidra.

So, it seems there's an indirect access `clr.b (A0,2)` with A0 likely being 0. Going back to the caller at $087DB9FC to see where this zero comes from.

It looks like $802C412 is supposed to contain a pointer to an array, but it is zero instead.

Let's see which instruction writes to it last:

```
wpset 802c412,4,w
bpset 87db9fc
```

Only the OS writes zero there, to clear the memory at startup, then no one else does. According to Ghidra's cross references, it should have been written by either $87DD238 or $87DD9CE, but none are executed.

1. $87DD238 is part of $87DD1F0 that has 3 callers.
2. $87DD9CE is part of $87DD96E that has one caller, $87E59F8.

Let's start with caller 2 since it has just one caller.

* $87E59F8 is part of $87E59E6 that has one caller, $87D81C6.
    * $87D81C6 is part of $87D8198, a function with a huge jump table. Input command parser perhaps?

During system startup, that jump table is queried for opcodes $67, $259, $362, $259 again, $251.

When loading `ebt`, we see opcodes $321 (64 times, just like the number of layers...) and $C9.

But, our function would be called for opcode $6A, which is not requested. Maybe that happens for a specific command. So, let's explore caller 1 instead:

* $87DD18A that is part of $87DD090
    * called by $87D80D4 that is part of $87D8062
        * called by $87D7F22 in m2dispsys's main function, $87D7E42
* $87DD33E that is part of $87DD2F4
    * called by $87E5A5A that is part of $87E5A4A
        * called by $87D81DA that is part of $87D8198, the big jump table
            * called by $87D815C that is part of $87D8062
                * called by $87D7F22 in m2dispsys's main function (*)
    * (other functions that have the same graph as above)
* $87DDA38 that is part of $87DD96E
    * called by $87E59F8 that is part of $87E59E6
        * called by $87D81C6 that is part of $87D8198 (*)

So why isn't the main function calling $87DD238? To see when the chain stops, let's add breakpoints:
```
bpset 87D7E42; bpset 87D7F22; bpset 87D8062; bpset 87D80D4; bpset 87DD090; bpset 87DD18A; bpset 87D81DA; bpset 87E5A4A; bpset 87E5A5A; bpset 87DD2F4; bpset 87DD33E; bpset 87D81C6; bpset 87E59E6; bpset 87E59F8; bpset 87DD96E; bpset 87DDA38
```

Looks like $87D8062 does not hit $87D80D4; let's see why. A branch instruction at $87D80B2 prevents that address to be hit. That's due to a call to $87E02DE (at $87D80AA) that should return zero (via D0) but it didn't.

That function checks the return value of two other functions ($87D8C12 and $87D9D9A) and the value of two global variables ($802C220 and $802C224).

Both those functions do reads/writes to $4FCB001 (at $87D8C50) and $4FCB101 respectively. The logs with VME enabled confirm this. They might be the two side GPUs, that are currently not emulated at all.

I added a very simple emulation, that returns $FF at every read, and now it seems to load `ebt` completely! At least, we see "waiting" in the central B/W screen.

