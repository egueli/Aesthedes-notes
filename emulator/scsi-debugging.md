
SCSILIB

module starts at 80198f8, ends at 801af20.

interrupt handler:
starts at 801a334, ends at 801a362.

        A2  087FDB2C (a2) = global static pointer
        A3  00020000 (a3) = port address
        A6  08021000 (a6) = system global data pointer (D_’s)
        A7  08020FF0 (a7) = system stack (in active proc’s descriptor)



```
[:crate5:04:pme6822:scsi:7:ncr5385] dat_w 0xaa (':crate5:04:pme6822:maincpu' (0801A388))
[:crate5:04:pme6822:scsi:7:ncr5385] update_int 1
[:crate5:04:pme6822:scsi:7:ncr5385] int_status_r 0x01 (':crate5:04:pme6822:maincpu' (0801A33A))
[:crate5:04:pme6822:scsi:7:ncr5385] update_int 0
[:crate5:04:pme6822:scsi:7:ncr5385] aux_status_r 0x82 (':crate5:04:pme6822:maincpu' (0801A340))
[:crate5:04:pme6822:scsi:7:ncr5385] dat_w 0x00 (':crate5:04:pme6822:maincpu' (0801A3AA))
[:crate5:04:pme6822:scsi:7:ncr5385] data register full
[:crate5:04:pme6822:scsi:7:ncr5385] cmd_w 0x0b (':crate5:04:pme6822:maincpu' (0801A384))
[:crate5:04:pme6822:scsi:7:ncr5385] diagnostic (good parity)
[:crate5:04:pme6822:scsi:7:ncr5385] dat_w 0x55 (':crate5:04:pme6822:maincpu' (0801A388))
[:crate5:04:pme6822:scsi:7:ncr5385] update_int 1
[:crate5:04:pme6822:scsi:7:ncr5385] int_status_r 0x01 (':crate5:04:pme6822:maincpu' (0801A33A))
[:crate5:04:pme6822:scsi:7:ncr5385] update_int 0
[:crate5:04:pme6822:scsi:7:ncr5385] aux_status_r 0x82 (':crate5:04:pme6822:maincpu' (0801A340))
[:crate5:04:pme6822:scsi:7:ncr5385] dat_w 0x00 (':crate5:04:pme6822:maincpu' (0801A3AA))
[:crate5:04:pme6822:scsi:7:ncr5385] data register full
[:crate5:04:pme6822:scsi:7:ncr5385] ctl_w 0x00 (':crate5:04:pme6822:maincpu' (0801A46E))
[:crate5:04:pme6822:scsi:7:ncr5385] ctl_w 0x04 (':crate5:04:pme6822:maincpu' (0801A474))
[:crate5:04:pme6822:scsi:7:ncr5385] ctl_w 0x0c (':crate5:04:pme6822:maincpu' (0801A47A))
[:crate5:04:pme6822:scsi:7:ncr5385] dst_id_w 0x02 (':crate5:04:pme6822:maincpu' (0801A484))
[:crate5:04:pme6822:scsi:7:ncr5385] cmd_w 0x08 (':crate5:04:pme6822:maincpu' (0801A4BE))
[:crate5:04:pme6822:scsi:7:ncr5385] select 2 w/atn (timeout 0000.199,987,200)
[:crate5:04:pme6822:scsi:7:ncr5385] arbitration: waiting for bus free
[:crate5:04:pme6822:scsi:7:ncr5385] arbitration: started
[:crate5:04:pme6822:scsi:7:ncr5385] arbitration: won
[:crate5:04:pme6822:scsi:7:ncr5385] selection: SEL asserted
[:crate5:04:pme6822:scsi:7:ncr5385] selection: BSY cleared
[:crate5:04:pme6822:scsi:7:ncr5385] scsi_ctrl_changed 0x098 arbitration/selection
[:crate5:04:pme6822:scsi:7:ncr5385] selection: BSY asserted by target
[:crate5:04:pme6822:scsi:7:ncr5385] selection: complete
[:crate5:04:pme6822:scsi:7:ncr5385] update_int 1
[:crate5:04:pme6822:scsi:7:ncr5385] scsi_ctrl_changed 0x08e phase MESSAGE OUT
[:crate5:04:pme6822:scsi:7:ncr5385] scsi_ctrl_changed 0x0ae phase MESSAGE OUT REQ
[:crate5:04:pme6822:scsi:7:ncr5385] int_status_r 0x01 (':crate5:04:pme6822:maincpu' (0801A33A))
[:crate5:04:pme6822:scsi:7:ncr5385] update_int 0
[:crate5:04:pme6822:scsi:7:ncr5385] selection: REQ asserted by target
[:crate5:04:pme6822:scsi:7:ncr5385] update_int 1
[:crate5:04:pme6822:scsi:7:ncr5385] aux_status_r 0x32 (':crate5:04:pme6822:maincpu' (0801A340))
[:crate5:04:pme6822:scsi:7:ncr5385] int_status_r 0x02 (':crate5:04:pme6822:maincpu' (0801A348))
[:crate5:04:pme6822:scsi:7:ncr5385] update_int 0
[:crate5:04:pme6822:scsi:7:ncr5385] cmd_w 0x54 (':crate5:04:pme6822:maincpu' (0801A5EC))
[:crate5:04:pme6822:scsi:7:ncr5385] transfer info (pio, single byte)
[:crate5:04:pme6822:scsi:7:ncr5385] cmd_w 0x54 (':crate5:04:pme6822:maincpu' (0801A6FE))
[:crate5:04:pme6822:scsi:7:ncr5385] transfer info (pio, single byte)
[:crate5:04:pme6822:scsi:7:ncr5385] dat_w 0x80 (':crate5:04:pme6822:maincpu' (0801A712))
[:crate5:04:pme6822:scsi:7:ncr5385] xfi_out: data 0x80
[:crate5:04:pme6822:scsi:7:ncr5385] scsi_ctrl_changed 0x04e phase MESSAGE OUT ACK
[:crate5:04:pme6822:scsi:7:ncr5385] scsi_ctrl_changed 0x00a phase COMMAND
[:crate5:04:pme6822:scsi:7:ncr5385] scsi_ctrl_changed 0x02a phase COMMAND REQ
[:crate5:04:pme6822:scsi:7:ncr5385] xfi_out: transfer complete
[:crate5:04:pme6822:scsi:7:ncr5385] update_int 1
[:crate5:04:pme6822:scsi:7:ncr5385] int_status_r 0x02 (':crate5:04:pme6822:maincpu' (0801A718))
[:crate5:04:pme6822:scsi:7:ncr5385] update_int 0
```

