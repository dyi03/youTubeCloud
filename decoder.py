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



def extract_frames(video_path, output_folder):
    # Create the output folder if it doesn't exist
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)  # Remove the folder and all its contents
    os.makedirs(output_folder)

    # Open the video file
    container = av.open(video_path)

    # Iterate through frames in the video
    for i, frame in enumerate(container.decode()):
        # Convert the frame to PIL image
        img = frame.to_image()
        # Save the image file
        img.save(os.path.join(output_folder, f'{i}.png'))
        print(f"Extracted frame {i}")

    print("All frames extracted.")


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


# def decode_hex_images(image_folder):
#     hex_data = ""
#
#     # Loop through each image file
#     for filename in sorted(os.listdir(image_folder)):  # Ensure files are processed in order
#         if filename.endswith('.png'):
#             img_path = os.path.join(image_folder, filename)
#             img = Image.open(img_path)
#             pixels = img.load()
#
#             width, height = img.size
#
#             # Read each pixel and convert it back to hex character
#             for y in range(0, height, 2):
#                 for x in range(0, width, 2):
#                     color = pixels[x, y]
#                     hex_char = closest_color(color, color_to_hex)  # Find the closest color match
#                     hex_data += hex_char
#
#     return hex_data


def extract_hex_from_images(image_folder):
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
                    # Assuming the color of the pixel can be converted back to a hex character
                    color = pixels[x, y]  # Get the pixel color at the top-left of each 2x2 grid
                    hex_char = closest_color(color, color_to_hex)
                    # hex_char = color_to_hex.get(color, 'F')  # Convert color back to hex, default to 'F'
                    hex_data += hex_char
                    x += 2
                y += 2

    return hex_data


def hex_to_ascii(hex_string, output):
    ascii_string = ""
    for i in range(0, len(hex_string), 2):  # Process two characters at a time
        hex_value = hex_string[i:i+2]  # Get two characters from the hex string
        if not hex_value:  # Check if hex_value is empty, stop if it is
            break
        char_code = int(hex_value, 16)  # Convert from hex to an integer
        if char_code < 32 or char_code > 126:  # ASCII printable characters range from 32 to 126
            break  # Stop converting if a non-printable character is encountered
        ascii_char = chr(char_code)  # Convert integer to the ASCII char
        ascii_string += ascii_char

    with open(output, 'w') as file:
        file.write(ascii_string)


if __name__ == '__main__':
    image_folder = 'decodertemp'  # Folder containing images
    video = "output.AVI"
    output = "output_ascii.txt"
    extract_frames(video, image_folder)

    hex_data = extract_hex_from_images(image_folder)

    hex_to_ascii(hex_data, output)

    shutil.rmtree(image_folder)
