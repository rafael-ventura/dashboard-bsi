import os
import unidecode
import pandas as pd


def pega_caminho_base():
    """
    Retorna o caminho base do projeto.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../', '..'))


def carregar_dados(caminho='dados/processado/dfPrincipal.csv'):
    """
    Carrega o DataFrame de um arquivo CSV.
    """
    caminho_completo = os.path.join(pega_caminho_base(), caminho)
    if os.path.exists(caminho_completo):
        return pd.read_csv(caminho_completo)
    else:
        print(f"Arquivo não encontrado: {caminho_completo}")
        return pd.DataFrame()


def salvar_dados(dataframe, caminho='dados/processado/dfPrincipal.csv'):
    """
    Salva um DataFrame em um arquivo CSV.
    """
    caminho_completo = os.path.join(pega_caminho_base(), caminho)
    dataframe.to_csv(caminho_completo, index=False)
    print(f"Arquivo salvo em: {caminho_completo}")


def remover_acentos_e_maiusculas(texto):
    """
    Remove acentos e converte o texto para maiúsculas.
    """
    return unidecode.unidecode(texto).upper() if isinstance(texto, str) else texto


def limpar_e_normalizar(df, coluna, case='lower'):
    """
    Limpa e normaliza os valores de uma coluna em um DataFrame.
    """
    if case == 'lower':
        df[coluna] = df[coluna].apply(lambda x: unidecode.unidecode(str(x)).lower().strip())
    elif case == 'upper':
        df[coluna] = df[coluna].apply(lambda x: unidecode.unidecode(str(x)).upper().strip())
    elif case == 'title':
        df[coluna] = df[coluna].apply(lambda x: unidecode.unidecode(str(x)).title().strip())
    return df


def corrigir_nomes(df, coluna, correcoes):
    """
    Corrige valores de uma coluna com base em um dicionário de correções.
    """
    for correto, errados in correcoes.items():
        df[coluna] = df[coluna].replace(errados, correto)
    return df
