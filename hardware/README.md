This document collects information about the internal AES2 hardware that can be useful to implement an emulator.

# Hardware analysis

## CPU cards PME 68-22M

By looking again at the [pictures I made to the Aesthedes boards](pics) when I visited the HCM on 8th June 2024, I noticed the text "PME 68-22M" on the handle of the CPU board. After some intensive googling, I found out a few facts I didn't know:

- PME 68-xx was a lineup of VME-bus CPU boards with 68k architecture for industrial/defense applications, made by Plessey Microsystems, UK-based, later [incorporated](https://www.techmonitor.ai/technology/vme_board_builder_plessey_microsystems_becomes_radstone_in_management_buyout) by Radstone Technology Ltd, who later became Abaco Systems.

  - This means that the CPU board is a commercial product, rather than something developed in-house. This could make it easier to write an emulator for, especially if somehow we manage to get the technical manuals or even another board.

- Unsurprisingly, the entire PME 68-xx lineup is now discontinued. One can find some old stock hardware via [eBay](https://www.ebay.com/sch/i.html?_nkw=pme+68&_sacat=0&_from=R40&_trksid=p4624852.m570.l1313) or [Artisan Technology Group](https://www.artisantg.com/Search?q=pme%2068), an US-based company specialized in old electronics equipment. 

- It is also a bit hard to find technical information about the 68-22M. The [OS-9 HW/SW Source Book 1988](https://colorcomputerarchive.com/repo/Documents/Books/OS-9%20Hardware-Software%20Source%20Book%201988%20Edition%20(Microware).pdf) describes it as:
  > "Multi-user/multitasking processor, 68020 CPU, optional FPCP, 68851 PMMU, SM dual-port DRAM, on-board SCSI interface, 2 async. ports, programmable timer, real-time clock, up to 64K EPROM.".
  
  [This other document](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=1663520) says about it:
  
  > "The PME 68-22 ($4350) has multitasking paged memory management for Unix, IEEE-P754 floating-point capability, an intelligent SCSI interface, and offers 32-bit processing at 16.7 or 20 MHz.".
- Among the lineup described by the OS-9 Source Book, the 68-22 looks like the most complex one with its SCSI interface (which is obviously used for the Aesthedes hard drive) and MMU, unlike similar products like the 68-23. The 68-23 is [on sale by Artisan](https://www.artisantg.com/TestMeasurement/69626-6/Abaco-Systems-Radstone-PME-68-23-VME-Module).

- I could not find a technical manual for the 68-22, but we can look for similar products to get an idea on how the 68-22 system architecture would look like:
    - In the same lineup there are manuals for [68-1B](manuals/pme_681b-1.pdf) and the [68-14](manuals/Radstone_PME_68_14_SBC_Manual-1.pdf). They're equipped with a 68000 and a 68010 respectively.
    - One can expand the search for boards with the same or similar chipset (68020 CPU, 68851 MMU, VME, optional SCSI) made by other companies. Examples are Motorola's MVME132, MVME136 ([manual](https://www.mvme.net/manuals/MVME135_136-manual.pdf)), Compcontrol CC-120, Cyclone Microsystems CY4110. 
    - Among non-VME systems, one can find the Macintosh II (with MMU installed) and the Amiga A2500.

- About the "M" suffix in 68-22M: The 68-14 manual specifies that the 68-14M variant has more memory; therefore, the suffix may indicate it has more RAM than the standard version (how much anyway?).

- These boards come with ROM/EPROM sockets, some populated with firmware provided by Radstone, some unpopulated so the user can supply their own EPROMS.
  - The OS-9 kernel used by the Aesthedes may reside in one of such chips.


Some insights about how these boards are installed in the Aesthedes:
  - There are two identical 68-22Ms (except for EPROM contents maybe?). This matches with the machine specs having 2x68020.
  - One of them is mounted near the power supplies, the other near the video cards. Let's call them "A" and "B" respectively.
  - They both seem to be attached to two independent VME backplanes.
  - Maybe the A board hosts the application/UI and B takes care of rasterization on screen? Although the B seems connected to the only SCSI hard drive. It would be great to have a system block diagram to clarify that.
  - In picture 172344 we see the A next to a SCSI controller board. Both boards have a SCSI flat cable attached. Since the hard drive seems to be connected to the B, so I'm not sure what are they attached to.
    - To each other? What for? There's the VME backplane already.
    - To the floppy drives? Unlikely, because the HDD images contain drivers for the [WD37C65](https://bitsavers.org/components/westernDigital/_dataSheets/WD37C65.pdf) which is all but a SCSI controller.
  - Besides, what are the floppy drives connected to? And where is the WD37C65?

About the video cards: it might well be the case that they are built in-house, given how peculiar the Aesthedes was w.r.t. other computers of its era. The lack of a front panel/handles with model information may also be a hint. A reverse-engineering (PCB photographs, EPROM/GAL/PAL dumps) may be in order, if anything for preservation purposes.

## All cards

### Crate 3 backplanes

There is a "front" and a "back" backplane, made to accommodate different card depths (6U and what I called 6U+). The two backplanes are connected together via a bridge card.

| Card location | Front backplane | Back backplane |
|---------------|-----------------|----------------|
| 302           | Both            |                |
| 305           | Top only        |                |
| 320           |                 | Both           |

### Crate 5 backplanes

There is a "front" and a "back" backplane, made to accommodate 6U and 6U+ cards. The two backplanes are connected together via a bridge card.




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