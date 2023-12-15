import machine
import os

# I2S Pins
I2S_BCLK = 26
I2S_DOUT = 22
I2S_LRC = 25
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


print("start play ... \n\n")
wav_file_path = '/test5s.wav'
play_wav(wav_file_path)
