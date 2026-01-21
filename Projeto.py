import csv
import json
from pathlib import Path


# =========================
# CAMINHOS DO PROJETO
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'



ARQUIVO_CSV = RAW_DIR / 'clientes.csv'
ARQUIVO_JSON = PROCESSED_DIR / 'clientes_limpos.json'


# =========================
# LEITURA DO CSV
# =========================

def ler_csv(caminho):
    """
    Lê um arquivo CSV e retorna os dados como lista de dicionários
    """
    dados = []

    with open(caminho, newline='', encoding='utf-8-sig') as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=',')
        for linha in leitor:
            dados.append(linha)

    return dados

# =========================
# LIMPEZA E VALIDAÇÃO
# =========================

def limpar_dados(dados):
    dados_limpos = []

    for registro in dados:
        try:
            # normaliza chaves (remove espaços e força minúsculo)
            registro_normalizado = {
                chave.strip().lower(): valor.strip()
                for chave, valor in registro.items()
            }

            id_raw = registro_normalizado.get('id', '')
            nome = registro_normalizado.get('nome', '')
            email = registro_normalizado.get('email', '')
            idade_raw = registro_normalizado.get('idade', '')

            if not id_raw.isdigit():
                continue

            idade_digits = ''.join(c for c in idade_raw if c.isdigit())
            if not idade_digits:
                continue

            id_cliente = int(id_raw)
            idade = int(idade_digits)

            if nome and email and idade >= 18:
                dados_limpos.append({
                    'id': id_cliente,
                    'nome': nome,
                    'email': email,
                    'idade': idade
                })

        except Exception as e:
            print('Erro ao processar registro:', registro, e)

    return dados_limpos

# =========================
# SALVAR EM JSON
# =========================

def salvar_json(dados, caminho):
    """
    Salva os dados limpos em um arquivo JSON
    """
    caminho.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


# =========================
# RELATÓRIO SIMPLES
# =========================

def gerar_relatorio(dados):
    """
    Gera um relatório simples no terminal
    """
    total_clientes = len(dados)
    media_idade = sum(cliente['idade'] for cliente in dados) / total_clientes if total_clientes else 0

    print('\n📊 RELATÓRIO FINAL')
    print(f'Total de clientes válidos: {total_clientes}')
    print(f'Idade média: {media_idade:.1f} anos')


# =========================
# FUNÇÃO PRINCIPAL
# =========================

def main():
    if not ARQUIVO_CSV.exists():
        print('❌ Arquivo CSV não encontrado!')
        return

    dados_brutos = ler_csv(ARQUIVO_CSV)
    print(f'📥 Registros carregados: {len(dados_brutos)}')

    dados_limpos = limpar_dados(dados_brutos)
    print(f'✅ Registros válidos: {len(dados_limpos)}')

    salvar_json(dados_limpos, ARQUIVO_JSON)
    print(f'💾 Dados salvos em: {ARQUIVO_JSON}')

    gerar_relatorio(dados_limpos)


# =========================
# EXECUÇÃO
# =========================

if __name__ == '__main__':
    main()





