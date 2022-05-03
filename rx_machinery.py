from can_bytes_converter import *


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
            id, payload = bytes_to_id_payload(bytes(self.frame))
            # except ValueError as e:
            #     print("ERROR!!!")
            #     print(e)
            #     Raise e
            #     return
            self.on_rx(id, payload)

    def _put_byte(self, rx_byte: int):
        # If last one was not escape byte and current is from start sentence do this
        # print("{} ".format(rx_byte), end='')
        if rx_byte == ord('x') and self.escape_byte_encounter == False:
            self.is_start = False
            self.start_counter += 1

            if self.start_counter == 3:
                self._reset()
                self.is_start = True
                for i in range(3):
                    self._append_byte(ord('x'))
            return
        self.start_counter = 0
        # print(rx_byte)
        # Wait till header sentence
        if self.is_start is False:
            print("A")
            return

        if self.escape_byte_encounter == True:
            if rx_byte != ord('\\') and rx_byte != ord('x') and rx_byte != ord('y'):
                # escape byte before unexpected byte
                self._reset()
                return
            self.escape_byte_encounter = False
           
        # Escape byte detected
        elif rx_byte == ord('\\') and self.escape_byte_encounter == False:
            self.escape_byte_encounter = True


        self._append_byte(rx_byte)

        if rx_byte == ord('y'):
            self.end_counter += 1
            if self.end_counter == 3:
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
