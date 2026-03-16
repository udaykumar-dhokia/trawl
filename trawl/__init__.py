"""trawl - On-Premise AI Powered Research Assistant."""

import os
import sys
import logging

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["HF_HUB_OP_LEVEL_WARNINGS"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

__version__ = "0.1.0"
__author__ = "Udaykumar Dhokia"
__email__ = "udaykumardhokia@gmail.com"
__license__ = "MIT"