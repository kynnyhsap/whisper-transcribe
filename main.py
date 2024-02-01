import json
import whisper
import warnings
import os

# Suppress all warnings
warnings.filterwarnings("ignore")


sample_name = 'short_podcast'

transcriptions_dir = './transcriptions'

sample_path = './samples/' + sample_name + '.wav'
output_path = transcriptions_dir + '/' + sample_name + '.json'

os.makedirs(transcriptions_dir, exist_ok=True)

model_name = "medium.en"

model = whisper.load_model(model_name)
print("Loaded whisper model: " + model_name)

print("Other available models", whisper.available_models())

print("Transcribing audio: " + sample_path)
result = model.transcribe(sample_path)
with open(output_path, 'w') as outfile:
        json.dump(result, outfile, indent=4)
print("Transcription saved to: " + output_path)