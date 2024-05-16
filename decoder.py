import binascii
import shutil

from PIL import Image
import av
import glob
import os

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

color_to_hex = {v: k for k, v in hex_to_color.items()}


def hexdump(file_content):
    # Convert bytes to a hex string
    # res = bytes(file_content, 'utf-8')

    hex_bytes = binascii.hexlify(file_content)
    return hex_bytes


def extract_frames(video_path, image_folder):
    """
    Extracts frames from a video file and saves them as images.
    """
    # Open the video file
    container = av.open(video_path)

    if os.path.exists(image_folder):
        shutil.rmtree(image_folder)  # Remove the folder and all its contents
    os.makedirs(image_folder)

    # Loop through the frames in the video
    for frame in container.decode(video=0):
        # Check if the frame is a video frame
        if isinstance(frame, av.VideoFrame):
            # Convert frame to an image
            img = frame.to_image()

            # Create an image file name
            img_filename = os.path.join(image_folder, f"{frame.index:04d}.png")

            # Save the image
            img.save(img_filename)

    print("Frame extraction complete!")


def closest_color(target_color, color_map):
    min_distance = float('inf')
    closest_hex = ''
    for color, hex_char in color_map.items():
        # Calculate Euclidean distance between target color and each color in the map
        distance = sum((tc - c) ** 2 for tc, c in zip(target_color, color))
        if distance < min_distance:
            min_distance = distance
            closest_hex = hex_char
    return closest_hex


def extract_hex_from_images(image_folder, gridsize):
    hex_data = ""
    files = sorted(os.listdir(image_folder))  # Ensure files are processed in order

    for file in files:
        if file.endswith('.png'):
            img_path = os.path.join(image_folder, file)
            img = Image.open(img_path)
            pixels = img.load()
            width, height = img.size

            y = 0
            while y < height:
                x = 0
                while x < width:

                    # Collect colors from a 2x2 pixel grid
                    colors = []
                    for dy in range(gridsize):
                        for dx in range(gridsize):
                            if x + dx < width and y + dy < height:  # Ensure we don't go out of bounds
                                colors.append(pixels[x + dx, y + dy])

                    # Average the RGB values
                    if colors:
                        average_color = tuple(sum(c) // len(c) for c in zip(*colors))
                        hex_char = closest_color(average_color, color_to_hex)
                        hex_data += hex_char

                    x += gridsize
                y += gridsize

    return hex_data


def hex_to_ascii(hex_string, output):
    ascii_string = ""

    for i in range(0, len(hex_string), 2):  # Process two characters at a time
        hex_value = hex_string[i:i + 2]  # Get two characters from the hex string
        # if not hex_value:  # Check if hex_value is empty, stop if it is
        #     break
        char_code = int(hex_value, 16)  # Convert from hex to an integer
        # # if char_code < 32 or char_code > 126:  # ASCII printable characters range from 32 to 126
        # # break  # Stop converting if a non-printable character is encountered
        ascii_char = chr(char_code)  # Convert integer to the ASCII char
        ascii_string += ascii_char

    with open(output, 'w') as file:
        file.write(ascii_string)