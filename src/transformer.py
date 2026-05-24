import pandas as pd


def format_transaction_date(date_value: str) -> str:
    """
    Converte a data da transação para o formato DD/MM/YYYY.
    A API retorna data com hora:
    2026-05-20 23:10:45

    O formato final solicitado apresenta apenas a data:
    20/05/2026
    """
    parsed_date = pd.to_datetime(date_value, errors="coerce")

    if pd.isna(parsed_date):
        return date_value

    return parsed_date.strftime("%d/%m/%Y")


def transform_data(transactions_data: dict, products_data: list) -> pd.DataFrame:
    """
    Normaliza e cruza os dados de transactions e products pelo campo transaction_id.

    Cada produto associado a uma transação vira uma linha no arquivo final.
    """
    final_rows = []

    for product_group in products_data:
        transaction_id = product_group.get("transaction_id")
        products = product_group.get("products", [])

        transaction = transactions_data.get(transaction_id)

        # Se não existir transação correspondente, o registro é ignorado
        # para evitar gerar linhas incompletas no arquivo final.
        if not transaction:
            continue

        user_data = transaction.get("user_data", {})

        for product in products:
            row = {
                "transaction_id": transaction_id,
                "date": format_transaction_date(transaction.get("date")),
                "user_city": user_data.get("city"),
                "user_state": user_data.get("state"),
                "SKU": product.get("SKU"),
                "description": product.get("description"),
                "color": product.get("color"),
                "product_price": float(product.get("product_price", 0)),
                "quantity": int(product.get("quantity", 0)),
            }

            final_rows.append(row)

    columns = [
        "transaction_id",
        "date",
        "user_city",
        "user_state",
        "SKU",
        "description",
        "color",
        "product_price",
        "quantity",
    ]

    return pd.DataFrame(final_rows, columns=columns)