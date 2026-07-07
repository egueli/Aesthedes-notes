Once that the kernel has been able to "mount" the SCSI hard drive, another error appears:

```
OS-9/68K System Bootstrap
OS-9 kernel found in ROM at $08010004
Can't access /D0
Error #000:221
**** Can't install trap handler ****
 **** cio ****
```

Which process triggered this error? Is it `sysgo`, or something else? What else is `sysgo` launching after itself?

It's `sysgo`. It calls `F$TLink` at 801BBE4 to load `cio`, and that fails with error code 0xE8 = 232 (Bad Module CRC).

When enabling `LOG_COMMAND` logging in `nscsi/hd.cpp`, the logs are:

```
[:crate5:04:pme6822:scsi:2:harddisk] 28 00 00 00 00 00
[:crate5:04:pme6822:scsi:2:harddisk] command READ EXTENDED start=00000000 blocks=0001
[:crate5:04:pme6822:scsi:2:harddisk] 28 00 00 00 00 20
[:crate5:04:pme6822:scsi:2:harddisk] command READ EXTENDED start=00000020 blocks=0001
[:crate5:04:pme6822:scsi:2:harddisk] 28 00 00 00 00 21
[:crate5:04:pme6822:scsi:2:harddisk] command READ EXTENDED start=00000021 blocks=0001
[:crate5:04:pme6822:scsi:2:harddisk] 28 00 00 00 00 22
[:crate5:04:pme6822:scsi:2:harddisk] command READ EXTENDED start=00000022 blocks=0001
[:crate5:04:pme6822:scsi:2:harddisk] 28 00 00 00 18 f0
[:crate5:04:pme6822:scsi:2:harddisk] command READ EXTENDED start=000018f0 blocks=0001
[:crate5:04:pme6822:scsi:2:harddisk] 28 00 00 00 18 f1
[:crate5:04:pme6822:scsi:2:harddisk] command READ EXTENDED start=000018f1 blocks=0026
[:crate5:04:pme6822:scsi:2:harddisk] 28 00 00 00 19 17
[:crate5:04:pme6822:scsi:2:harddisk] command READ EXTENDED start=00001917 blocks=0001
```
Block 0 is LSN 0. Blocks 20-22 contain the `CMDS` directory (with `cio` being at sector 22).

`cio` starts indeed at sector 18f1. It is 0x4ee0 = 20192 byte big. The last byte is before raw image offset 0x322fe0 (sector 0x1917 offset 0x1e0).
Is it fully copied in memory before CRC computation?
And if so, where?

Let's let it read a few sectors then use MAME to find a unique data sequence, like `4a fc 00 01 00 00 4e e0`:
```
find $08000000,$087ffffff,d.4afc0001,00004ee0
Found at 087F7890
```
By looking there, it seems that only the first 256 bytes have been written to memory, then a lot of zeros until 87FC590, then valid data until 87FC770 where the CRC bytes (5545B0) can be seen.

That data should have been read by a 38-sector read:
```
[:crate5:04:pme6822:scsi:2:harddisk] command READ EXTENDED start=000018f1 blocks=0026
```
Therefore, it looks like the current I/O reading part works only for a single sector at a time, and fails otherwise. Is it the SCSI HDD implementation? The DMA? SCSILIB?

By enabling `LOG_GENERAL | LOG_COMMAND` in `hd.cpp`, it looks like both the single-sector read of sector 18F0 (containing the file descriptor of `cio` and the first LSN) and the 38-sector read starting from 18F1 are read just fine.

A possible cause is that the multi-sector read should trigger the 1K-large transfers as mentioned in [SectorSize.md](SectorSize.md). Because that condition is hardcoded to less than that, too few data (or none at all) is transferred. The destination address when `scsilib_read_sector` is hit (i.e. 801A784) is around 87F7990 which is wide enough to store such large transfers.

After some investigation, including the "discovery" of a 1KiB FIFO right on the board (Renesas IDT7202), it turns out that SCSILIB expect the input pin 2 of the DUART to be low when the FIFO is full. After implementing that logic, all multi-sector reads now work as expected.
