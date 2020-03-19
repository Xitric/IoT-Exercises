class Message:

    def __init__(self, time: float, value: float, delta: float):
        self.time = time
        self.value = value
        self.delta = delta

    def __str__(self):
        return 'Message[t={},v={},d={}]'.format(self.time, self.value, self.delta)


class MessageBuffer:

    def __init__(self, size: int):
        self.size = size
        self.stack: [Message] = []

    def push_message(self, time: float, value: float, delta: float):
        message = Message(time, value, delta)

        for index, msg in enumerate(self.stack):
            if msg.delta < delta:
                self.__shift_messages(index)
                self.stack[index] = message
                return

        if len(self.stack) < self.size:
            self.stack.append(message)

    def __shift_messages(self, from_index: int):
        for index in range(len(self.stack), from_index, -1):
            if index < self.size:
                self.__put(index, self.stack[index - 1])

    def __put(self, index: int, message: Message):
        if index >= self.size:
            raise IndexError('buffer index out of range')

        while len(self.stack) <= index:
            self.stack.append(None)

        self.stack[index] = message

    def extract_messages(self) -> [Message]:
        result = self.stack[:]
        result.sort(key=lambda msg: msg.time)
        self.stack.clear()
        return result
