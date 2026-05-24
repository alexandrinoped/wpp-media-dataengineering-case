from datetime import datetime, timedelta

from api_client import (
    generate_report,
    get_access_token,
    get_report_data,
    load_credentials,
    wait_until_report_is_ready,
)
from config import FINAL_REPORT_FILE, PROCESS_ID_FILE, RAW_DIR, REPORT_DAYS
from loader import ensure_directories, save_final_report, save_json, save_process_id
from transformer import transform_data


def main() -> None:
    """
    Orquestra o fluxo completo do pipeline: desde a obtenção do access token,
    passando pela geração e verificação do relatório, até a transformação dos dados.
    """
    print("Iniciando processo...")

    ensure_directories()

    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=REPORT_DAYS)

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    print(f"Período do relatório: {start_date_str} até {end_date_str}")

    print("Carregando credenciais...")
    credentials = load_credentials()

    print("Obtendo access token...")
    access_token = get_access_token(credentials)

    print("Gerando relatório...")
    process_id = generate_report(access_token, start_date_str, end_date_str)
    save_process_id(process_id)

    print(f"process_id gerado: {process_id}")

    print("Aguardando relatório ficar pronto...")
    wait_until_report_is_ready(access_token, process_id)

    print("Baixando relatório de transactions...")
    transactions_data = get_report_data(access_token, process_id, "transactions")

    print("Baixando relatório de products...")
    products_data = get_report_data(access_token, process_id, "products")

    print("Salvando dados brutos em data/raw...")
    save_json(transactions_data, RAW_DIR / "transactions_raw.json")
    save_json(products_data, RAW_DIR / "products_raw.json")

    print("Transformando e cruzando os dados...")
    df_final = transform_data(transactions_data, products_data)

    print(f"Total de linhas no arquivo final: {len(df_final)}")

    print("Salvando arquivo final em CSV UTF-8...")
    save_final_report(df_final)

    print("Processo finalizado com sucesso.")
    print(f"Arquivo final salvo em: {FINAL_REPORT_FILE}")
    print(f"process_id salvo em: {PROCESS_ID_FILE}")


if __name__ == "__main__":
    main()