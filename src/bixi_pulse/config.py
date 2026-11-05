"""Configuration du projet, lue depuis les variables d'environnement."""

import os

from dotenv import load_dotenv

load_dotenv()

AZURE_STORAGE_ACCOUNT = os.environ["AZURE_STORAGE_ACCOUNT"]
BRONZE_CONTAINER = os.environ.get("BRONZE_CONTAINER", "bronze")