Note that the addresses in Machine Log show PC at the instruction after the one that made the read/write.

I suspect a race condition, i.e. the SCSI controller triggers an interrupt before the driver is waiting for it.
The last register write happens at 0x0801a710, with totalcycles=1f9b85a. That triggers some SCSI transaction.



The driver seems to freeze when it tries to send a multi-byte transfer.
The driver writes 6 in the transfer counter registers, then 0x14 in the command register (Transfer Info).

```
[:crate5:04:pme6822] NCR5385: reg_w(b, 00) (':crate5:04:pme6822:maincpu' (0801A544))
[:crate5:04:pme6822] NCR5385: reg_w(c, 00) (':crate5:04:pme6822:maincpu' (0801A544))
[:crate5:04:pme6822] NCR5385: reg_w(d, 00) (':crate5:04:pme6822:maincpu' (0801A544))
[:crate5:04:pme6822] NCR5385: reg_w(e, 06) (':crate5:04:pme6822:maincpu' (0801A544))
[:crate5:04:pme6822] NCR5385: reg_w(1, 14) (':crate5:04:pme6822:maincpu' (0801A70C))
[:crate5:04:pme6822:scsi:7:ncr5385] cmd_w 0x14 (':crate5:04:pme6822:maincpu' (0801A70C))
[:crate5:04:pme6822:scsi:7:ncr5385] transfer info (pio, count=6)
[:crate5:04:pme6822:scsi:7:ncr5385] state_step state=10 mode=1 (time=0001.988,266,346)
[:crate5:04:pme6822:scsi:7:ncr5385] state_step state=14 mode=1 (time=0001.988,266,446)
[:crate5:04:pme6822:scsi:7:ncr5385] xfi_out: REQ asserted, data 0x80
[:crate5:04:pme6822] NCR5385: reg_w(0, 01) (':crate5:04:pme6822:maincpu' (0801A712))
[:crate5:04:pme6822:scsi:7:ncr5385] dat_w 0x01 (':crate5:04:pme6822:maincpu' (0801A712))
[:crate5:04:pme6822:scsi:7:ncr5385] state_step state=15 mode=1 (time=0001.988,267,366)
[:crate5:04:pme6822:scsi:7:ncr5385] xfi_out: data 0x01
[:crate5:04:pme6822:scsi] ctrl ..KQ.B.C. cmd  0001
[:crate5:04:pme6822:scsi] dev0=QBC
[:crate5:04:pme6822:scsi] dev1=K
[:crate5:04:pme6822:scsi:2:harddisk] state=5.2 change
[:crate5:04:pme6822:scsi:2:harddisk] nscsi_bus: scsi_put_data MAIN, id:0 pos:0 data:01
[:crate5:04:pme6822:scsi] ctrl ..K..B.C. cmd  0001
[:crate5:04:pme6822:scsi] dev0=BC
[:crate5:04:pme6822:scsi] dev1=K
[:crate5:04:pme6822:scsi:7:ncr5385] scsi_ctrl_changed 0x04a phase COMMAND ACK
[:crate5:04:pme6822] NCR5385: reg_r(5) (':crate5:04:pme6822:maincpu' (0801A718))
[:crate5:04:pme6822] NCR5385: reg_r(5) with reg6_cache_valid=1 cache=02
[:crate5:04:pme6822:scsi:7:ncr5385] state_step state=16 mode=1 (time=0001.988,277,366)
[:crate5:04:pme6822:scsi:7:ncr5385] xfi_out: 5 remaining
[:crate5:04:pme6822:scsi] ctrl .....B.C. cmd  0000
[:crate5:04:pme6822:scsi] dev0=BC
[:crate5:04:pme6822:scsi:2:harddisk] state=5.1 change
[:crate5:04:pme6822:scsi:2:harddisk] state=5.0 change
[:crate5:04:pme6822:scsi] ctrl ...Q.B.C. cmd  0000
[:crate5:04:pme6822:scsi] dev0=QBC
[:crate5:04:pme6822:scsi:7:ncr5385] scsi_ctrl_changed 0x02a phase COMMAND REQ
[:crate5:04:pme6822:scsi:2:harddisk] state=5.2 change
[:crate5:04:pme6822:scsi:7:ncr5385] state_step state=14 mode=1 (time=0001.988,277,466)
[:crate5:04:pme6822:scsi:7:ncr5385] xfi_out: REQ asserted, data 0x01


```

