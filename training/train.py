# %%
import glob
import csv
import re

from datasets import load_dataset, Audio
from transformers import EncodecModel, AutoProcessor

import torch

#from perceiver_ar_pytorch import PerceiverAR
#from perceiver_ar_pytorch.autoregressive_wrapper import AutoregressiveWrapper

if torch.backends.mps.is_available():
    print("MPS is available!")
    device = torch.device("mps")
else:
    print("MPS is not available. Falling back to CPU.")
    device = torch.device("cpu")


# %%
processor = AutoProcessor.from_pretrained(
    "facebook/encodec_24khz", padding="max_length", max_length=24_000 * 20, device=device
)

files = glob.glob("**/*.wav", recursive=True)

with open("metadata.csv", "w") as metadata:
    writer = csv.writer(metadata)
    writer.writerow(["file_name", "text"])
    for file in files:
        with open(re.sub(r"\.wav$", "", file)) as source:
            text = source.read()
        writer.writerow([re.sub(r"^data\/", "", file), text])


# audio_dataset = load_dataset("audiofolder", data_files=files)
audio_dataset = load_dataset("audiofolder", data_dir="data")

audio_dataset = audio_dataset.cast_column(
    "audio", Audio(sampling_rate=processor.sampling_rate)
)

model_id = "facebook/encodec_24khz"
audio_tokenizing_model = EncodecModel.from_pretrained(model_id)

# %%
def prepare_dataset(batch):
    audio = batch["audio"]
    inputs = processor(
        raw_audio=audio["array"],
        sampling_rate=processor.sampling_rate,
        return_tensors="pt",
    )
    inputs['bandwidth'] = 6

    # Extract discrete codes from EnCodec
    with torch.no_grad():
        audio_codes = audio_tokenizing_model(**inputs).audio_codes
    batch["codes"] = torch.cat([t for t in torch.tensor(audio_codes).squeeze(0).squeeze(0)])
    return batch


encoded_audio_dataset = audio_dataset.map(
    # prepare_dataset, remove_columns=audio_dataset.column_names
    prepare_dataset
)

# %%
