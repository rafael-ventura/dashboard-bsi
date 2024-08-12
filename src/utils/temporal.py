import numpy as np
import pandas as pd


def formatar_periodos(df):
    """
    Função para formatar os períodos de ingresso e evasão.
    """
    for periodo in ['PERIODO_EVASAO', 'PERIODO_INGRESSO']:
        df_temp = pd.DataFrame(df[periodo].str.split('/', expand=True))
        df_temp.columns = ['ANO', periodo]
        df_temp[periodo] = df_temp[periodo].str.extract('(\d+)', expand=False)
        df[f'{periodo}_FORMATADO'] = df_temp['ANO'] + '.' + df_temp[periodo]
        df[periodo] = df_temp[periodo]
        df[f'ANO_{periodo}'] = df_temp['ANO']

    df['PERIODO_INGRESSO_FORMATADO'] = df['PERIODO_INGRESSO_FORMATADO'].fillna('0.0')
    return df


def calcular_idade_ingresso(row):
    """
    Função para calcular a idade do aluno no momento do ingresso
    """
    if pd.isna(row['PERIODO_INGRESSO_FORMATADO']) or pd.isna(row['DT_NASCIMENTO']):
        return np.nan

    try:
        ano_ingresso, semestre_ingresso = map(int, row['PERIODO_INGRESSO_FORMATADO'].split('.'))
        if ano_ingresso == 0 and semestre_ingresso == 0:
            return np.nan

        mes_ingresso = 1 if semestre_ingresso == 1 else 7
        data_ingresso = pd.Timestamp(year=ano_ingresso, month=mes_ingresso, day=1)
        idade_ingresso = data_ingresso.year - row['DT_NASCIMENTO'].year - (
                (data_ingresso.month, data_ingresso.day) < (row['DT_NASCIMENTO'].month, row['DT_NASCIMENTO'].day))
        return idade_ingresso
    except (ValueError, TypeError):
        return np.nan


def classificar_idade(df):
    """
    Função para classificar a idade dos alunos no ingresso.
    """
    df['IDADE_INGRESSO'] = df.apply(calcular_idade_ingresso, axis=1)
    return df


def calcular_tempo_curso(df):
    """
    Função para calcular o tempo de curso dos alunos que concluíram.
    """

    def calcular_tempo(row):
        if pd.isna(row['PERIODO_INGRESSO_FORMATADO']) or pd.isna(row['PERIODO_EVASAO_FORMATADO']):
            return np.nan
        try:
            ano_ingresso, semestre_ingresso = map(int, row['PERIODO_INGRESSO_FORMATADO'].split('.'))
            ano_evasao, semestre_evasao = map(int, row['PERIODO_EVASAO_FORMATADO'].split('.'))

            mes_ingresso = 1 if semestre_ingresso == 1 else 7
            mes_evasao = 1 if semestre_evasao == 1 else 7

            data_ingresso = pd.Timestamp(year=ano_ingresso, month=mes_ingresso, day=1)
            data_evasao = pd.Timestamp(year=ano_evasao, month=mes_evasao, day=1)

            tempo_curso = (data_evasao - data_ingresso).days / 365.25  # Calcula o tempo de curso em anos
            return round(tempo_curso, 2)  # Arredonda para 2 casas decimais
        except (ValueError, TypeError):
            return np.nan

    df['TEMPO_CURSO'] = df.apply(calcular_tempo, axis=1)
    return df


def extrair_data_ingresso(row):
    """
    Função para extrair a data de ingresso do aluno
    """
    ano_ingresso, semestre_ingresso = map(int, row['PERIODO_INGRESSO_FORMATADO'].split('.'))
    mes_ingresso = 1 if semestre_ingresso == 1 else 7
    return pd.Timestamp(year=ano_ingresso, month=mes_ingresso, day=1)


def remover_alunos_anteriores_2014(df):
    """
    Função para remover alunos que ingressaram antes de 2014
    """
    df = df[df['ANO_PERIODO_INGRESSO'].astype(float) >= 2014]
    return df
