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

    # Here we have storage mechanism that storages unique frames. As
    # we have been using the same arbitration_id for unique frames (eg. sending
    # cell voltages over can with the same arbitration_id, but with unique
    # param_id: data[2]) we check if arbitration_id is higher than 0x10. frames
    # with arbitration_id <= 0x10 support param_id. We can refactor this as:
    # self.storage[msg.arbitration_id] = msg
    # after we will get rid of param_id approach.
    def append_frame(self, msg: can.Message) -> None:
        if msg.arbitration_id > 0x10:
            self.storage[msg.arbitration_id] = msg
        else:
            self.storage[msg.data[2]] = msg
