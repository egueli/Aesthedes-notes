# `AE_CONFIG` EPROM analysis

These EPROMs contain configuration data used by the Aesthedes startup and application code.

The data is formatted as an OS-9 data module; as such, it starts with magic numbers 4A FC and end with a 3-byte CRC over the entire contents.

## Hex dumps

AE_CONFIG @504:

```
00000000  4a fc 00 01 00 00 00 80  00 00 00 00 00 00 00 34  |J..............4|
00000010  00 03 04 00 80 01 00 01  00 00 00 00 00 00 00 00  |................|
00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 31 b5  |..............1.|
00000030  00 00 00 3e 41 45 5f 43  4f 4e 46 49 47 00 01 20  |...>AE_CONFIG.. |
00000040  20 00 04 fc 00 00 59 56  40 01 01 05 11 11 02 00  | .....YV@.......|
00000050  01 00 13 ff 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000060  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000070  00 00 00 00 00 00 00 00  00 00 00 00 00 1c 67 bb  |..............g.|
```

AE_CONFIG @302:

```
00000000  4a fc 00 01 00 00 00 80  00 00 00 00 00 00 00 34  |J..............4|
00000010  00 03 04 00 80 01 00 01  00 00 00 00 00 00 00 00  |................|
00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 31 b5  |..............1.|
00000030  00 00 00 3e 41 45 5f 43  4f 4e 46 49 47 00 01 20  |...>AE_CONFIG.. |
00000040  20 00 04 fc 00 00 59 56  40 01 01 05 11 11 02 00  | .....YV@.......|
00000050  01 00 13 ff 00 00 00 00  00 0f 00 0f 00 04 00 04  |................|
00000060  00 08 00 01 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000070  00 00 00 00 00 00 00 00  00 00 00 00 00 d6 89 d4  |................|
```

## Screen outputs

Output of `print_eprom -e` run from os9exec emulator:

```
$ print_eprom ae_config_504.bin

SYSTEM-OPTIONS
        SYSTEM_ID : 01
        TARGET_ID : 20
        USER_ID   : 5956
        MEMORY    : 8192
        BASE      : 04FC0000

AES2-OPTIONS
        GDP_1  : 64
        GDP_2  : 1
        COLOUR : 01
        SERVER : 05
        KEYBOARD : 1
        BITPAD   : 1
        LANGUAGE : 0
        ASCII    : 2
        SCREEN1  : 1
        SCREEN2  : 1
        OPT_ALL_OPTIONS

STORAGE DEVICES
        HARD_DISK  :
        FLOPPY     :
        TAPES      :

BOOT DEVICES
        HARD-DISK  : QUANTUM   
        FLOPPY     :  

```

302:

```
$ print_eprom ae_config_302.bin

SYSTEM-OPTIONS
        SYSTEM_ID : 01
        TARGET_ID : 20
        USER_ID   : 5956
        MEMORY    : 8192
        BASE      : 04FC0000

AES2-OPTIONS
        GDP_1  : 64
        GDP_2  : 1
        COLOUR : 01
        SERVER : 05
        KEYBOARD : 1
        BITPAD   : 1
        LANGUAGE : 0
        ASCII    : 2
        SCREEN1  : 1
        SCREEN2  : 1
        OPT_ALL_OPTIONS

STORAGE DEVICES
        HARD_DISK  :    QUANTUM   
        FLOPPY     :    SF001 + 3.5
        TAPES      :    MT0_QIC150      MT1_GCR990      MT2_EXABYTE     OPTICAL    

BOOT DEVICES
        HARD-DISK  : PRIAM V738
        FLOPPY     : SF001 + 3.5 

```

