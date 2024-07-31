import os

import disnake
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", None) is not None

TOKEN = os.getenv("TOKEN", "")
if not TOKEN:
    raise ValueError("TOKEN is not set")

GIT_SHA = os.getenv("GIT_SHA", "unknown")

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "DEBUG" if DEBUG else "INFO")

ECHO_SENTENCE = "I will not ask for updates"

# Typehints
ACI = disnake.ApplicationCommandInteraction
