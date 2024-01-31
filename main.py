import os
import json
import whisper
import time
import warnings
from pydub import AudioSegment

# Suppress all warnings
warnings.filterwarnings("ignore")

sample_name = 'podcast'
sample_path = './samples/' + sample_name + '.wav'

# Load the Whisper model
model = whisper.load_model("large-v3")

# Extract the base filename without extension
base_filename = os.path.splitext(os.path.basename(sample_path))[0]

# Directory containing chunks of audio
chunks_dir = os.path.join('./chunks', base_filename)
# Directory for saving transcriptions as JSON files
transcriptions_dir = os.path.join('./transcriptions', base_filename)

def chunk_audio(file_path, chunk_length_ms=30000):
    audio = AudioSegment.from_file(file_path)
    os.makedirs(chunks_dir, exist_ok=True)
    num_chunks = len(audio) // chunk_length_ms + 1

    print(f"Splitting '{base_filename}' into {num_chunks} chunks...")

    for i in range(num_chunks):
        start_ms = i * chunk_length_ms
        end_ms = start_ms + chunk_length_ms
        chunk = audio[start_ms:end_ms]
        chunk_file = os.path.join(chunks_dir, f'{i}.wav')
        chunk.export(chunk_file, format='wav')
        print(f"Chunk {i}/{num_chunks} exported.")

chunk_audio(sample_path)

os.makedirs(transcriptions_dir, exist_ok=True)

def transcribe_and_save(chunk_path, output_path, model):
    start_time = time.time()
    print(f"Transcribing: {os.path.basename(chunk_path)}")
    result = model.transcribe(chunk_path)
    transcription_time = time.time() - start_time
    with open(output_path, 'w') as outfile:
        json.dump(result, outfile, indent=4)
    print(f"Transcription saved: {os.path.basename(output_path)}")
    return transcription_time

chunk_files = sorted(os.listdir(chunks_dir), key=lambda x: int(os.path.splitext(x)[0]))

total_transcription_time = 0
for i, filename in enumerate(chunk_files):
    chunk_path = os.path.join(chunks_dir, filename)
    transcription_filename = os.path.splitext(filename)[0] + '.json'
    transcription_path = os.path.join(transcriptions_dir, transcription_filename)

    transcription_time = transcribe_and_save(chunk_path, transcription_path, model)
    total_transcription_time += transcription_time

    estimated_time_remaining = transcription_time * (len(chunk_files) - i - 1)
    print(f"Chunk {i+1}/{len(chunk_files)} transcribed in {transcription_time:.2f} seconds.")
    print(f"Estimated time remaining: {estimated_time_remaining:.2f} seconds.")

print(f"Total transcription time: {total_transcription_time:.2f} seconds.")
