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

May need some OS-9 tracking to see which process it is, then use Ghidra to disasemble it, map it to the right memory location, then see what code does these accesses.
