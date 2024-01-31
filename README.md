# Wisper transcriptions

transcribe long audio files with wisper model

## How to run

1. Intall the wisper model `pip install pip install git+https://github.com/openai/whisper.git`
2. Put your audio file into `./samlples` folder. Change `sample_name` variable in `main.py` script to match your file.
3. Run `python main.py`, this will create chunks of audio then transcribe them.
   > First time the model will be loading locally and it will take some time
