import binascii
from PIL import Image

hex_to_color = {
    '0': (255, 255, 255),   # white
    '1': (128, 128, 128),   # gray
    '2': (0, 0, 0),         # black
    '3': (128, 0, 0),       # burgundy red
    '4': (0, 128, 0),       # grass green
    '5': (0, 0, 128),       # deep blue
    '6': (255, 0, 0),       # red
    '7': (0, 255, 0),       # green
    '8': (0, 0, 255),       # blue
    '9': (255, 255, 0),     # yellow
    'A': (255, 0, 255),     # fuchsia purple
    'B': (0, 255, 255),     # cyan
    'C': (255, 128, 0),     # orange
    'D': (0, 255, 128),     # mint green
    'E': (128, 0, 255),     # purple
    'F': (255, 128, 128),   # coral
}
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


# def generate_image(binary_data, width=320, pixels_per_bit=10):
#     height = ((len(binary_data) * pixels_per_bit) // width + 1) * pixels_per_bit
#     img = Image.new('1', (width, height), "white")
#     pixels = img.load()
#
#     x, y = 0, 0
#     for bit in binary_data:
#         for px in range(pixels_per_bit):
#             for py in range(pixels_per_bit):
#                 pixels[x * pixels_per_bit + px, y * pixels_per_bit + py] = int(bit)
#         x += 1
#         if x * pixels_per_bit >= width:
#             x = 0
#             y += 1
#
#     return img

# def generate_hex_images(hex_data, width=1920, height=1080):
#     # Calculate the number of hex characters per image
#     chars_per_image = width * height
#
#     # Split the hex data into chunks that fit into individual images
#     chunks = [hex_data[i:i + chars_per_image] for i in range(0, len(hex_data), chars_per_image)]
#
#     images = []  # This will store all the image objects
#
#     for chunk in chunks:
#
#         img = Image.new('RGB', (width, height), "white")  # 'RGB' mode for color
#         pixels = img.load()
#
#         hex_string = chunk.decode('ascii')
#         x, y = 0, 0
#         for hex_char in hex_string:
#             # Map the hex character to its color and set the pixel
#             pixels[x, y] = hex_to_color.get(hex_char.upper(), (0, 0, 0))  # Default to black if not found
#             x += 1
#             if x >= width:
#                 x = 0
#                 y += 1
#
#             # Save the image locally
#             filename = f'hex_image_{index}.png'
#             img.save(filename)
#             images.append(img)
#
#     return images

def generate_hex_images(hex_data, width=1920, height=1080):
    # Calculate the number of hex characters per image
    chars_per_image = width * height

    # Split the hex data into chunks that fit into individual images
    chunks = [hex_data[i:i + chars_per_image] for i in range(0, len(hex_data), chars_per_image)]

    images = []  # This will store all the image objects

    for index, chunk in enumerate(chunks):
        img = Image.new('RGB', (width, height), "white")  # 'RGB' mode for color
        pixels = img.load()

        hex_string = chunk.decode('ascii')

        x, y = 0, 0
        for hex_char in hex_string:
            # Map the hex character to its color and set the pixel
            color = hex_to_color.get(hex_char.upper(), (255, 255, 255)) # Default to black if not found
            pixels[x, y] = color
            x += 1
            if x >= width:
                x = 0
                y += 1

        # Save the image locally
        filename = f'hex_image_{index}.png'
        img.save(filename)
        images.append(img)

    return images



if __name__ == '__main__':
    f = open("books/bible.txt", "rb")
    input_text = f.read()

    hex_input = hexdump(input_text)
    # print(hex_input)

    # padded = null_byte_padding(hex_input)
    # print(len(padded))

    x = generate_hex_images(hex_input)

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
