import machine
import os

# SD Card Pins
SD_MMC_CMD = 15
SD_MMC_CLK = 14
SD_MMC_D0 = 2

# I2S Pins
I2S_BCLK = 26
I2S_DOUT = 22
I2S_LRC = 25

def mount_sd_card():
    try:
        sd = machine.SDCard(slot=1)
        os.mount(sd, '/sd')
        print("SD card mounted.")
    except OSError as e:
        if e.args[0] == -259:  # ESP_ERR_INVALID_STATE
            try:
                # Check if '/sd' is accessible
                os.listdir('/sd')
                print("SD card is already mounted.")
            except OSError:
                # If '/sd' is not accessible, there's a state issue
                print("SD card is in an invalid state. Please check the card and connections.")
        else:
            raise

def parse_wav_header(file_path):
    with open(file_path, 'rb') as wav_file:
        # Read the first 44 bytes (standard WAV header size)
        header = wav_file.read(44)

        # Unpack header using struct (if available) or manually
        # Here's a manual approach:
        if header[0:4] != b'RIFF' or header[8:12] != b'WAVE':
            raise ValueError("This is not a valid WAV file.")

        # Parse necessary fields
        audio_format = int.from_bytes(header[20:22], 'little')  # Should be 1 for PCM
        num_channels = int.from_bytes(header[22:24], 'little')
        sample_rate = int.from_bytes(header[24:28], 'little')
        byte_rate = int.from_bytes(header[28:32], 'little')
        block_align = int.from_bytes(header[32:34], 'little')
        bits_per_sample = int.from_bytes(header[34:36], 'little')

        return {
            "Audio Format": audio_format,
            "Number of Channels": num_channels,
            "Sample Rate": sample_rate,
            "Byte Rate": byte_rate,
            "Block Align": block_align,
            "Bits per Sample": bits_per_sample
        }
# Initialize the I2S interface
i2s = machine.I2S(0, 
                  sck=machine.Pin(I2S_BCLK), 
                  ws=machine.Pin(I2S_LRC), 
                  sd=machine.Pin(I2S_DOUT),
                  mode=machine.I2S.TX, 
                  bits=16, 
                  format=machine.I2S.STEREO, 
                  rate=48000,
                  ibuf=2048)

# Function to play WAV file
def play_wav(file_path):
    with open(file_path, 'rb') as wav_file:
        # Skip the WAV header (44 bytes)
        wav_file.seek(44) 

        # Play audio
        chunk_size = 1024
        data = wav_file.read(chunk_size)
        while data:
            i2s.write(data)
            data = wav_file.read(chunk_size)

'''
wav_file_path = '/sd/Test2.wav'
# Parse and print WAV header information
wav_info = parse_wav_header(wav_file_path)
for key, value in wav_info.items():
    print(f"{key}: {value}")
'''

print("start play ... \n\n")

mount_sd_card()
wav_file_path = '/sd/Test2.wav'
play_wav(wav_file_path)

