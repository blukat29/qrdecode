
class QRCodec:
    @staticmethod
    def decode(ver, data):
        data = ''.join(data).replace('2','0')
        all_text = ""
        while True:
            if len(data) < 8:
                break
            mode = data[:4]
            if mode == "0010":
                text, data = AlnumCodec.decode(ver, data)
            elif mode == "0100":
                text, data = ByteCodec.decode(ver, data)
            elif mode == "0000":
                break
            else:
                break
            all_text += text
        return all_text

class AlnumCodec:

    _alnum_table = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"

    @staticmethod
    def decode(ver, data):

        # Check magic number
        assert(data[:4] == "0010")
        data = data[4:]

        # Get character count
        if ver <= 9: counter_size = 9
        elif ver <= 26: counter_size = 11
        else: counter_size = 13

        char_count = int(data[:counter_size], 2)
        data = data[counter_size:]

        # Gather characters
        text = ""
        while char_count >= 2:
            char_count -= 2
            n = int(data[:11], 2)
            data = data[11:]
            text += AlnumCodec._alnum_table[n // 45]
            text += AlnumCodec._alnum_table[n % 45]

        if char_count > 0:  # Last odd number'th character
            n = int(data[:6], 2)
            data = data[6:]
            text += AlnumCodec._alnum_table[n]

        return text, data


class ByteCodec:

    @staticmethod
    def decode(ver, data):

        # Check magic number
        assert(data[:4] == "0100")
        data = data[4:]

        # Get character count
        if ver <= 9: counter_size = 8
        else: counter_size = 16

        char_count = int(data[:counter_size], 2)
        data = data[counter_size:]

        # Gather characters
        text = ""
        for i in range(char_count):
            text += chr(int(data[:8], 2))
            data = data[8:]

        return text, data

