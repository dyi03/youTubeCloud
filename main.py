import encoder
import decoder
import accuracy

import shutil

# setup
width = 1920
height = 1080
framerate = 30
gridsize = 8

encoderTempDir = "encoderTemp"
decoderTempDir = "decodertemp"

encoderSource = "books/bible.txt"
encoderOutput = f"{height}p{framerate}fps{gridsize}x{gridsize}.AVI"

decoderSource = "1080p30fps8x8 [-P6Dh_KondY].mp4"
decoderOutput = "1080p30fps8x8.txt"


def encoderHelper():
    # encoder
    f = open(encoderSource, "rb")
    input_text = f.read()
    hex_input = encoder.hexdump(input_text)
    encoder.generate_hex_images(encoderTempDir, hex_input, width, height, gridsize)
    encoder.images_to_video(encoderTempDir, encoderOutput, framerate)


def decoderHelper():
    decoder.extract_frames(decoderSource, decoderTempDir)
    decoder.find_and_remove_duplicate_frames(decoderTempDir)
    hex_data = decoder.extract_hex_from_images(decoderTempDir, gridsize)
    decoder.hex_to_ascii(hex_data, decoderOutput)


if __name__ == '__main__':
    # encoder
    # encoderHelper()

    # decoder
    decoderHelper()

    # Accuracy
    # source_file_path = "books/bible.txt"
    # accuracy.compare_files(source_file_path, '1080p30fps2x2.txt')
    # accuracy.compare_files(source_file_path, '1080p30fps4x4.txt')
    # accuracy.compare_files(source_file_path, '1080p30fps8x8.txt')
