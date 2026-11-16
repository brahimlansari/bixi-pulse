"""Configuration commune à tous les tests."""
import os

# config.py lit cette variable dès l'import : on fournit une valeur factice pour les tests.
os.environ.setdefault("AZURE_STORAGE_ACCOUNT", "comptedetest")