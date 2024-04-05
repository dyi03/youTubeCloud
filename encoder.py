import binascii


def hexdump(file_content):
    # Convert bytes to a hex string
    res = bytes(file_content, 'utf-8')

    hex_bytes = binascii.hexlify(res)
    return hex_bytes

# def padding(input_bytes):
#     # each frame has 1920*1080 bytes, 2073600 bytes. Bytes should be padded so that it matches the size or a multiple of it.
#     output_bytes =

def pkcs7_padding(input_bytes, block_size=2073600):
    # Calculate the number of padding bytes needed
    padding_needed = block_size - (len(input_bytes) % block_size)
    # If the length of the data is already a multiple of the block size, add a full block of padding
    if padding_needed == 0:
        padding_needed = block_size
    # Generate the padding bytes. Each padding byte is the same as the number of padding bytes needed.
    padding = bytes([padding_needed] * padding_needed)
    # Append the padding to the input bytes
    output_bytes = input_bytes + padding
    return output_bytes


if __name__ == '__main__':
    f = open("test", "r")
    input_text = f.read()

    hex_input = hexdump(input_text)
    # print(hex_input)

    padded = pkcs7_padding(hex_input)
    print(padded)
