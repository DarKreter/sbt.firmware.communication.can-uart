import can

from myFrames import can_frame_to_bytes


class can_buffer:
    def __init__(self):
        self.storage = dict()
        pass

    def clean(self):
        self.storage.clear()

    def storage_to_serialized_data(self) -> bytearray:
        b = bytearray()
        for frame in self.storage.values():
            frame_bytes = can_frame_to_bytes(frame)
            b += bytearray(frame_bytes)
        return b

    def append_frame(self, msg: can.Message): 
        if msg.arbitration_id > 0x10:
            self.storage[msg.arbitration_id] = msg
        else:
            self.storage[msg.data[2]] = msg
        