import pandas as pd


def juntar_planilhas(nome_planilha1: str, nome_planilha2: str) -> pd.DataFrame:
    df_1 = pd.read_excel(f'{nome_planilha1.strip()}.xlsx')
    df_2 = pd.read_excel(f'{nome_planilha2.strip()}.xlsx')

    df_join = pd.merge(df_1, df_2, left_on='MATR_ALUNO', right_on='MATRICULA')

    colunas = ['ID_PESSOA', 'NOME_PESSOA', 'SEXO',
               'DT_NASCIMENTO', 'FORMA_INGRESSO', 'FORMA_EVASAO',
               'MATR_ALUNO', 'NUM_VERSAO', 'PERIODO_INGRESSO',
               'DT_EVASAO', 'PERIODO_EVASAO', 'CPF_MASCARA',
               'CRA', 'BAIRRO', 'CIDADE', 'ESTADO']
    df_join = df_join.filter(items=colunas)

    return df_join
