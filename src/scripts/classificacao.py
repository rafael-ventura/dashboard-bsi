import numpy as np
import pandas as pd


def classificar_idade(dataframe):
    # Função para calcular a idade no momento do ingresso
    def calcular_idade_ingresso(row):
        ano_ingresso, semestre_ingresso = map(int, row['PER_PERIODO_INGRESSO_FORMAT'].split('.'))
        mes_ingresso = 1 if semestre_ingresso == 1 else 7  # Janeiro para o 1º semestre, Julho para o 2º
        data_ingresso = pd.Timestamp(year=ano_ingresso, month=mes_ingresso, day=1)
        idade_ingresso = data_ingresso.year - row['DT_NASCIMENTO'].year - ((data_ingresso.month, data_ingresso.day) < (row['DT_NASCIMENTO'].month, row['DT_NASCIMENTO'].day))
        return idade_ingresso

    # Aplicar a função para calcular a idade no momento do ingresso
    dataframe['IDADE'] = dataframe.apply(calcular_idade_ingresso, axis=1)

    return dataframe


def classificar_forma_ingresso(dataframe):
    # Cotas
    cotas = [
        'SISU Escola Publica - Indep. de Renda',
        'SISU Escola Publica até 1,5 S.M.',
        # ... outros termos para cotas
    ]
    # Ampla Concorrência
    ampla_concorrencia = [
        'VE - Vestibular',
        'EN - ENEM',
        'SISU Ampla Concorrencia'
    ]
    # Classificação
    dataframe['FORMA_INGRESSO_SIMPLES'] = dataframe['FORMA_INGRESSO'].apply(
        lambda x: 'Cotas' if x in cotas else 'Ampla Concorrência' if x in ampla_concorrencia else 'Outros'
    )
    return dataframe


def classificar_forma_evasao(dataframe):
    # Condições para classificação de evasão
    condicoes = [
        dataframe['FORMA_EVASAO'].str.contains('ABA|APO|Desistência SiSU|JUB|CAN', na=False),
        dataframe['FORMA_EVASAO'].str.contains('CON', na=False),
        dataframe['FORMA_EVASAO'].str.contains('Sem evasão', na=False)
    ]
    # Categorias correspondentes às condições
    categorias = ['Evasão', 'Concluído', 'Cursando']
    # Classificação
    dataframe['STATUS_EVASAO'] = np.select(condicoes, categorias, default='Evasão')

    # Ajuste da coluna ANO_EVASAO
    # Para os alunos que concluíram, usar o ano de DT_EVASAO
    dataframe.loc[dataframe['STATUS_EVASAO'] == 'Concluído', 'ANO_EVASAO'] = dataframe['DT_EVASAO'].dt.year
    # Para os alunos que estão cursando, ANO_EVASAO deve ser nulo
    dataframe.loc[dataframe['STATUS_EVASAO'] == 'Cursando', 'ANO_EVASAO'] = np.nan
    # Para os alunos que evadiram, usar o ano de DT_EVASAO se disponível, caso contrário, deixar como está
    dataframe.loc[(dataframe['STATUS_EVASAO'] == 'Evasão') & (dataframe['DT_EVASAO'].notnull()), 'ANO_EVASAO'] = \
        dataframe['DT_EVASAO'].dt.year

    return dataframe


def arredondar_cra(df):
    df['CRA_arredondado'] = (df['CRA'] * 2).round() / 2
    return df
