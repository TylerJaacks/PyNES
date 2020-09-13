# https://youtu.be/_1UMXx39Jxk?t=1145
class AddressingMixin(object):
    data_length = 0

    def get_instruction_length(self):
        return self.data_length + 1


class NoAddressingMixin(AddressingMixin):
    data_length = 0


class ImmediateAddressingMixin(AddressingMixin):
    data_length = 1

    def get_data(self, data_bytes: bytes):
        return data_bytes[0]
