from telethon.sync import TelegramClient
from tracker.version_scrape import Linux 
from dotenv import load_dotenv
import logging
import os
import sys

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

LOGGER = logging.getLogger(__name__)
sys.path.insert(0, os.path.abspath(".."))
load_dotenv("vars.env")

api_id = str(os.getenv("API_ID"))
api_hash=str(os.getenv("API_HASH"))
client = TelegramClient('kernel_track',api_id,api_hash)
lin = Linux()