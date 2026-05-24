import json
import time

import requests

from config import BASE_URL, CREDENTIALS_DIR, MAX_RETRIES, WAIT_SECONDS


def load_credentials() -> dict:
    """
    Carrega as credenciais a partir do arquivo JSON dentro da pasta credentials.

    O client_id é considerado como o nome do arquivo sem a extensão .json.
    """
    credential_files = list(CREDENTIALS_DIR.glob("*.json"))

    if not credential_files:
        raise FileNotFoundError(
            "Nenhum arquivo de credenciais .json foi encontrado na pasta credentials."
        )

    credential_file = credential_files[0]

    with open(credential_file, "r", encoding="utf-8") as file:
        credentials = json.load(file)

    client_id = credential_file.stem

    required_fields = ["client_secret", "jwt_key"]
    missing_fields = [field for field in required_fields if field not in credentials]

    if missing_fields:
        raise ValueError(f"Campos ausentes no arquivo de credenciais: {missing_fields}")

    return {
        "client_id": client_id,
        "client_secret": credentials["client_secret"],
        "jwt_key": credentials["jwt_key"],
    }


def post_to_api(payload: dict) -> dict:
    """
    Executa uma requisição POST para a API e retorna o JSON da resposta.
    """
    try:
        response = requests.post(BASE_URL, json=payload, timeout=60)

        if response.status_code not in [200, 202]:
            raise requests.HTTPError(
                f"Erro na API. Status code: {response.status_code}. Resposta: {response.text}"
            )

        return response.json()

    except requests.exceptions.Timeout as error:
        raise TimeoutError("A requisição para a API excedeu o tempo limite.") from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Erro ao realizar requisição para a API: {error}") from error


def get_access_token(credentials: dict) -> str:
    """
    Obtém o access token usando o fluxo de client credentials.
    """
    payload = {
        "resource": "get_access_token",
        "credentials": {
            "grant_type": "client_credentials",
            "client_id": credentials["client_id"],
            "client_secret": credentials["client_secret"],
            "jwt_key": credentials["jwt_key"],
        },
    }

    response = post_to_api(payload)

    access_token = response.get("access_token")

    if not access_token:
        raise ValueError("Access token não encontrado na resposta da API.")

    return access_token


def generate_report(access_token: str, start_date: str, end_date: str) -> str:
    """
    Solicita a geração do relatório para o período informado.
    """
    payload = {
        "resource": "generate_report",
        "period": {
            "start": start_date,
            "end": end_date,
        },
        "access_token": access_token,
    }

    response = post_to_api(payload)

    process_id = response.get("process_id")

    if not process_id:
        raise ValueError("process_id não encontrado na resposta da API.")

    return process_id


def wait_until_report_is_ready(access_token: str, process_id: str) -> None:
    """
    Verifica periodicamente se o relatório está pronto.
    """
    payload = {
        "resource": "check_report",
        "process_id": process_id,
        "access_token": access_token,
    }

    for attempt in range(1, MAX_RETRIES + 1):
        response = post_to_api(payload)

        ready = response.get("ready", False)

        print(f"Tentativa {attempt}/{MAX_RETRIES} - relatório pronto: {ready}")

        if ready:
            return

        time.sleep(WAIT_SECONDS)

    raise TimeoutError(
        "O relatório não ficou pronto dentro do número máximo de tentativas."
    )


def get_report_data(access_token: str, process_id: str, report_type: str):
    """
    Recupera os dados do relatório gerado.

    report_type pode ser:
    - transactions
    - products
    """
    payload = {
        "resource": "get_data",
        "report_type": report_type,
        "process_id": process_id,
        "access_token": access_token,
    }

    return post_to_api(payload)