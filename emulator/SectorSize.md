# Sector size

The code that reads a sector has this snippet:

```
                     LAB_0801a7c2                                    XREF[1]:     0801a7b6(j)  
0801a7c2 3a 3c 00 ff     move.w     #0xff,D5w                                        transfer 1024 bytes from queue
                     LAB_0801a7c6                                    XREF[1]:     0801a7c8(j)  
0801a7c6 20 d4           move.l     (A4),(A0)+
0801a7c8 51 cd ff fc     dbf        D5w,LAB_0801a7c6
```

This transfers 1KiB from the DMA scratchpad (0x30000) to a memory block (0x87FD8F0). That block contains zeros but there is an OS-9 header at 0x87FDAF0, 512 bytes after that. That transfer overwrites existing data and even the stack area, causing a really bad crash shortly after.

I tried manually patching that 0xff to a lower value but there are issues later (see Sector number confusion below). A possible option is to figure out how that block size is computed, and see if can somehow alter it so that the block starts at a lower address to make room for 1KiB.

* A0 = 0x87FD8F0 is done at 801A778, read from 0x87FDBFC.
* That location is written by 801A3CA (at 3rd hit), using A2+0xD8. That's 87FDCF8.
* 87FDCF8 is being written by 801AB26 (at 1st hit), using A0 which was set at 801AAF2 where multiple registers were read from A2+0x1FE. That's 87FDE1E. A0 is stored at 87FDE3E.
* The last time 87FDE3E was written with 87FD8F0, was by 801AACC.
* That's in the same function: 87FD8F0 is carried as argument by D0.
* That function is called by 801AD42. D0 is set to the value of A3 at that time.
* At 801AC4E, A3 is set to 87FD8F0 by reading from A2+0x1E2. That's 87FDE02.
* That location is being written with 87FD8F0 by 8019AC2, from A2, which contains the address of a block of memory requested to the OS at 8019AB8 (F$SRqMem).
* I believe that the number of requested bytes, 0x200 (in D0 register), is too low and should have been 0x400 (1KiB).
* D0 takes the value of 87FDE0E, written by 8019AAE.
* 8019AAE ultimately takes that value from the `h0` device descriptor at offset 0x51, containing 0x200. 

So, some things don't quite match:

* Looking at the hard disk image's hexdump, one can clearly see data organized in 256-byte blocks.
* But the `h0` device descriptor defines a 512-byte sector.
    * This may not be a problem: OS-9 supports _logical_ 256-byte sectors fitting into _physical_ 512-byte sectors. Therefore, `h0` may simply describe the physical disk layout.
* And `SCSILIB` transfers 1024 bytes regardless of the actual size of the buffer used to store a sector's worth of data.

# "Fast" 1K transfer

Is it possible that there are alternative execution paths, that don't involve the 1K hardcoded transfer loop?

I noticed that the function at 801A784 (`scsilib_read_sector`) has several `move (A4), (A0)+` instructions in a loop, to transfer from the hardware FIFO to a memory block:

* The one at 801A7C6, is hard-coded to 1K transfers;
* The one at 801A82A depends on the value of D5w.

Idea: what if the 1K transfer loop at 801A7C2 was actually meant to be run only when 1K+ bytes have to be transferred? Maybe for the Aesthedes, with its 512-byte hard drive, that loop wouldn't never run and the other one would run instead.

The last branching point between the two loops is at 801A7B6:

```
                             LAB_0801a7b2                                    XREF[2]:     0801a7be(j), 0801a7d2(j)  
        0801a7b2 08 12 00 02     btst.b     #0x2,(A2)=>duart_input_port                     
        0801a7b6 67 0a           beq.b      LAB_0801a7c2                                     if finished, jump
        0801a7b8 08 2b 00        btst.b     #0x5,(0x5,A3)                                    is NCR asserting IRQ?
                 05 00 05
        0801a7be 67 f2           beq.b      LAB_0801a7b2                                     if not, keep waiting
        0801a7c0 60 14           bra.b      LAB_0801a7d6
                             LAB_0801a7c2                                    XREF[1]:     0801a7b6(j)  
        0801a7c2 3a 3c 00 ff     move.w     #0xff,D5w                                        transfer 1024 bytes from queue
                             LAB_0801a7c6                                    XREF[1]:     0801a7c8(j)  
        0801a7c6 20 d4           move.l     (A4),(A0)+                                       copy from DMA scratchpad 4 bytes
        0801a7c8 51 cd ff fc     dbf        D5w,LAB_0801a7c6
        0801a7cc dc bc 00        add.l      #0x400,D6
                 00 04 00
        0801a7d2 51 cc ff de     dbf        D4w,LAB_0801a7b2
                             LAB_0801a7d6                                    XREF[1]:     0801a7c0(j)  
        0801a7d6 46 ee 00 be     move       (0xbe,A6)=>scsilib_sr_copy,SR

```
If the branch at 801A7B6 is never taken, flow goes to 801A7B8 where execution either loops back to 801A7B2 or jumps to 801A7D6, skipping the entire 1K transfer.

