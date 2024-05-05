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


def decode_hex_images(image_folder):
    hex_data = ""

    # Loop through each image file
    for filename in sorted(os.listdir(image_folder)):  # Ensure files are processed in order
        if filename.endswith('.png'):
            img_path = os.path.join(image_folder, filename)
            img = Image.open(img_path)
            pixels = img.load()

            width, height = img.size

            # Read each pixel and convert it back to hex character
            for y in range(0, height, 2):
                for x in range(0, width, 2):
                    color = pixels[x, y]
                    hex_char = closest_color(color, color_to_hex)  # Find the closest color match
                    hex_data += hex_char

    return hex_data


def decode_hex_images_to_ascii_file(image_folder, output_file_path, color_to_hex):
    with open(output_file_path, 'w') as file:  # Open the file in write mode from the start
        # Process each image file in order
        for filename in sorted(os.listdir(image_folder)):
            if filename.endswith('.png'):
                img_path = os.path.join(image_folder, filename)
                img = Image.open(img_path)
                pixels = img.load()
                width, height = img.size

                # Read each pixel, find its closest hex representation
                byte_builder = ""
                for y in range(height):
                    for x in range(width):
                        color = pixels[x, y]
                        hex_char = closest_color(color, color_to_hex)
                        byte_builder += hex_char  # Build the byte from two hex characters
                        if len(byte_builder) == 2:  # Check if we have a complete byte
                            if byte_builder == '00':  # Stop if the whole null byte is encountered
                                print("Whole null byte encountered, stopping decoding.")
                                return  # Return to stop processing further
                            # Convert hex byte to ASCII character
                            try:
                                ascii_char = bytes.fromhex(byte_builder).decode('utf-8', 'ignore')
                                file.write(ascii_char)  # Write the ASCII character to file
                            except ValueError as e:
                                print("Failed to convert hex to ASCII:", e)
                            byte_builder = ""  # Reset byte builder for next byte


if __name__ == '__main__':
    image_folder = 'decodertemp'  # Folder containing images
    video = "output.AVI"
    output = "output_ascii.txt"
    extract_frames(video, image_folder)

    # output_file_path = 'decoded_hex_data.txt'  # File to write the decoded hex data
    decode_hex_images_to_ascii_file(image_folder, output, color_to_hex)

    # shutil.rmtree(image_folder)

    # print("Hex data has been written to:", output_file_path)

    # f = open("output.AVI", "rb")
    # input_text = f.read()
    #
    # hex_input = hexdump(input_text)
    # print(hex_input)

    # padded = null_byte_padding(hex_input)
    # print(len(padded))

    # generate_hex_images(hex_input)

    # images_to_video("output", "output.AVI")