It gets stuck in the same loop 0x0801a73c-0x0801a748, where it waits for an interrupt to happen, but it never happens. Since it's a multi-byte transfer, the NCR won't trigger an interrupt until all bytes have been transferred. And since DMA is disabled, the driver should wait for the right moment to send the next byte, by polling the Aux register. But it's not doing that.

We shall go up the backtrace to see how it sets up the 6-byte transfer. Maybe there's a condition that goes the wrong way.

The write of "6" in the transfer count register happens at 0x0801a544. The CPU gets there by a jump table (switch/case) done at 0x0801a524:

```
                             LAB_0801a512                                    XREF[1]:     0801a506(j)  
        0801a512 1a 2e 00 00     move.b     (0x0,A6)=>scsilib_ncr_aux_reg,D5b                = 00h
        0801a516 ca 7c 00 38     and.w      #0x38,D5w
        0801a51a e4 0d           lsr.b      #0x2,D5b
        0801a51c 49 fa f4 62     lea        (-0xb9e,PC)=>scsilib_jump_table,A4
        0801a520 3a 34 50 00     move.w     (0x0,A4,D5w*0x1)=>scsilib_jump_table,D5w
        0801a524 4e b4 50 00     jsr        (0x0,A4,D5w*0x1)
```
This happens at `totalcycles=1f9b87e4`.

That jump table is run in two occasions:

* at totalcycles = 1f9b7ca, PC = 0x801a516, NCR Aux register = 0x32
* at totalcycles = 1f9bf76, PC = 0x801a516, NCR Aux register = 0x12

