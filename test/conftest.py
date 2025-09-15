import os
import sys
import types

# Añade <repo>/src al sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

# Mock mínimo de SecretConfig como módulo para evitar fallos de import en CI
secret = types.ModuleType("SecretConfig")
secret.PGHOST = "localhost"
secret.PGDATABASE = "db"
secret.PGUSER = "user"
secret.PGPASSWORD = "pwd"
secret.PGPORT = "5432"
sys.modules["SecretConfig"] = secret
