from can_bytes_converter import *
import can


class rx_machinery:
    def __init__(self, on_rx):
        self.on_rx = on_rx
        self._reset()

    def _reset(self):
        self.start_counter = 0
        self.end_counter = 0
        self.frame = bytearray()
        self.is_start = False
        self.escape_byte_encounter = False

    def _append_byte(self, rx_byte):
        self.frame.append(rx_byte)

    def _whole_frame(self):
        if self.on_rx is not None:
            # try:
            frame = bytes_to_can_frame(bytes(self.frame))
            # except ValueError as e:
            #     print("ERROR!!!")
            #     print(e)
            #     Raise e
            #     return
            self.on_rx(frame)

    def _put_byte(self, rx_byte: int):
        # If last one was not escape byte and current is from start sentence do this
        # print("{} ".format(rx_byte), end='')
        if rx_byte == ord(start_byte) and self.escape_byte_encounter == False:
            self.is_start = False
            self.start_counter += 1

            if self.start_counter == start_sequence_length:
                self._reset()
                self.is_start = True
                for i in range(start_sequence_length):
                    self._append_byte(ord(start_byte))
            return
        self.start_counter = 0
        # print(rx_byte)
        # Wait till header sentence
        if self.is_start is False:
            return

        if self.escape_byte_encounter == True:
            if rx_byte != ord(escape_byte) and rx_byte != ord(start_byte) and rx_byte != ord(end_byte):
                # escape byte before unexpected byte
                self._reset()
                return
            self.escape_byte_encounter = False
           
        # Escape byte detected
        elif rx_byte == ord(escape_byte) and self.escape_byte_encounter == False:
            self.escape_byte_encounter = True


        self._append_byte(rx_byte)

        if rx_byte == ord(escape_byte):
            self.end_counter += 1
            if self.end_counter == end_sequence_length:
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
