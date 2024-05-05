import glob
import re

from encodec import EncodecModel
from encodec.utils import convert_audio

import torchaudio
import torch


import random

import numpy as np
import torch
import torch.optim as optim
import tqdm
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset

from perceiver_ar_pytorch import PerceiverAR
from perceiver_ar_pytorch.autoregressive_wrapper import AutoregressiveWrapper

# constants

NUM_BATCHES = int(1e5)
BATCH_SIZE = 4
GRADIENT_ACCUMULATE_EVERY = 4
LEARNING_RATE = 2e-4
VALIDATE_EVERY = 100
GENERATE_EVERY = 500
GENERATE_LENGTH = 512
SEQ_LEN = 4096
PREFIX_SEQ_LEN = 3584

# helpers


def cycle(loader):
    while True:
        for data in loader:
            yield data


def decode_token(token):
    return str(chr(max(32, token)))


def decode_tokens(tokens):
    return "".join(list(map(decode_token, tokens)))


model = PerceiverAR(
    num_tokens=256,
    dim=512,
    depth=8,
    heads=8,
    dim_head=64,
    cross_attn_dropout=0.5,
    max_seq_len=SEQ_LEN,
    cross_attn_seq_len=PREFIX_SEQ_LEN,
)

model = AutoregressiveWrapper(model)
# model.cuda()


class SonicPiDataset(Dataset):

    # Instantiate a pretrained EnCodec model
    model = EncodecModel.encodec_model_24khz()
    # The number of codebooks used will be determined bythe bandwidth selected.
    # E.g. for a bandwidth of 6kbps, `n_q = 8` codebooks are used.
    # Supported bandwidths are 1.5kbps (n_q = 2), 3 kbps (n_q = 4), 6 kbps (n_q = 8) and 12 kbps (n_q =16) and 24kbps (n_q=32).
    # For the 48 kHz model, only 3, 6, 12, and 24 kbps are supported. The number
    # of codebooks for each is half that of the 24 kHz model as the frame rate is twice as much.
    model.set_target_bandwidth(6.0)

    def __init__(self, path):
        super().__init__()
        self.files = glob.glob("**/*.wav", recursive=True)
        print(self.files)

    def __getitem__(self, index):
        wav = self.files[index]
        full_seq = self.load_wav(wav)
        with open(re.sub(r"\.wav$", "", wav)) as source:
            text = source.read()
        return full_seq, text  # .cuda()

    def __len__(self):
        return len(self.files)

    def load_wav(self, file):
        # Load and pre-process the audio waveform
        wav, sr = torchaudio.load(file)
        wav = convert_audio(wav, sr, self.model.sample_rate, self.model.channels)
        wav = wav.unsqueeze(0)

        # Extract discrete codes from EnCodec
        with torch.no_grad():
            encoded_frames = self.model.encode(wav)
        codes = torch.cat(
            [encoded[0] for encoded in encoded_frames], dim=-1
        )  # [B, n_q, T]

        return codes


sonic_pi = SonicPiDataset("data")
train_size = int(0.8 * len(sonic_pi))
test_size = len(sonic_pi) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(
    sonic_pi, [train_size, test_size]
)


print(train_dataset[1])
print(test_dataset[1])


class TextSamplerDataset(Dataset):
    def __init__(self, data, seq_len):
        super().__init__()
        self.data = data
        self.seq_len = seq_len

    def __getitem__(self, index):
        rand_start = torch.randint(0, self.data.size(0) - self.seq_len, (1,))
        full_seq = self.data[rand_start : rand_start + self.seq_len + 1].long()
        return full_seq  # .cuda()

    def __len__(self):
        return self.data.size(0) // self.seq_len


# train_dataset = TextSamplerDataset(data_train, SEQ_LEN)
# val_dataset = TextSamplerDataset(data_val, SEQ_LEN)
val_dataset = train_dataset
train_loader = cycle(DataLoader(train_dataset, batch_size=BATCH_SIZE))
val_loader = cycle(DataLoader(val_dataset, batch_size=BATCH_SIZE))

# optimizer

optim = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

# training

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
            loss = model(next(val_loader))
            print(f"validation loss: {loss.item()}")

    if i % GENERATE_EVERY == 0:
        model.eval()
        inp = random.choice(val_dataset)[:-1]
        prime = decode_tokens(inp)
        print(f"%s \n\n %s", (prime, "*" * 100))

        sample = model.generate(inp[None, ...], GENERATE_LENGTH)
        output_str = decode_tokens(sample[0])
        print(output_str)
