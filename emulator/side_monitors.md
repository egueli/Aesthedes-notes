# Enable the side monitors

The right one is the Current-Level monitor, while the left one is the Window (detail) monitor. Each is controlled by an aes_gpu card.

The lack of these cards causes the loading of a design file to fail. This has been worked around by implementing a skeleton card that returns 0xff.

The next step is to add an emulated EF9365 chip since the system reads/writes to registers in a way that matches the '9365 register map.

But, the file loading fails again.

Looks like subroutine $87E02DE, that tries to initialize the two side video cards, returns 2 instead of 0. That may be because it failed to initialize the second card (first card = 1; both cards = 3).

That's done by the function $87D9D9A, which returned -1 instead of zero.