
from can_bytes_converter import *

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
        if rx_byte == ord('x') and self.is_start is False:
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
