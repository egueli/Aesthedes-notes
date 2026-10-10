# Multilevel Screen Protocol

This document tries to explain how the PME 68-22 @ 504 (via the I/O card @ 516) and 68K @ 616 (controlling the multilevel i.e. central monitor) talk together.

The basic unit of communication is a transaction. Each transaction is made of three moments:

1. latch (sender sets data to output port B)
2. strobe (sender asserts CB2, receiver gets it on CA1 respectively)
3. acknowledge (receiver sets 0xFF on port A, asserts CA2)

Commands are sent primarily on port B. Some commands also send an additional byte on port A on the same transaction.


## Command 0x03: Set layer color

PB 03, (layer-num), (red), (green), (blue)

Ack: PB FF, FF, FF, FF

At startup, this command is sent for all 64 layers to initialize them as black.

## Command 0x0A: ?

PB 0A + PA FF, 00

Ack: PB FF, FF

This is the last command during startup.

## Command 0x55: Test connection

PB 55 + PA FF

Ack: PB FF + PA 55

