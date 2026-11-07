# `fcontrol` <-> `m2dispsys` command protocol

(note: this document is AI-generated)

## Summary

The Ghidra evidence supports the theory that `fcontrol` sends commands to
`m2dispsys` through a shared module-data buffer and an OS-9 event. The event is
a notification, not the command transport itself: the sender writes the command
and its arguments into the service module's data area, then signals the event;
the receiver waits for that event and reads the shared buffer.

The protocol below is reconstructed from the `fcontrol` and `m2dispsys` code in
the Ghidra program `fcontrol` (68000, OS-9 module). Some fields are not
understood well enough to name more precisely, and are marked accordingly.

## Service setup

In the `fcontrol` portion:

1. `FUN_086eb0fe` takes a service name and formats two names from it:
   `EV_<service>` for the event and `DM_<service>` for the data module.
2. It creates the service event, loads the data module, and obtains a pointer
   to that module's data area.
3. It stores the event ID and data-area pointer for later send/receive
   operations. It also calls the `SetEvent` wrapper once during setup.

The `m2dispsys` side has matching `EV_%s` and `DM_%s` name formats and obtains
the service data area used by its command receiver. This is consistent with a
name-based service connection. The sender's service name is passed at runtime;
the code inspected here does not by itself prove which caller supplied
`m2dispsys` as that name in a particular run.

## Sending a command

`FUN_086eb478` is the clearest sender-side example. It writes four 16-bit
header words to the shared data area, then calls the `SetEvent` wrapper
(`FUN_086f3e42`) for the service event:

| Word offset | Contents | Confidence |
|---|---|---|
| 0 | Command/opcode (`DAT_00024814` low word) | High |
| 1 | A second command-related word (value supplied in `D0.w`) | Exact role not established |
| 2 | Argument count (`DAT_00024824` low word) | High; receiver uses it as the number of typed arguments |
| 3 | Zero/reserved | High |
| 4 onward | Encoded arguments | High; consumed by the receiver's typed-argument reader |

The event call uses OS-9 `F$Event` operation 10 in the wrapper. The event value
is a separate per-command field; it is not the opcode or an argument. The
wrapper is called `SetEvent` by its caller.

The setup and send paths therefore have two distinct roles:

- **Shared module data** carries the command header and argument bytes.
- **`F$Event`** wakes/notifies the receiver that command data is available.

## Receiving and dispatching a command

The `m2dispsys` main loop in `FUN_m2dispsys__087d8062` repeatedly:

1. Calls `receive_opcode()`.
2. Passes the returned 16-bit value to `opcode_dispatcher()`.
3. Runs its post-command processing before looping.

`receive_opcode()` calls `FUN_m2dispsys__087e780e`, which invokes
`FUN_m2dispsys__087e8212` and then reads the header from the shared data area.
`FUN_m2dispsys__087e8212` calls `FUN_m2dispsys__087ea524`; its `TRAP #0`
instruction is identified in Ghidra as OS-9 `F$Event`. The wrapper sets the
event operation to 4, consistent with the receiver waiting for the sender's
notification.

After waking, `FUN_m2dispsys__087e780e` reads the header words and initializes
the argument cursor to the data immediately after the four-word header.
`receive_opcode()` returns the first header word, which the main loop dispatches
as the opcode. Thus the opcode is read from the shared command block, not
directly from a PIA register.

## Argument encoding

The common `read_command_word()` helper calls `FUN_m2dispsys__087e78be`. That
reader consumes one type-tag word for each argument, advances the cursor by a
tag-dependent number of additional words, and increments the argument count.
The decompiled switch indicates these advances:

| Type tag | Additional 16-bit words skipped |
|---:|---:|
| 1 | 1 |
| 2 | 2 |
| 3 or 5 | 4 |
| 4 or 6 | 3 |
| 7 | 5 |

The opcode handlers use helpers such as `read_command_word()` and other typed
readers to decode the payload. The exact byte order and full meaning of every
type are not inferred here; the table records the cursor behavior visible in
the reader.

## Opcode reference

### `0007/0321` — set level RGB color

This command sets the RGB color for one multi-level screen intensity level.
The `m2dispsys` dispatcher handles opcode `0x0321` in `opcode_321`; the
corresponding `fcontrol` command is identified as `0007/0321`.

The observed event value for this opcode is `2`.

The command has four dword arguments:

| Argument | Meaning | Valid/used value |
|---:|---|---|
| 1 | Level number | `0x00`–`0x3F` |
| 2 | Red | Least-significant byte is used; upper 24 bits are ignored |
| 3 | Green | Least-significant byte is used; upper 24 bits are ignored |
| 4 | Blue | Least-significant byte is used; upper 24 bits are ignored |

The handler reads four arguments and passes them to `send_set_color_command`.
That routine builds a four-byte payload (level, red, green, blue) and sends it
as PIA command `3` via `send_pia_command_packet`.

### `0007/0065` — purpose unknown

This command is observed with event value `0` and no arguments. Its purpose is
not yet known. One possibility is that it saves or selects the level most
recently sent with `0007/0321`, but this is only a hypothesis and has not been
confirmed from the handler or its effects.

## Relation to the PIA output paths

Once `opcode_dispatcher()` receives a command, some handlers can reach
`send_pia_command_packet()` and `m2_dispsys_pia_send()`. The latter writes
through `io_addr_table[pia_idx]`; `send_pia_command_packet()` passes PIA index
6. This is downstream of the IPC receive/dispatch protocol: the OS-9 event
delivers work to `m2dispsys`, while the PIA routine performs the eventual
hardware transmission.

The command values and their PIA send paths are documented in the separate
trace analysis. Static reachability shows what the handlers could send; it
does not establish that a given command was sent in the captured trace.

## Evidence and caveats

- `fcontrol`: `FUN_086eb0fe` (service/event setup), `FUN_086eb478` (write
  header and notify), `FUN_086f3e42` / `FUN_086f6970` (SetEvent wrapper and
  `F$Event` operation 10).
- `m2dispsys`: `FUN_m2dispsys__087d8062` (receive/dispatch loop),
  `receive_opcode()` at `m2dispsys::087e40a2`,
  `FUN_m2dispsys__087e780e` (read header and set argument cursor),
  `FUN_m2dispsys__087e8212` / `FUN_m2dispsys__087ea524` (wait using
  `F$Event` operation 4), and `FUN_m2dispsys__087e78be` (typed argument
  cursor).
- Ghidra's decompiler has imperfect parameter names and signatures around
  register-based OS-9 calls. The event operation numbers and data flow are
  corroborated by the disassembly; the meaning of the second header word and
  the purpose of `0007/0065` remain open questions.
- The code supports a shared-memory-plus-event protocol. It does not show the
  OS-9 event carrying the opcode itself.