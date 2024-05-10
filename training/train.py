# %%
import glob
import csv
import re
import random

from datasets import load_dataset, Audio
from transformers import EncodecModel, AutoProcessor

import torch
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import tqdm

from perceiver_ar_pytorch import PerceiverAR
from perceiver_ar_pytorch.autoregressive_wrapper import AutoregressiveWrapper

if torch.backends.mps.is_available():
    print("MPS is available!")
    device = torch.device("mps")
else:
    print("MPS is not available. Falling back to CPU.")
    device = torch.device("cpu")

NUM_BATCHES = int(1e5)
BATCH_SIZE = 4
GRADIENT_ACCUMULATE_EVERY = 4
LEARNING_RATE = 2e-4
VALIDATE_EVERY = 100
GENERATE_EVERY = 500
GENERATE_LENGTH = 512
SEQ_LEN = 4096
PREFIX_SEQ_LEN = 3584

# %%
processor = AutoProcessor.from_pretrained(
    "facebook/encodec_24khz",
    device=device,
)

files = glob.glob("**/*.wav", recursive=True)

with open("metadata.csv", "w") as metadata:
    writer = csv.writer(metadata)
    writer.writerow(["file_name", "text"])
    for file in files:
        with open(re.sub(r"\.wav$", "", file)) as source:
            # append and prepend silence tokens to account for recording artifact?
            # e.g. #intro and #outro or #beginrecording and #endrecording
            text = source.read()
        writer.writerow([re.sub(r"^data\/", "", file), text])


# audio_dataset = load_dataset("audiofolder", data_files=files)
audio_dataset = load_dataset("audiofolder", data_dir="data").with_format(
    "torch", device=device
)

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
        padding="max_length",
        max_length=2_000_000,
    )
    inputs["bandwidth"] = 6

    print("input values length:", (inputs["input_values"].shape))

    # Extract discrete codes from EnCodec
    with torch.no_grad():
        audio_codes = audio_tokenizing_model(**inputs).audio_codes
        # batch["audio_codes"] = audio_codes
        # batch["audio_codes"] = torch.cat(
        #     [t for t in torch.tensor(audio_codes).squeeze(0).squeeze(0)]
        # )
        batch["audio_codes"] = torch.cat(
            [encoded[0] for encoded in audio_codes], dim=-1
        )  # [B, n_q, T]

    return batch


encoded_audio_dataset = audio_dataset.map(
    # prepare_dataset, remove_columns=audio_dataset.column_names
    prepare_dataset
)


# %%

filtered_encoded_audio_datasets = encoded_audio_dataset.remove_columns("audio")

# assert # shape of training data is correct


def cycle(loader):
    while True:
        for data in loader:
            print("data:", data)
            yield data


model = PerceiverAR(
    num_tokens=20_000,
    dim=512,
    depth=8,
    heads=8,
    dim_head=64,
    cross_attn_dropout=0.5,
    max_seq_len=SEQ_LEN,
    cross_attn_seq_len=PREFIX_SEQ_LEN,
)

model = AutoregressiveWrapper(model)
model.to(device)

split = filtered_encoded_audio_datasets["train"].train_test_split(test_size=0.2)
train_dataset = split["train"]
test_dataset = split["test"]
train_loader = cycle(DataLoader(train_dataset, batch_size=BATCH_SIZE))
test_loader = cycle(DataLoader(test_dataset, batch_size=BATCH_SIZE))

# %%
optim = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)

for i in tqdm.tqdm(range(NUM_BATCHES), mininterval=10.0, desc="training"):
    model.train()

    for __ in range(GRADIENT_ACCUMULATE_EVERY):
        loss = model(next(train_loader))
        loss.backward()

    print(f"training loss: {loss.item()}")
    torch.nn.utils.clip_grad_norm_(model.parameters(), 0.5)
    optim.step()
    optim.zero_grad()

    if i % VALIDATE_EVERY == 0:
        model.eval()
        with torch.no_grad():
            loss = model(next(test_loader))
            print(f"validation loss: {loss.item()}")

    if i % GENERATE_EVERY == 0:
        model.eval()
        inp = random.choice(test_dataset)[:-1]
        print(f"%s \n\n %s", (inp["text"], "*" * 100))

        sample = model.generate(inp[None, ...], GENERATE_LENGTH)
        output_str = sample[0]
        print(output_str)

# %%
