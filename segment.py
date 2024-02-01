import os
import json
from math import inf
from pydub import AudioSegment

sample_name = 'short_short_podcast'
sample_path = './samples/' + sample_name + '.wav'

output_dir = './output/' + sample_name
transcription_path = os.path.join(output_dir, 'transcription.json')
wavs_dir = os.path.join(output_dir, 'wavs')

with open(transcription_path, 'r') as f:
    transcription = json.load(f)
segments = transcription['segments']

def concatenate_sentence_segments():
    ending_punctuation = {'.', '?', '!'}
    res = []
    combining_segment = None
    for i, sgmt in enumerate(segments):
        segment_text = sgmt['text'].strip()
        if i != len(segments) - 1 and segment_text[-1] not in ending_punctuation:
            if combining_segment is None:
                combining_segment = sgmt
            if combining_segment != sgmt:
                combining_segment['text'] += ' ' + segment_text
        else:
            if combining_segment is None:
                res.append(sgmt)
            else:
                combining_segment['end'] = sgmt['end']
                combining_segment['text'] += ' ' + segment_text
                res.append(combining_segment)
                combining_segment = None
    return res


segments = concatenate_sentence_segments()

audio = AudioSegment.from_file(sample_path)
metadata = []
durations = []
for i, segment in enumerate(segments):
    start = float(segment['start']) * 1000  # sec to ms
    end = segment['end'] * 1000  # sec to ms
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
