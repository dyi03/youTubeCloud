import binascii
from PIL import Image


def hexdump(file_content):
    # Convert bytes to a hex string
    # res = bytes(file_content, 'utf-8')

    hex_bytes = binascii.hexlify(file_content)
    return hex_bytes


def null_byte_padding(input_bytes, frame_size=2073600):
    # each frame has 1920*1080 bytes, 2073600 bytes. Bytes should be padded
    # so that it matches the size or a multiple of it.
    input_length = len(input_bytes)
    padding_needed = (frame_size - (input_length % frame_size)) % frame_size

    padding = b'0' * padding_needed

    output_bytes = input_bytes + padding
    return output_bytes

def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def generate_image(binary_data, width=320, pixels_per_bit=10):
    height = ((len(binary_data) * pixels_per_bit) // width + 1) * pixels_per_bit
    img = Image.new('1', (width, height), "white")
    pixels = img.load()

    x, y = 0, 0
    for bit in binary_data:
        for px in range(pixels_per_bit):
            for py in range(pixels_per_bit):
                pixels[x * pixels_per_bit + px, y * pixels_per_bit + py] = int(bit)
        x += 1
        if x * pixels_per_bit >= width:
            x = 0
            y += 1

    return img

if __name__ == '__main__':
    f = open("test", "rb")
    input_text = f.read()

    hex_input = hexdump(input_text)
    print(hex_input)

    padded = null_byte_padding(hex_input)
    print(len(padded))


# 000 - black
# 111 - gray
# 222 - white
#
# 100 - burgundy red
# 010 - grass green
# 001 - deep blue
#
# 200 - red
# 020 - green
# 002 - blue
#
# 220 - yellow
# 202 - fuchsia purple
# 022 - cyan
#
# 210 - orange
# 021 - mint green
# 102 - purple
#
# 211 - coral