To do that, a simple way would be to set IP2 always high (before, I wired it to the FIFO state i.e. high if empty, low otherwise). But now the SCSI write function (at 801A840), invoked before this one, is unhappy: it gets stuck in an infinite loop (at 801A890) waiting for IP3 to be low. 

What happens if IP3 is permanently low? The write function now works fine. Most importantly, the read function finally skips the 1K transfer! But that's not enough, because it checks if IP3 is high (at 801A7E8) to actually perform the copy; if not, it returns without copying anything.

So, it looks like the write function wants IP3 to be low, and the read function to be high. How can the 68-22 hardware know which is the wanted direction? Maybe from the OPx pins they set right when they're called?
```
                             undefined scsilib_read_sector()
...
        0801a786 15 7c 00        move.b     #-0x80,(0xf,A2)
                 80 00 0f
        0801a78c 15 7c 00        move.b     #0x4,(0xf,A2)
                 04 00 0f

```
After this, OP7, OP6 and OP2 are set.
```
                             undefined scsilib_write_data()
...
        0801a844 15 7c 00        move.b     #-0x80,(0xf,A2)
                 80 00 0f
        0801a84a 15 7c 00        move.b     #0x4,(0xe,A2)
                 04 00 0e
```
After this, only OP7 and OP6 are set.

It looks like OP2 is used by SCSILIB to tell the hardware the DMA direction: high for a read, low for a write.

So, what happens if we simply wire IP3 to OP2? It happens that it worked :D


# Sector number confusion

The system is able to read the first sector (LSN 0), and when it's time to read the root directory entries, the emulated drive returns the contents of LSN 7. That's the descriptor sector of the root directory at LSN 8.

The system asks for sector 0, then sector 3. It looks like it doesn't find what it's looking for, because shortly after it falls back on searching for a ROM disk.

So, either it should be reading sector 8 instead of 3, or something else prevents it from reading sector 8 after having successfully read sector 0 and 3.

I see some confusion in the sector size: the HD image is organized in 256-byte sectors, but OS-9 does 512-byte reads. OS-9 may read two sectors at a time, or maybe just use the first 256 bytes and ignore the rest.

The driver sends a MODE SELECT command (section 8.1.7 of https://nvlpubs.nist.gov/nistpubs/Legacy/FIPS/fipspub131.pdf) specifying a block size of 512 bytes. But the HD has 256-byte sectors. Even if the emulated drive has knowledge of a 256-byte image, it must be able transfer 512-byte blocks through the SCSI bus. I fixed this by patching `nscsi/hd.cpp`.

With these fixes, it now gets the contents of sector 3 (i.e. offset $300 of the HD image). But it's still not happy.

Maybe it's asking for the wrong sector. Some calculation, that should result in number 8, may have gone wrong and it results in 3 instead.

* The request of sector 3 can be traced by a write of 00000003 to 087FDCEA, at PC=0801AB1A, from register D2.
* D2 was set from 087FDE26, which was last written with this value by 0801AAD6 (second time after reset).
* That value was read from the stack (A7+4). The function started at 0801AAC4.
* That function is called by 0801AC9E, with D1=3.
* It was part of function 801AC26, its caller is at 8019AF8 (`scsilib_2`).
* `scsilib_2` seems to exit without error (i.e. with carry bit clear).

Do note that RBF asks for LSN 0 (call to 801c472) followed by LSN 7. So, it is SCSILIB that seems to be doing some mapping that leads to sector 3.