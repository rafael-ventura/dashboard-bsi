import re
import unidecode
from src.utils.zonas_geograficas import *


def adicionar_cidade_estado(df):
    mapeamento_bairros = {
        'Rio de Janeiro': [
            'tijuca', 'jardim botanico', 'santa teresa', 'leme', 'copacabana',
            'meier', 'vila da penha', 'botafogo', 'icarai', 'laranjeiras',
            'catete', 'rocinha', 'olaria', 'flamengo', 'madureira', 'urca', 'rocha'
        ],
        'Duque de Caxias': ['jardim olavo bilac', 'gramacho'],
        'Ilha do Governador': ['jardim guanabara', 'cocaia', 'freguesia (ilha do governador)'],
    }

    for cidade, bairros in mapeamento_bairros.items():
        df.loc[
            (df['BAIRRO'].isin(bairros)) &
            ((df['CIDADE'] == 'Desconhecido') | (df['ESTADO'] == 'Desconhecido')),
            ['CIDADE', 'ESTADO']
        ] = [cidade, 'Rio de Janeiro']

    return df


def normalizar(texto):
    """Função para normalizar strings: remove acentos, converte para minúsculas e remove espaços extras."""
    texto = unidecode.unidecode(texto.strip().lower())
    texto = re.sub(r'\s+', ' ', texto)  # Remove múltiplos espaços
    return texto


def verificar_bairro_em_zonas(bairro):
    bairro_normalizado = normalizar(bairro)

    for zona, lista_bairros in [
        ('Zona Norte', zona_norte),
        ('Zona Oeste', zona_oeste),
        ('Zona Sul', zona_sul),
        ('Centro', bairros_centro),
        ('Baixada Fluminense', baixada_fluminense),
        ('Niterói/São Gonçalo', niteroi_sao_goncalo),
        ('Região Serrana', regiao_serrana),
        ('Região dos Lagos', regiao_dos_lagos)
    ]:
        for bairro_zona in lista_bairros:
            bairro_zona_normalizado = normalizar(bairro_zona)
            if bairro_normalizado == bairro_zona_normalizado:
                return zona

    return None


def verificar_cidade_em_regioes(cidade):
    cidade_normalizada = normalizar(cidade)

    for regiao, lista_cidades in [
        ('Baixada Fluminense', baixada_fluminense),
        ('Niterói/São Gonçalo', niteroi_sao_goncalo),
        ('Região Serrana', regiao_serrana),
        ('Região dos Lagos', regiao_dos_lagos),
        ('Volta Redonda', regiao_volta_redonda),
        ('Campos dos Goytacazes', regiao_campos)
    ]:
        for cidade_regiao in lista_cidades:
            cidade_regiao_normalizada = normalizar(cidade_regiao)
            if cidade_normalizada == cidade_regiao_normalizada:
                return regiao

    return None


def agrupar_por_zona(df):
    """
    Função para agrupar os bairros do Rio de Janeiro por zona.
    """

    def get_zona(bairro, cidade, estado):
        if estado != 'Rio de Janeiro':
            return 'Outro Estado'

        zona_bairro = verificar_bairro_em_zonas(bairro)
        if zona_bairro:
            return zona_bairro

        zona_cidade = verificar_cidade_em_regioes(cidade)
        if zona_cidade:
            return zona_cidade

        return 'Outros'

    # Adiciona a coluna 'ZONA' ao DataFrame
    df['ZONA'] = df.apply(lambda row: get_zona(row['BAIRRO'], row['CIDADE'], row['ESTADO']), axis=1)
    return df
