from tracker.module.version_scrape import Linux 
from dotenv import load_dotenv
import logging
import os
import sys

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

LOGGER = logging.getLogger(__name__)
sys.path.insert(0, os.path.abspath(".."))
lin = Linux()