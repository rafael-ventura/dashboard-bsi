from datetime import datetime

import numpy as np


def classificar_idade(dataframe):
    # Data atual para referência
    data_atual = datetime.now()

    # Calcular idade usando a data de nascimento e a data atual
    # O método .apply() é usado para aplicar a função lambda em cada linha
    dataframe['IDADE'] = dataframe['DT_NASCIMENTO'].apply(
        lambda x: data_atual.year - x.year - ((data_atual.month, data_atual.day) < (x.month, x.day)))

    print("Idade calculada com sucesso")
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
