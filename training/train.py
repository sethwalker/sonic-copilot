# %%
import glob
import csv
import re

from datasets import load_dataset, Audio
from transformers import EncodecModel, AutoProcessor

import torch

from perceiver_ar_pytorch import PerceiverAR
from perceiver_ar_pytorch.autoregressive_wrapper import AutoregressiveWrapper


# %%
processor = AutoProcessor.from_pretrained(
    "facebook/encodec_24khz", padding="max_length", max_length=24_000 * 20
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

    # Extract discrete codes from EnCodec
    with torch.no_grad():
        encoded_frames = audio_tokenizing_model.encode(**inputs)
    codes = torch.cat([encoded[0] for encoded in encoded_frames], dim=-1)  # [B, n_q, T]
    batch["codes"] = codes
    return batch


encoded_audio_dataset = audio_dataset.map(
    # prepare_dataset, remove_columns=audio_dataset.column_names
    prepare_dataset
)

# %%
