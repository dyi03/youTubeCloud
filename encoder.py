import binascii


def hexdump(file_content):
    # Convert bytes to a hex string
    # res = bytes(file_content, 'utf-8')

    hex_bytes = binascii.hexlify(file_content)
    return hex_bytes

# def padding(input_bytes):
#     # each frame has 1920*1080 bytes, 2073600 bytes. Bytes should be padded so that it matches the size or a multiple of it.
#     output_bytes =

def null_byte_padding(input_bytes, frame_size=2073600):
    # Determine the length of the input data
    input_length = len(input_bytes)

    # Calculate the number of bytes to add to make the input length a multiple of the frame size
    # If the input length is already a multiple of the frame size, no padding is needed.
    padding_needed = (frame_size - (input_length % frame_size)) % frame_size

    # Create a bytes object containing the padding
    # This uses the null byte ('\x00') for padding
    padding = b'00' * padding_needed

    # Append the padding to the input bytes and return
    output_bytes = input_bytes + padding
    return output_bytes


if __name__ == '__main__':
    f = open("test", "rb")
    input_text = f.read()

    hex_input = hexdump(input_text)
    print(hex_input)

    padded = null_byte_padding(hex_input)
    print(padded)
