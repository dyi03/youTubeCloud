import encoder
import decoder

import shutil

# setup
encoderTempDir = "encoderTemp"
decoderTempDir = "decodertemp"

encoderSource = "books/bible.txt"
encoderOutput = "output.AVI"

decoderSource = "4x4 720p30fps.mp4"
decoderOutput = "output_ascii.txt"

width = 1280
height = 720
gridsize = 4


def encoderHelper():
    # encoder
    f = open(encoderSource, "rb")
    input_text = f.read()
    hex_input = decoder.hexdump(input_text)
    encoder.generate_hex_images(encoderTempDir, hex_input, width, height, gridsize)
    encoder.images_to_video(encoderTempDir, encoderOutput)


def decoderHelper():
    decoder.extract_frames(decoderSource, decoderTempDir)
    hex_data = decoder.extract_hex_from_images(decoderTempDir, gridsize)
    decoder.hex_to_ascii(hex_data, decoderOutput)


if __name__ == '__main__':
    # encoder
    encoderHelper()

    # decoder
    decoderHelper()
