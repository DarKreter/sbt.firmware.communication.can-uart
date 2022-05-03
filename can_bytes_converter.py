import can
import crc16


def id_payload_to_bytes(extID: int, payload: bytes) -> bytes:
    byt_id = extID.to_bytes(4, 'little')
    byt_data = payload
    byt_inside_for_crc = byt_id + payload
    byt_crc = crc16.crc16xmodem(byt_inside_for_crc).to_bytes(2, 'little')

    byt_inside = bytearray()
    for byte in byt_id:
        if byte == ord('x') or byte == ord('y') or byte == ord('\\'):
            byt_inside.append(ord('\\'))
        byt_inside.append(byte)
    for byte in byt_data:
        if byte == ord('x') or byte == ord('y') or byte == ord('\\'):
            byt_inside.append(ord('\\'))
        byt_inside.append(byte)

    byt_out = b"xxx" + byt_inside + byt_crc + b"yyy"
    return byt_out


# def can_frame_to_bytes(frame_can: can.Message) -> bytes:
#     return id_payload_to_bytes(frame_can.arbitration_id, frame_can.data)


def bytes_to_id_payload(frame_bytes: bytes):
    # check header
    if frame_bytes[0:3] != b'xxx':
        raise ValueError("invalid start")

    # check footer
    if frame_bytes[-3:] != b'yyy':
        raise ValueError("invalid end")

    # cut start and end
    frame_bytes = frame_bytes[3:-3]

    # Get CRC from received frame
    rx_crc = int.from_bytes(frame_bytes[-2:], 'little')
    # cut crc part from frame
    frame_bytes = frame_bytes[:-2]

    # cut escape bytes
    frame_content = bytearray()
    escape_byte = False
    # Go through all bytes in payload
    for byte in frame_bytes:
        # If previous byte was not escape byte and current one is equal to '\'
        # we mark escape byte flag and dont add byte to frame_content
        if byte == ord('\\') and escape_byte == False:
            escape_byte = True

        # If previous byte was escape byte
        elif escape_byte == True:
            # Only x, y or \ is preceded by escape byt
            if byte != ord('x') and byte != ord('y') and byte != ord('\\'):
                raise ValueError("Escape byte before not x, y nor \\")
            # Clear flag
            escape_byte = False
            # Add byte to frame_content
            frame_content.append(byte)
        # previous and current byte was not escape byte so we just append
        else:
            frame_content.append(byte)

    # Calc CRC from frame
    content_crc = crc16.crc16xmodem(bytes(frame_content))
    if content_crc != rx_crc:
        raise ValueError("invalid CRC")

    # Get data and ID
    rx_data = frame_content[4:]
    rx_id = int.from_bytes(frame_content[:4], 'little')

    return rx_id, rx_data


# def bytes_to_can_frame(frame_bytes: bytes) -> can.Message:
#     rx_id, rx_data = bytes_to_id_payload(frame_bytes)

#     return can.Message(arbitration_id=rx_id, data=rx_data)
