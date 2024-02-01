import json
import os
import warnings

import whisper

# Suppress all warnings
warnings.filterwarnings("ignore")

sample_name = 'short_short_podcast'
sample_path = './samples/' + sample_name + '.wav'

output_dir = './output/' + sample_name

model_name = "medium.en"

# Load the Whisper model
model = whisper.load_model(model_name)
print("loaded whisper " + model_name)

# Other available models
print("other available models", whisper.available_models())

result = model.transcribe(sample_path, verbose=True)

os.makedirs(output_dir, exist_ok=True)
with open(os.path.join(output_dir, 'transcription.json'), 'w') as f:
    json.dump(result, f, indent=4)
