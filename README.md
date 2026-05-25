# WPP Media - Data Engineering Technical Case

## Visão Geral

Este projeto foi desenvolvido como parte de um teste técnico.

O objetivo é consumir uma API REST de relatórios, autenticar utilizando o fluxo OAuth 2.0, gerar relatórios de transações e produtos, recuperar os dados, realizar o cruzamento entre as fontes e salvar o resultado final em formato tabular.

---

## Objetivo do Pipeline

O pipeline executa as seguintes etapas:

1. Carrega as credenciais da API.
2. Obtém um `access_token` utilizando o fluxo OAuth 2.0.
3. Gera um relatório para um período definido.
4. Verifica o status do relatório até que ele esteja pronto.
5. Recupera os dados dos relatórios de `transactions` e `products`.
6. Salva os dados brutos em formato JSON.
7. Normaliza e cruza os dados utilizando `transaction_id` como chave.
8. Converte os campos numéricos para os tipos corretos:
   - `product_price`: float
   - `quantity`: int
9. Salva o arquivo final em CSV com codificação UTF-8.
10. Salva o `process_id` utilizado na execução.

---

## Estrutura do Projeto

```
wpp-media-dataengineering-case/
│
├── src/
│   ├── __init__.py
│   ├── api_client.py
│   ├── config.py
│   ├── loader.py
│   ├── main.py
│   └── transformer.py
│
├── credentials/
│   └── app_pedro-alexandrino.json
│
├── data/
│   ├── raw/
│   │   ├── transactions_raw.json
│   │   └── products_raw.json
│   │
│   └── output/
│       └── final_report.csv
│
├── process_id.txt
├── requirements.txt
├── .gitignore
└── README.md
```
---

## Organização do Código
O projeto foi organizado de forma modular para separar as responsabilidades do pipeline:

 - `config.py`: centraliza configurações, caminhos e parâmetros de execução.
 - `api_client.py`: concentra a comunicação com a API, autenticação, geração e recuperação dos relatórios.
 - `transformer.py`: realiza a normalização, conversão de tipos e cruzamento dos dados.
 - `loader.py`: salva os arquivos JSON brutos, o CSV final e o process_id.
 - `main.py`: orquestra a execução completa do pipeline:
    1. Carrega credenciais
    2. Obtém access token
    3. Gera relatório
    4. Aguarda processamento
    5. Recupera transactions e products
    6. Salva dados brutos
    7. Transforma e cruza os dados
    8. Salva arquivo final em CSV UTF-8
    9. Salva o process_id utilizado

Essa abordagem melhora a legibilidade do código, facilita manutenção futura e permite evoluções sem alterar toda a lógica principal.

## Pré-requisitos

- Python 3.10, 3.11 ou 3.12
- Ambiente virtual Python
- Bibliotecas listadas no arquivo `requirements.txt`
```
O projeto foi validado utilizando Python 3.12.3 Recomenda-se evitar versões muito recentes ou ainda pouco suportadas por algumas bibliotecas, como Python 3.14, para evitar incompatibilidades na instalação de dependências.
```

## Instalação

1. Crie e ative o ambiente virtual:
```bash
python -m venv .venv
```

2. No Windows PowerShell:
```PowerShell
.venv\Scripts\Activate
```
Ou

```
.\.venv\Scripts\Activate.ps1
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```
## Credenciais
O projeto espera um arquivo JSON de credenciais dentro da pasta `credentials/`.

Exemplo:
```
credentials/app_pedro-alexandrino.json
```

O `client_id` é considerado como o nome do arquivo sem a extensão .json.

Exemplo:
```
app_pedro-alexandrino.json -> client_id = app_pedro-alexandrino
```

O arquivo deve conter os campos:
```JSON
{
  "client_secret": "seu_client_secret",
  "jwt_key": "sua_jwt_key"
}
```
Por segurança, a pasta `credentials/*.json` está incluída no `.gitignore` e não deve ser versionada.

## Execução

Para executar o pipeline, rode o comando abaixo a partir da raiz do projeto:
```bash
python src/main.py
```
## Arquivos Gerados

Após a execução, serão gerados os seguintes arquivos:
```
data/raw/transactions_raw.json
data/raw/products_raw.json
data/output/final_report.csv
process_id.txt
```

## Arquivo Final

O arquivo final é salvo em:
```
data/output/final_report.csv
```
O CSV é salvo com codificação UTF-8 para preservar caracteres especiais, como acentos e cedilha.

As colunas finais seguem o layout solicitado:
```
transaction_id,date,user_city,user_state,SKU,description,color,product_price,quantity
```

## Process ID

O `process_id utilizado` para geração dos relatórios é salvo em:
```
process_id.txt
```

## Decisões Técnicas

 - O projeto utiliza uma estrutura modular para separar extração, transformação e carga.
 - O arquivo final foi salvo em CSV por ser um formato tabular simples, aderente ao layout solicitado no teste.
 - Os dados brutos da API são salvos em data/raw/ para permitir rastreabilidade.
 - O CSV final é salvo em UTF-8 para garantir compatibilidade com caracteres especiais.
 - O período do relatório foi definido no arquivo config.py, respeitando a limitação da API de recuperar apenas dados dos últimos 60 dias.
 - O script implementa verificação do status do relatório antes de tentar recuperar os dados.
 - O token de acesso é obtido utilizando o fluxo OAuth 2.0 com client_credentials.

## Observações de Segurança

O arquivo real de credenciais não deve ser enviado para repositórios públicos.

A entrega deve conter o código-fonte, o arquivo final gerado e o `process_id` utilizado, mas as credenciais devem ser tratadas separadamente.

## Observação sobre execuções

Cada execução do pipeline gera um novo `process_id` por meio do recurso `generate_report`.

Por isso, caso o script seja executado novamente, a quantidade de linhas do arquivo final pode variar conforme os dados retornados pela API para o novo processo gerado.

O arquivo `process_id.txt` corresponde à execução utilizada para gerar os arquivos entregues.