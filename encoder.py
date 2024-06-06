import binascii
import shutil

from PIL import Image
import av
import glob
import os
import re

hex_to_color = {
    '0': (255, 255, 255),  # white
    '1': (128, 128, 128),  # gray
    '2': (0, 0, 0),  # black
    '3': (128, 0, 0),  # burgundy red
    '4': (0, 128, 0),  # grass green
    '5': (0, 0, 128),  # deep blue
    '6': (255, 0, 0),  # red
    '7': (0, 255, 0),  # green
    '8': (0, 0, 255),  # blue
    '9': (255, 255, 0),  # yellow
    'A': (255, 0, 255),  # fuchsia purple
    'B': (0, 255, 255),  # cyan
    'C': (255, 128, 0),  # orange
    'D': (0, 255, 128),  # mint green
    'E': (128, 0, 255),  # purple
    'F': (255, 128, 128),  # coral
}


def numerical_sort(value):
    """
    This helper function takes a string and returns a list of parts,
    with all digit parts turned into integers. This list can be used
    as a key for sorting.
    """
    parts = re.split(r'(\d+)', value)
    parts[1::2] = map(int, parts[1::2])  # Convert all digit strings to integers
    return parts


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


def generate_hex_images(tempDir, hex_data, width, height, gridsize):
    if os.path.exists(tempDir):
        shutil.rmtree(tempDir)  # Remove the folder and all its contents
    os.makedirs(tempDir)

    # Calculate the number of hex characters per image
    chars_per_image = (width * height) // (gridsize ** 2)  # Each character is represented by a 2x2 pixel grid

    # Split the hex data into chunks that fit into individual images
    chunks = [hex_data[i:i + chars_per_image] for i in range(0, len(hex_data), chars_per_image)]

    images = []  # This will store all the image objects

    for index, chunk in enumerate(chunks):
        img = Image.new('RGB', (width, height), "white")  # 'RGB' mode for color
        pixels = img.load()

        hex_string = chunk.decode('ascii')

        x, y = 0, 0
        for hex_char in hex_string:
            # Map the hex character to its color and set the pixel for a 2x2 grid
            color = hex_to_color.get(hex_char.upper(), (255, 255, 255))  # Default to white if not found

            # Set the color for the pixel grid
            for dx in range(gridsize):
                for dy in range(gridsize):
                    if x + dx < width and y + dy < height:
                        pixels[x + dx, y + dy] = color

            # Move to the next position for the next character
            x += gridsize
            if x >= width:
                x = 0
                y += gridsize
                if y >= height:
                    break  # Stop if y exceeds the height, to avoid IndexError

        # Save the image locally
        filename = f'{tempDir}/hex_image_{index}.png'
        img.save(filename)
        images.append(img)

    return images


def images_to_video(image_folder, output_file, frame_rate):
    """
    Create a video from a sequence of images.

    Args:
    image_folder (str): The path to the directory containing the images.
    output_file (str): The path for the output video file.
    frame_rate (int, optional): The frame rate of the output video. Default is 24.
    """
    # Sort files by name
    # images = sorted(glob.glob(f"{image_folder}/*.png"))
    images = sorted(glob.glob(f"{image_folder}/*.png"), key=numerical_sort)
    print(images)

    if not images:
        raise ValueError("No images found in the specified directory")

    # Open the first image to determine width and height for the video
    first_image = av.open(images[0])
    stream = first_image.streams.video[0]
    frame = next(first_image.decode(stream))

    # Create an output container and add a video stream
    container = av.open(output_file, "w")
    stream = container.add_stream('ffv1', rate=frame_rate)
    stream.width = frame.width
    stream.height = frame.height

    for img_path in images:
        img = av.open(img_path)
        for frame in img.decode(video=0):
            frame.pts = None  # Resetting PTS might not be necessary if you calculate it correctly.

            # Encode the frame to a packet
            for packet in stream.encode(frame):
                container.mux(packet)  # Mux the packet into the container

    container.close()