This second time, the driver reacts to the NCR getting into Command phase. Probably, this means that the target is ready to get a command. 
1. At 0x801a52a, A0 is set to the command bytes array at 0x87fdce8 and D0 is set to the length (6 bytes). 
2. The Transfer Length registers are written with the length. 
3. The Transfer Info command is issued at 0x801a706. 
4. The first byte to send (0x01) is written to the NCR Data Register at 0x801a712.
5. At 0x801a712, bit 5 of register 5 is read. In the current reg6 cache implementation, this causes the interrupt register to be read as well (0 at the moment, since the command is not yet complete), and the cache to be marked as valid. The bit value is then 0, and the CPU doesn't take the branch at 0x801a712.
6. The loop continues as in step 4, for the second byte and so on.
7. Once the loop finishes (all bytes being sent), the driver waits for an interrupt.
8. The interrupt arrives, and the Aux register is updated to 0x1A (C/D, I/O, Transfer Counter Zero: SCSI bus phase is Status)
9. Execution continues at 0x801a528. A (new) loop begins at 0x801a4f4.
10. The driver verifies that the SCSI target didn't disconnect (bit 2 of Interrupt register).
11. At 0x801a500, the driver verifies checks if the controller is in Bus Service, i.e. is waiting for the CPU to fulfill a request from the target (at this moment, the target seems indeed in STATUS REQ state). In this case it is, therefore it jumps to 0x801a512, where it re-enters the jump table.
12. The handler for MESSAGE OUT phase is executed, at 0x801a55e. It seems to set up a 1-byte inbound transfer.
13. Another Tranfer Info command happens, this time for a 1-byte transfer (NCR command code 0x54). The reg6 cache is cleared.
14. We're again at 0x801a726, where the 5th bit of register 5 is read. This will cause the Interrupt register to be read. Value is 0.
15. In the meantime, the NCR has triggered an interrupt. This may be a problem, because the driver is not yet waiting for it (interrupts are disabled at this time).
16. At 0x801a730, the Data Register Full bit is read. Since the status has been read, this reads as 1.
17. At 0x801a732, the status is stored at 0x87fddcc.
18. Since there are no more bytes to read, execution goes to the reactivation of the interrupts (0x801a738). This causes the interrupt to be serviced (surprisingly!). So far, so good.
19. Like in step 9, we go processing another phase change at 0x801a4f4. 
20. Same as in step 10, we check if the target is still connected. It is.
21. At 0x801a500, we check if we're in Bus Service. We are, so we jump to the jump table again.
22. The handler for MESSAGE IN phase is executed, at 0x801a56e. It seems to set up a 1-byte inbound transfer, with destination at 0x87fdb32.
23. The Transfer Info command is issued again.
24. At 0x801a57c, the contents of 0x87fdb32 are checked for nonzero. This confirms we just received a Command Complete message from the target, to signal that the entire command (starting with the 6-byte transfer) has been processed and the target is now idle.
25. The driver sends the Message Accepted command. This triggers an interrupt immediately, due to the bus being now free.
26. After a short wait, the handler goes back to 0x801a4f4.
27. The driver checks if the target is connected. Since the last command is complete, the target has indeed disconnected, therefore we jump to 0x801a634.
28. Some processing happens around 0x87fdc04, then jumps to 801a690.
29. Some other stuff happens, then it returns to the original caller at 0x801a902 (`scsilib_23`).
30. Another return to 0x8019a28 (`scsilib_1`).
31. ???
32. at 0x801a4b8, command 0x08 (Select w/ATN) is sent.

----

