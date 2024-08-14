import numpy as np
import pandas as pd


def arredondar_cra(df):
    """
    Função para arredondar o CRA.
    """
    df['CRA_ARREDONDADO'] = (df['CRA'] * 2).round() / 2
    return df


def classificar_forma_ingresso(df, incluir_outros=True):
    """
    Função para classificar a forma de ingresso dos alunos
    """
    cotas = [
        'SISU Escola Publica - Indep. de Renda',
        'SISU Escola Pública até 1,5 S.M Índio',
        'SISU Escola Pública até 1,5 S.M Preto e Pardo',
        'SISU Escola Pública até 1,5 S.M.',
        'SISU Escola Pública até 1,5 S.M. Preto, Pardo, Indígena',
        'SISU Escola Pública, Indep. de Renda: Preto, Pardo, Indígena',
        'SISU Escola Pública, Indep. de Renda: Índio',
        'SISU Escola Pública, Indep. de Renda: Preto e Pardo'
    ]
    ampla_concorrencia = ['VE - Vestibular', 'EN - ENEM', 'SISU Ampla Concorrencia']
    df['FORMA_INGRESSO_SIMPLES'] = df['FORMA_INGRESSO'].apply(
        lambda x: 'Cotas' if x in cotas else 'Ampla Concorrencia' if x in ampla_concorrencia else 'Outros')
    if not incluir_outros:
        df = df[(df['FORMA_INGRESSO_SIMPLES'] == 'Cotas') | (df['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia')]
    return df


def classificar_forma_evasao(df):
    """
    Função para classificar a forma de evasão dos alunos e preservar a forma detalhada.
    """
    # Preservando a forma de evasão detalhada
    df['FORMA_EVASAO_DETALHADA'] = df['FORMA_EVASAO'].copy()

    condicoes = [
        df['FORMA_EVASAO'].str.contains('ABA|APO|Desistência SiSU|JUB|CAN|FAL|TIC ', na=False),
        df['FORMA_EVASAO'].str.contains('CON', na=False),
        df['FORMA_EVASAO'].str.contains('Sem evasão', na=False)
    ]
    categorias = ['Evasão', 'Concluído', 'Cursando']
    df['STATUS_EVASAO'] = np.select(condicoes, categorias, default='Evasão')
    return df
