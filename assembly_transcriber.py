import assemblyai as aai
import json
import os
from assemblyai import TranscriptionConfig

sample_name = 't1F7EEGPQwo'
sample_path = './samples/' + sample_name + '.wav'

output_dir = './output/' + sample_name

aai.settings.api_key = ""
transcriber = aai.Transcriber()

config = TranscriptionConfig(punctuate=True, content_safety=False)
transcription = transcriber.transcribe(sample_path, config=config)
sentences = transcription.get_sentences()

json_sentences = []
for sentence in sentences:
    json_sentence = {
        'start': sentence.start,
        'end': sentence.end,
        'text': sentence.text
    }
    json_sentences.append(json_sentence)

os.makedirs(output_dir, exist_ok=True)
with open(os.path.join(output_dir, 'transcription.json'), 'w') as f:
    json.dump(json_sentences, f, indent=4)