There is a race condition somewhere: the behavior changes between (hard) restarts.
In one case, it runs up to 1.997,396,220 seconds (after a slew of other unmapped memory access, but that's another story).
In another case, it gets stuck at 1.998,267,946 seconds. That's when the first byte of the 6-byte transfer is sent:

```
0001.988,266,346 [:crate5:04:pme6822:scsi:7:ncr5385] transfer info (pio, count=6)
0001.988,266,346 [:crate5:04:pme6822:scsi:7:ncr5385] state_step state=10 mode=1 (time=0001.988,266,346)
0001.988,266,446 [:crate5:04:pme6822:scsi:7:ncr5385] state_step state=14 mode=1 (time=0001.988,266,446)
0001.988,266,446 [:crate5:04:pme6822:scsi:7:ncr5385] xfi_out: REQ asserted, data 0x80
0001.988,267,366 [:crate5:04:pme6822] NCR5385: reg_w(0, 01)
0001.988,267,366 [:crate5:04:pme6822:scsi:7:ncr5385] dat_w 0x01 (':crate5:04:pme6822:maincpu' (0801A712))
0001.988,267,366 [:crate5:04:pme6822:scsi:7:ncr5385] state_step state=15 mode=1 (time=0001.988,267,366)
0001.988,267,366 [:crate5:04:pme6822:scsi:7:ncr5385] xfi_out: data 0x01
0001.988,267,366 [:crate5:04:pme6822:scsi] ctrl ..KQ.B.C. cmd  0001
0001.988,267,366 [:crate5:04:pme6822:scsi] dev0=QBC
0001.988,267,366 [:crate5:04:pme6822:scsi] dev1=K
0001.988,267,366 [:crate5:04:pme6822:scsi:2:harddisk] state=5.2 change
0001.988,267,366 [:crate5:04:pme6822:scsi:2:harddisk] nscsi_bus: scsi_put_data MAIN, id:0 pos:0 data:01
0001.988,267,366 [:crate5:04:pme6822:scsi] ctrl ..K..B.C. cmd  0001
0001.988,267,366 [:crate5:04:pme6822:scsi] dev0=BC
0001.988,267,366 [:crate5:04:pme6822:scsi] dev1=K
0001.988,267,366 [:crate5:04:pme6822:scsi:7:ncr5385] scsi_ctrl_changed 0x04a phase COMMAND ACK
0001.988,267,846 [:crate5:04:pme6822] NCR5385: reg_r(5) with reg6_cache_valid=0 cache=02
0001.988,267,846 [:crate5:04:pme6822:scsi:7:ncr5385] int_status_r 0x00 (':crate5:04:pme6822:maincpu' (0801A718))
0001.988,267,846 [:crate5:04:pme6822] NCR5385: reg_r(5) read reg6 into cache=00
0001.988,267,846 [:crate5:04:pme6822:scsi:7:ncr5385] state_step state=16 mode=1 (time=0001.988,267,846)
0001.988,267,846 [:crate5:04:pme6822:scsi:7:ncr5385] xfi_out: 5 remaining
0001.988,267,846 [:crate5:04:pme6822:scsi] ctrl .....B.C. cmd  0000
0001.988,267,846 [:crate5:04:pme6822:scsi] dev0=BC
0001.988,267,846 [:crate5:04:pme6822:scsi:2:harddisk] state=5.1 change
0001.988,267,846 [:crate5:04:pme6822:scsi:2:harddisk] state=5.0 change
0001.988,267,846 [:crate5:04:pme6822:scsi] ctrl ...Q.B.C. cmd  0000
0001.988,267,846 [:crate5:04:pme6822:scsi] dev0=QBC
0001.988,267,846 [:crate5:04:pme6822:scsi:7:ncr5385] scsi_ctrl_changed 0x02a phase COMMAND REQ
0001.988,267,846 [:crate5:04:pme6822:scsi:2:harddisk] state=5.2 change
0001.988,267,946 [:crate5:04:pme6822:scsi:7:ncr5385] state_step state=14 mode=1 (time=0001.988,267,946)
0001.988,267,946 [:crate5:04:pme6822:scsi:7:ncr5385] xfi_out: REQ asserted, data 0x01


```

Turns out, it's not a race condition but a case of unitialized memory. `ncr5385_device::m_own_id` was never set; it was supposed to be anything between 0 and 7, but sometimes the higher bits were also set; if bit 5 was set, then the check at 0x801a726 would make the driver think that the transfer was finished, even though only one byte was transferred.

-----

Lots of arbitration attempts, then the system just gives up and tries to load from RAM.

1. at 0x801a4b8, command 0x08 (Select w/ATN) is sent:

```
0001.738,047,810 [:crate5:04:pme6822] NCR5385: reg_w(1, 08)
0001.738,047,810 [:crate5:04:pme6822:scsi:7:ncr5385] cmd_w 0x08 (':crate5:04:pme6822:maincpu' (0801A4BE))
0001.738,047,810 [:crate5:04:pme6822:scsi:7:ncr5385] select 2 w/atn (timeout 0000.199,987,200)
0001.738,047,810 [:crate5:04:pme6822:scsi:7:ncr5385] state_step state=2 mode=0 (time=0001.738,047,810)
0001.738,047,810 [:crate5:04:pme6822:scsi:7:ncr5385] arbitration: waiting for bus free
```

The function at 0x081a40c is called four times. Here's the backtrace at each call:
 022006D8    0801A906    08019A28    02200002    0801C43E    ..�....(. ....�>
 022006D8    0801A906    08019A7C    00000002    0801C43E    ..�....|......�>
 022006D8    0801A906    08019A7C    00000001    0801C43E    ..�....|......�>
 022006D8    0801A906    08019A7C    00000000    0801C43E    ..�....|......�>


0001.988,781,043 [:crate5:04:pme6822] NCR5385: reg_w(1, 41)
0001.988,925,734 [:crate5:04:pme6822] NCR5385: reg_w(1, 41)


-----

