A process in CPU 504 configures port A as input:

```
0027.763,649,729 [:crate5:17:aesthedes2_io] ':crate5:04:pme6822:maincpu' (086F074E) reg WRITE @02 data=00
0027.763,649,729 [:crate5:17:aesthedes2_io:pia_a] PIA control A write = 00
0027.763,649,729 [:crate5:17:aesthedes2_io:pia_a]  - CA1 interrupts disabled
0027.763,649,729 [:crate5:17:aesthedes2_io:pia_a]  - CA1 interrupts active on high-to-low transition
0027.763,649,729 [:crate5:17:aesthedes2_io:pia_a]  - Port A DDR register selected
0027.763,651,169 [:crate5:17:aesthedes2_io] ':crate5:04:pme6822:maincpu' (086F075A) reg WRITE @00 data=00
0027.763,651,169 [:crate5:17:aesthedes2_io:pia_a] PIA DDR A write = 00 (input mode)
0027.763,652,609 [:crate5:17:aesthedes2_io] ':crate5:04:pme6822:maincpu' (086F0768) reg WRITE @02 data=2c
0027.763,652,609 [:crate5:17:aesthedes2_io:pia_a] PIA control A write = 2C
0027.763,652,609 [:crate5:17:aesthedes2_io:pia_a]  - CA1 interrupts disabled
0027.763,652,609 [:crate5:17:aesthedes2_io:pia_a]  - CA1 interrupts active on high-to-low transition
0027.763,652,609 [:crate5:17:aesthedes2_io:pia_a]  - Port A Data register selected
0027.763,652,609 [:crate5:17:aesthedes2_io:pia_a]  - CA2 strobe output mode
```

Then, it polls the port A status register:

```
0033.552,165,026 [:crate5:17:aesthedes2_io] ':crate5:04:pme6822:maincpu' (086F0A06) reg READ  @02 data=2c
0033.552,168,266 [:crate5:17:aesthedes2_io] ':crate5:04:pme6822:maincpu' (086F0A06) reg READ  @02 data=2c
0033.552,171,505 [:crate5:17:aesthedes2_io] ':crate5:04:pme6822:maincpu' (086F0A06) reg READ  @02 data=2c
...
```

Looks like it expects some incoming data on port A, strobed on CA1. That's offset 0x000ba446 in `fcontrol` process.

By stepping through instructions, it looks like it expects a sequence of 6 bytes, all with MSB set. There is a timeout wait of 6.48ms (assuming a 16 MHz CPU) between two bytes; if a timeout occurs, the function returns early.

Once the 6 bytes are received, the first byte is ANDed with $7C then divided by 4 (so, 5 bits) then stored to A7+$26.

The lower 2 bits are shifted left by 14 bits, then added to the second byte after being shifted left by 7 bits (overwriting the least significant of the original 2 bits?) then added to the third byte.

```
00000000 11111111 22222222 33333333 44444444 55555555
.6543210 76543210 76543210 ......10 76543210 76543210
 |---||- -------- -------|       |- -------- -------|
 (A7+26)       (A7+2A)                 (A7+3A)   

(A7+26) = $8089912
(A7+2A) = $80899CC
(A7+3A) = $80899C8
```

Those look like X-Y coordinates combined with info like buttons pressed.

Is that a mouse? No, it's the bitpad (aka digitizer)!!