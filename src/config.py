from pathlib import Path

# --------------------------
# API
# -------------------------

BASE_URL = "https://us-central1-hitchhikers-magrathea.cloudfunctions.net/technical_test"

# --------------------------
# Project paths
# --------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CREDENTIALS_DIR = PROJECT_ROOT / "credentials"

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = DATA_DIR / "output"

PROCESS_ID_FILE = PROJECT_ROOT / "process_id.txt"
FINAL_REPORT_FILE = OUTPUT_DIR / "final_report.csv"

#--------------------------
# Report parameters
#--------------------------

# A API permite recuperar apenas os últimos 60 dias.
# Usado 7 dias para manter a execução inicial mais leve e segura.
REPORT_DAYS = 7

# Quantidade máxima de tentativas para verificar se o relatório ficou pronto.
MAX_RETRIES = 30

# Intervalo, em segundos, entre uma tentativa e outra.
WAIT_SECONDS = 10