# Sector size

The system is able to read the first sector (LSN 0), but when it's time to read the root directory entries, the emulated drive returns the contents of LSN 7 instead of LSN 8. The system asks for sector 0, then sector 3. It looks like it doesn't find what it's looking for, because shortly after it falls back on searching for a ROM disk.

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
