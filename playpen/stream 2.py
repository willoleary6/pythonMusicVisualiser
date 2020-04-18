import pyaudio

BUFFER_SIZE = 4096
DURATION = 15
SAMPLE_RATE = 44100

p = pyaudio.PyAudio()

input_stream = p.open(
    format=pyaudio.paInt16,
    channels=2,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=BUFFER_SIZE,
    input_device_index=1
    )

output_stream = p.open(
    format=pyaudio.paInt16,
    channels=2,
    rate=SAMPLE_RATE,
    output=True
    )

for i in range(int(SAMPLE_RATE / BUFFER_SIZE * DURATION)):
    data = input_stream.read(BUFFER_SIZE)
    output_stream.write(data)

input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()
p.terminate()