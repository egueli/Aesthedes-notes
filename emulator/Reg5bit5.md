# Reg5bit5

The PME 68-22M has a NCR 5386 SCSI controller, mapped at addresses 0x20000..0x2000f.

The SCSI driver in the Aesthedes ROM (`SCSILIB`) reads and writes to its various registers. One of them, at index 5, stores the controller's own ID, that is never changed from its default of 7, it frequently reads bit 5 of register 5. That bit is not documented in the datasheet.

It seems to be used to "peek" at the interrupt pin without acknowledging it, while in a busy-loop when interrupts are disabled.

The SCSI interrupt handler, at 0x801a334, reads it as the very first thing. Maybe because that same IRQ line is used by other peripherals and this is used as a discriminator.

Outside the interrupt, it is read at other locations.
