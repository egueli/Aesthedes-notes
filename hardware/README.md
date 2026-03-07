This document collects information about the internal AES2 hardware that can be useful to implement an emulator.

# General information

The Home Computer Museum has two Aesthedes 2. I named them "Hilversum" and "Klokhuis". 

I visited the museum in two separate occasions, on 2024-06-08 and 2026-02-20, and took photos and notes of the Hilversum machine. Most of the information presented here is derived from these visits.

Unless otherwise specified, these pages are about the Hilversum machine.
# System overview

The machine is made of 5 larger components:

* A central unit with power, CPU cards, graphics cards, and three terminal-like CRTs.
* A "desk" for user input, made of a large button matrix ("bitpad"), a digitizer ("digipad") and a mechanical keyboard.
* Three color CRT monitors.

# Central unit

On the back of the unit, the volume is divided into six spaces. The top-left one is almost entirely taken by the power supplies. The other five are VMEBus crates, with backplanes and rail guides.

The following diagram shows how the crates are filled with PCBs:

![Diagram depicting how VMEbus PCBs are installed inside the Aesthedes 2 "Hilversum".](cards_location.svg)

How to read the diagram:

* I numbered the crates left-to-right, then right-to-bottom: the PSU at top-left corner would be #1, #2 is below it, #3 is at its right and so on.
* Each crate has room for 20 cards. Each card takes a slot. I labeled the slots with a three-digit code, where the fist digit is the crate number and the other two is the slot number, left to right, starting from 1.
  * This numbering scheme is similar to the one used in the original [wiring diagram of the Aesthedes 1](https://www.egueli.com/aesthedes/pics/hcm/Aesthedesbekabeling.jpg). I didn't have that diagram at hand when I numbered the cards, so I went by memory.
* Most of the cards have no edge panel, silkscreen or other indication describing the connectors. To keep track of their wiring, I labeled each connector top-to-bottom, alphabetically starting with A. The PME 68-22M cards are the only ones with clear labels, SCSI and RS-232, so I labeled them S and R respectively.

## Cards

The cards in the system are all compatible with the VMEbus.

Each subsection will describe each card and how their connections are used.

### 302: PME 68-22, 68020 CPU
	S: SCSI to HDD (now BlueSCSI emulator)
	R: RS-232 connection to ? (maybe one of the 6 D-sub connectors
### 305: SCSI & floppy controller (NCR 53C90 SCSI controller + WD37C65 floppy controller)
	F: to the two floppy drives
### 320: Aesthedes C100/0006, I/O card, SN 778
	A: to 516B
	B: to 516A
	C: to 504R
	D: unplugged
### 504: PME 68-22, 68020 CPU
	S: SCSI to Quantum HDD
	R: to 320C
### 508: Aesthedes C100/065, RGB out, SN ?, w/ vertical RAM
	A: to 611A
	B: to 513C
	C: to 613B
	D, E, F: to Color Current R, G, B
### 513: Aesthedes C100/065, RGB out, SN 25
	A: unplugged
	B: to Color Combi Sync out?
	C: to 508B
	D, E, F: to Color Window R, G, B
### 516: Aesthedes C100/0006, I/O, SN 637
	A: to 320B
	B: to 320A
	C: to 616A
	D: unplugged
### 517: Aesthedes C100/0006, I/O, SN 784
	A: to Digipad
	B: to Keyboard
	C: to Bitpad
	D: unplugged
### 518: Aesthedes C100/0009, CRTC, SN 568
	A: to left B/W CRT
### 519: Aesthedes C100/0009, CRTC, SN 556
	A: to center B/W CRT?
### 520: Aesthedes C100/0009, CRTC, SN 455
	A: to right B/W CRT?
### 611: Aesthedes C100/0036.1, video A, SN 104
	A: to 508A
	B: to 613A
	C: to 618A
### 613: Aesthedes C100/0030, video B, SN 78
	A: to 611B
	B: to 508C
	C: to Color Combi Sync Out
	D, F, H: to Color Combi R, G, B
	E, G, I: unplugged
### 616: Aesthedes C100/0038, 68000 CPU, SN 1964
	A: to 516C
	B, C, D: unplugged
### 617: Aesthedes C100/0032, video input, SN 97
	A, C, E: unplugged
	B, D, F: to Camera Input R, G, B
### 618: Aesthedes C100/0048, video C, SN 71
	A: to 618C
### 619: Aesthedes C100/0035, video RAM, SN 89




## Connections

All the cards are connected with one another, either via VME backplanes on each crate, or via cables on the user-facing edge.

The following subsections describe the backplane connections.

### Crate 3 backplanes

There is a "front" and a "back" backplane, made to accommodate different card depths (6U and what I called 6U+). The two backplanes are connected together via an interposer card.

| Card location | Front backplane | Back backplane |
|---------------|-----------------|----------------|
| 302           | Both            |                |
| 305           | Top only        |                |
| 320           |                 | Both           |

### Crate 5 backplanes

There is a "front" and a "back" backplane, made to accommodate 6U and 6U+ cards. The two backplanes are connected together via an interposer card.




### Crate 6 backplanes

There is a single backplane for all the 6U+ cards. The top DIN 41612 connector has 3x32 pins, the bottom one has 2x32 pins.

| Card location | Backplane usage     |
|---------------|---------------------|
| 611           | Both                |
| 613           | Both                |
| 616           | Bottom only         |
| 617           | Both                |
| 618           | Bottom only, 3 rows (*) |
| 619           | Top (**)             |

(*) No idea if the third row is actually connected. We should better look at that backplane.

(**) This card has a 2x32 connector on the bottom backplane but no pin seem connected to any PCB trace.


