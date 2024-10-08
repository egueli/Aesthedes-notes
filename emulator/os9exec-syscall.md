# Make os9exec print process address on syscall enter

Objective: figure out in Ghidra where `app` decides to exit.

I want `os9exec` to print the program counter (UPC) of the user process when it called a syscall.

- `I$Close` is implemented in `OS9_I_Close`.
- `OS9_I_Close` is referenced in the `icalltable` array.
- `icalltable` is used in `getfuncentry` and `show_syscalltimers`. We can ignore the latter.
- `getfuncentry` takes the raw syscall number i.e. 0x80 + syscall id. Gotta figure out how is this number is taken: its location is near the PC.
- `getfuncentry` is invoked by several functions: `debug_comein`, `debug_return`, `exec_syscall`. The latter seems the most interesting.
- `exec_syscall` is invoked by `os9exec_loop` line 1880, when processing TRAP0. It used `cp->func` to get the raw syscall number: that comes from the result of `llm_os9_go` → `OS9_GO`