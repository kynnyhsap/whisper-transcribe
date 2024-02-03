import os
import random
import shutil

output_dir = './output/'

metadata = []
for d in os.listdir(output_dir):
    metadata_path = os.path.join(output_dir, d, "metadata.csv")
    with open(metadata_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            metadata.append(f"{d}|{line.strip()}")

random.shuffle(metadata)

dataset_dir = './dataset/'
wavs_dir = os.path.join(dataset_dir, 'wavs')

os.makedirs(dataset_dir, exist_ok=True)
os.makedirs(wavs_dir, exist_ok=True)

for i, line in enumerate(metadata):
    d, f, _ = line.split('|')
    shutil.copy(os.path.join(output_dir, d, "wavs", f), os.path.join(wavs_dir, f"{i + 1}.wav"))

for i, line in enumerate(metadata):
    _, _, text = line.split('|')
    metadata[i] = f"{i + 1}.wav|{text}"

with open(os.path.join(dataset_dir, 'metadata.csv'), 'w') as f:
    f.write('\n'.join(metadata))