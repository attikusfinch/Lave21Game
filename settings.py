import os

from pathlib import Path
from dotenv import load_dotenv

import json

WORKDIR = Path(__file__).parent
I18N_DOMAIN = "lave_bot"
LOCALES_DIR = WORKDIR / "locales"

with open('config.env', 'r') as env_file:
    load_dotenv(stream=env_file)

TOKEN = os.getenv("TOKEN")

WALLET = os.getenv("WALLET")
TONCENTER_API_TOKEN = os.getenv("TONCENTER_API_TOKEN")

LAVE = os.getenv("LAVE") # чтобы его узнать, отправьте lave сами себе и посмотрите в explorer'е

wallet_mnemonics = json.loads(os.getenv("MNEMONIC"))

SUPPORT_ID = 5802571273