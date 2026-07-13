# Aesthedes ROM (bootloader, OS-9 kernel, modules)

## Modules

| Name      | Start address | End address            | Type (M$Type)            |
| --------- | ------------- | ---------------------- | ------------------------ |
| `init`    | 80149f4       | 8014aac                |                          |
| `crtdrv`  | 8016a96       | 8017188                | Physical Device Driver   |
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

Given that this module is referenced by `init` as the default directory's device, it may be loaded and initialized early in the boot process, before Sysgo.

Its initialization routine loads the `SCSILIB` library module.

### `SCSILIB` module

This library module implements the SCSI protocol and the low-level logic to control the NCR 5386 SCSI controller and the related interrupt and DMA on the PME 68-22.

### `crtdrv` module

This driver controls an R6545 CRTC. It will use address 1 to access the address register and register 3 for the status register.

It initializes the video in three stages:

1. First-stage CRTC init (all parameters set, but keep R1 (no. of horizontal display characters) to 0)
2. Initialize the video memory with 0x20 (space)
3. Second-stace CRTC init (set R1 to 80 characters)

It configures the CRTC to display an 80x25 screen with a 12-line font and transparent memory access.

Parameters:
```
R0 - Horizontal Total: 111 [6f] = 112 total characters per line
R1 - Horizontal Displayed:  80 [50] = 80 displayes characters per line
R2 - Horizontal Sync Position:  91 [5b] = HSYNC at character 91
R3 - Sync Width:  56 [38] = Pulse widths: HSYNC 8 clocks, VSYNC 3 lines
R4 - Vertical Total:  23 [17] = 24 total character rows
R5 - Vertical Total Adjust:  25 [19] = 25 additional scan lines to complete a frame
R6 - Vertical Displayed:  24 [18] = 25 displayed rows
R7 - Vertical Sync Position:  24 [18] = VSYNC at row 24
R8 - Interlace & Skew: 120 [78] [.6543...] = 
    * 7: update at HBlank / Vblank with update strobe
    * 6: pin 34 as update strobe
    * 5: delay cursor one character time
    * 4: Display Enable delayed one character time
    * 3: Transparent memory access
    * 2: Straight binary addressing
    * 1-0: No interlace
R9 - Maximum Raster Address:  11 [0b] = characters are 12 pixels tall
R12 - Start Address (H):   0 [00]
R13 - Start Address (L):   0 [00]

```

## Boot priority order

1. `/D0`
    * Note that there is no device descriptor called `D0` or `d0`, therefore that boot entry may never succeed.
2. `/H0/CMDS`
3. `/ROM0`
    * If the RTC is not present, all of the above are skipped and it will directly try with this one.

