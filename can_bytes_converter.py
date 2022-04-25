import can
import crc16


def can_frame_to_bytes(frame_can: can.Message) -> bytes:
    # print("START/{id}/{len}/{data}/END".format(id=frame.arbitration_id, len=len(frame.data), data=1))
    byt_id = frame_can.arbitration_id.to_bytes(4, 'little')
    byt_len = len(frame_can.data).to_bytes(1, 'little')
    byt_data = frame_can.data
    byt_inside = byt_id + byt_len + byt_data
    byt_crc = crc16.crc16xmodem(byt_inside).to_bytes(2, 'little')
    byt_out = b"xxxxxx" + byt_inside + byt_crc + b"yyyyyy"
    return byt_out


def bytes_to_can_frame(frame_bytes: bytes) -> can.Message:
    if frame_bytes[0:6] != b'xxxxxx':
        raise ValueError("invalid start")

    if frame_bytes[-6:] != b'yyyyyy':
        raise ValueError("invalid end")

    # cut start and end
    frame_bytes = frame_bytes[6:-6]

    # CRC
    rx_crc = int.from_bytes(frame_bytes[-2:], 'little')
    # cut crc part
    frame_bytes = frame_bytes[:-2]
    content_crc = crc16.crc16xmodem(frame_bytes)
    if content_crc != rx_crc:
        raise ValueError("invalid CRC")

    rx_len = frame_bytes[4]
    rx_data = frame_bytes[5:]
    if rx_len != len(rx_data):
        raise ValueError("len mismatch")

    rx_id = int.from_bytes(frame_bytes[:4], 'little')

    msg = can.Message(arbitration_id=rx_id, data=rx_data)
    return msg
