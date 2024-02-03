import os
import json
from math import inf
from pydub import AudioSegment

sample_name = '2XGREPnlI8U'
sample_path = './samples/' + sample_name + '.wav'

output_dir = './output/' + sample_name
transcription_path = os.path.join(output_dir, 'transcription.json')
wavs_dir = os.path.join(output_dir, 'wavs')

with open(transcription_path, 'r') as f:
    segments = json.load(f)

audio = AudioSegment.from_file(sample_path)
metadata = []
durations = []
for i, segment in enumerate(segments):
    start = float(segment['start'])
    end = segment['end']
    audio_segment = audio[start:end]

    duration = (end - start) / 1000  # ms to sec
    durations.append(duration)

    os.makedirs(wavs_dir, exist_ok=True)
    segment_name = f"{i}.wav"
    segment_path = os.path.join(wavs_dir, segment_name)
    audio_segment.export(segment_path, format='wav')

    metadata.append(f"{segment_name}|{segment['text'].strip()}")

with open(os.path.join(output_dir, 'metadata.csv'), 'w') as f:
    f.write('\n'.join(metadata))

print(f"Min Clip Duration {min(durations)}")
print(f"Max Clip Duration {max(durations)}")
print(f"Mean Clip Duration {sum(durations) / len(durations)}")