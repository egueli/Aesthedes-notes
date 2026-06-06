# Aesthedes ROM (bootloader, OS-9 kernel, modules)

## Modules

| Name      | Start address | End address            | Type (M$Type)            |
| --------- | ------------- | ---------------------- | ------------------------ |
| `init`    | 80149f4       | 8014aac                |                          |
| `SCSILIB` | 80198f8       | 801af20                |                          |
| `sysgo`   | 801af20       | 801c326                |                          |
| `H0SCSI`  | 801c3a8       | 801c4f2                | Physical Device Driver   |
| `h0`      | 801c5a0       | 801c64e (end of EPROM) | Device Descriptor Module |

### `init` module

This is the data module used by the kernel to initialize itself. Some possibily relevant details:

* The first process to be launched is `Sysgo`.
* The initial default directory name (`M$SysDev`) is `/h0`.
* The initial I/O pathlist (`M$Consol`) is `/Term`.
* The installation name string is `BARCO Graphics - AESTHEDES`.
* The OS-9 version is level 1, version 2.2, edition 0.
* The OS-9 name string is `OS-9/68020 V2.2`.

### `h0` module

This is a device descriptor for the SCSI hard disk. It references RBF as the file manager and `H0SCSI` as the driver.

## Boot priority order

1. `/D0`
    * Note that there is no device descriptor called `D0` or `d0`, therefore that boot entry may never succeed.
2. `/H0/CMDS`
3. `/ROM0`
    * If the RTC is not present, all of the above are skipped and it will directly try with this one.

