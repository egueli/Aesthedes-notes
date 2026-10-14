# Multilevel Graphics bus registers

This document describes how the 68K CPU card at slot 616 controls the other cards (611, 613, 617, 618, 619) in the same G-64 bus. For details, see the [CPU card description](cards/aes_68k/README.md).

Here we treat the multilevel graphics as a whole, without going into a specific card unless otherwise specified.

## Addressing

The system is an 8-bit peripheral in a 16-bit-wide bus; accesses are done at odd addresses.

Only the higher 8 bits of the address are effectively used; this means that we can discard the lower byte, being constantly 0x01. for example, an access via the 16-bit bus at 0xB201 may be considered as an access to the 8-bit register 0xB2. The rest of this document will simply refer as "registers" unless otherwise specified.

## Levels

The level-related registers are at 0xB0 to 0xB3.

The following example is about setting the green channel of level 49 to 240:

```
reg WRITE @b1 data=31
reg WRITE @b0 data=05
reg WRITE @b3 data=f0
reg WRITE @b0 data=15
```

In order:

1. set level number to 0x31 -> 49.
2. begin write to green channel (0x1 | 0x4)
3. set data register to 0xf0 -> 240.
4. end write to green channel (0x1 | 0x4 | 0x10)

### Command register

0xB0 is command/status register. It may have written to do the following commands:

* 0x01: begin write to red channel
* 0x05: begin write to green channel
* 0x09: begin write to blue channel
* 0x11: end write to red channel
* 0x15: end write to green channel
* 0x19: end write to blue channel

The "end" commands should be invoked after applying the respective color and the level number.

It can be read to wait for the command to be executed. When ready, it reads 0x00.

### Level select register

0xB1 is the level selection register. It is written with a value between 0 and 63.

### Data register

0xB3 is written between "begin write" and "end write" with the color value for the desired channel and level.