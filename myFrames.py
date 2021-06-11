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


# r = bytes_to_can_frame(b'xxxxxx#\x01\x00\x00\x024V\xd6nyyyyyy')


class rx_machiery:
    def __init__(self, on_rx):
        self.on_rx = on_rx
        self._reset()

    def _reset(self):
        self.start_counter = 0
        self.end_counter = 0
        self.frame = bytearray()
        self.is_start = False

    def _append_byte(self, rx_byte):
        self.frame.append(rx_byte)

    def _whole_frame(self):
        if self.on_rx is not None:
            try:
                frame = bytes_to_can_frame(bytes(self.frame))
            except ValueError as e:
                print("ERROR!!!")
                print(e)
                return
            self.on_rx(frame)

    def start_end_rx(self, frame_bytes: bytes):
        pass

    def _put_byte(self, rx_byte: int):
        # print(rx_byte)
        # look for starting combination
        if rx_byte == ord('x'):
            self.start_counter += 1
            # print("start: {}".format(self.start_counter))
            if self.start_counter == 6:
                self._reset()
                self.is_start = True
                for i in range(6):
                    self._append_byte(ord('x'))
            return
        self.start_counter = 0

        if self.is_start is False:
            return

        self._append_byte(rx_byte)

        if rx_byte == ord('y'):
            self.end_counter += 1
            if self.end_counter == 6:
                self._whole_frame()
                self._reset()
            return

        self.end_counter = 0

    def put_data(self, rx_data):
        if type(rx_data) == int:
            self._put_byte(rx_data)
        else:
            for b in rx_data:
                self._put_byte(b)


def test():
    def my_on_rx(frame: can.Message):
        print("WYSOKO")
        print(frame)

    m = rx_machiery(my_on_rx)
    m.put_data(b'aaaxxxxxx#\x01\x00\x00\x024V\xd6nyyyyyyqqq')
    heh = b'xxxxxx#\x01\x00\x00\x024V\xd6nyyyyyyxxxxxx#\x00\x00\x00\x02Egl6yyyyyy'
    m.put_data(heh)


if __name__ == '__main__':
    test()
