## Basic usage

```
./serialize_rx.py canIf uartIf
./serialize_tx.py canIf uartIf
```
eg.
```
./serialize_rx.py vcan0 /dev/ttyUSB0
./serialize_tx.py can0 /dev/ttyUSB0
```

## Lib files

### `can_buffer.py`
Stores last value of frame receiver over socketcan.

### `myFrames.py`

Translates socketcan objects to bytes and translates bytes to socketcan objects.

Implements `rx_machiery` class, that can receive byte after byte (defaultly from UART) and give as socketcan objects on the output.
