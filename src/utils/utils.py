import os
import re

import pandas as pd
import unidecode


def pega_caminho_base():
    """
    Função para obter o caminho base do projeto.
    :return: Caminho base do projeto.
    """
    # Retorna o caminho do diretório 'dashboard-bsi' assumindo que este script está em 'dashboard-bsi/src'
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../', '..'))


def carregar_dados(caminho='dados/processado/dfPrincipal.csv'):
    """
    Função para carregar o DataFrame.
    :param caminho: Caminho do arquivo CSV.
    :return: DataFrame com os dados carregados.
    """
    caminho_completo = os.path.join(pega_caminho_base(), caminho)
    if os.path.exists(caminho_completo):
        return pd.read_csv(caminho_completo)
    else:
        return pd.DataFrame()  # Retorna um DataFrame vazio se o arquivo não existir


def salvar_dados(dataframe, caminho='dados/processado/dfPrincipal.csv'):
    """
    Função para salvar o DataFrame em um arquivo CSV.
    :param dataframe: DataFrame a ser salvo.
    :param caminho: Caminho do arquivo CSV onde o DataFrame será salvo.
    :return: None
    """
    caminho_completo = os.path.join(pega_caminho_base(), caminho)
    dataframe.to_csv(caminho_completo, index=False)


def remover_acentos_e_maiusculas(texto):
    """
    Função para remover acentos e converter o texto para maiúsculas.
    :param texto: Texto a ser processado.
    :return: Texto sem acentos e em maiúsculas.
    """

    return unidecode.unidecode(texto).upper()


def limpar_e_normalizar(df, coluna, correcoes, case='lower'):
    """
    Função para limpar e normalizar os dados de uma coluna específica.
    """
    if case == 'lower':
        df[coluna] = df[coluna].apply(lambda x: unidecode.unidecode(x).lower().strip())
    elif case == 'upper':
        df[coluna] = df[coluna].apply(lambda x: unidecode.unidecode(x).upper().strip())
    elif case == 'title':
        df[coluna] = df[coluna].apply(lambda x: unidecode.unidecode(x).title().strip())

    return df


def corrigir_nomes_bairros(df, correcoes_bairros):
    for correto, errados in correcoes_bairros.items():
        df['BAIRRO'] = df['BAIRRO'].replace(errados, correto)
    return df


def corrigir_nomes_cidades(df, correcoes_cidades):
    for correto, errados in correcoes_cidades.items():
        df['CIDADE'] = df['CIDADE'].replace(errados, correto)
    return df


def limpar_e_normalizar_array(array, cases=None):
    """
    Função para limpar e normalizar os dados de um array.
    :param array: Lista com os nomes a serem processados.
    :param cases: Lista de casos a serem aplicados ('lower', 'upper', 'title').
    :return: Array normalizado e limpo.
    """
    if cases is None:
        cases = []

    for case in cases:
        if case == 'title':
            array = [unidecode.unidecode(x).lower().strip() for x in array]
        elif case == 'upper':
            array = [unidecode.unidecode(x).upper().strip() for x in array]
        elif case == 'lower':
            array = [unidecode.unidecode(x).title().strip() for x in array]

    return array


def separar_por_periodo(df):
    # print(f"Total de registros antes da separação por período: {len(df)}")
    df['PERIODO_INGRESSO_FORMATADO'] = pd.to_numeric(df['PERIODO_INGRESSO_FORMATADO'], errors='coerce')

    periodos = {
        '1_antes_cotas': df[(df['ANO_PERIODO_INGRESSO'] >= 2008) & (df['PERIODO_INGRESSO_FORMATADO'] < 2014.1)],
        '2_cotas_2014_2020': df[(df['PERIODO_INGRESSO_FORMATADO'] >= 2014.1) & (df['PERIODO_INGRESSO_FORMATADO'] <= 2019.2)],
        '3_pandemia': df[(df['PERIODO_INGRESSO_FORMATADO'] > 2020.1) & (df['PERIODO_INGRESSO_FORMATADO'] <= 2022.2)],
        '4_pos_pandemia': df[df['PERIODO_INGRESSO_FORMATADO'] >= 2023.0]
    }

    # for periodo, df_periodo in periodos.items():
    #     print(f"Registros no período {periodo}: {len(df_periodo)}")

    return periodos
