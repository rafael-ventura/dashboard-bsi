import numpy as np
import pandas as pd
import unidecode


def ler_dados():
    caminho_arquivo = r'C:\Dev\dashboard-bsi\dados\bruto\planilhaJoinCriptografada.xlsx'
    return pd.read_excel(caminho_arquivo)


def remover_colunas(dataframe):
    colunas_desnecessarias = ['Unnamed: 0', 'ID_PESSOA', 'NOME_PESSOA', 'MATR_ALUNO', 'CPF_MASCARA']
    return dataframe.drop(colunas_desnecessarias, axis=1)


def preencher_nulos(dataframe):
    substituicoes = {
        'BAIRRO': 'Desconhecido',
        'CIDADE': 'Desconhecido',
        'ESTADO': 'Desconhecido'
    }
    return dataframe.fillna(substituicoes)


def formatar_periodos(dataframe):
    for periodo in ['PERIODO_EVASAO', 'PERIODO_INGRESSO']:
        dataframe_temp = pd.DataFrame(dataframe[periodo].str.split('/', expand=True))
        dataframe_temp.columns = ['ANO', periodo]
        dataframe_temp[periodo] = dataframe_temp[periodo].str.extract('(\d+)', expand=False)
        dataframe['PER_' + periodo + '_FORMAT'] = dataframe_temp['ANO'] + '.' + dataframe_temp[periodo]
        dataframe[periodo] = dataframe_temp[periodo]
        dataframe['ANO_' + periodo] = dataframe_temp['ANO']
    return dataframe


def converter_tipos(dataframe):
    tipo_campos = {
        'SEXO': str,
        'DT_NASCIMENTO': 'datetime64[ns]',
        'FORMA_INGRESSO': str,
        'FORMA_EVASAO': str,
        'PERIODO_INGRESSO': np.float64,
        'DT_EVASAO': 'datetime64[ns]',
        'PERIODO_EVASAO': np.float64,
        'ANO_PERIODO_EVASAO': np.float64,
        'PER_PERIODO_EVASAO_FORMAT': str,
        'ANO_PERIODO_INGRESSO': np.float64,
    }
    return dataframe.astype(tipo_campos)


def salvar_dados(dataframe):
    dataframe.to_csv(r'C:\Dev\dashboard-bsi\dados\processado\dfPrincipal.csv', index=False)


def limpa_bairros(dataframe):
    dataframe['BAIRRO'] = dataframe['BAIRRO'].apply(lambda bairro: unidecode.unidecode(bairro).lower().strip())
    return dataframe


def main():
    dataframe = ler_dados()
    dataframe = remover_colunas(dataframe)
    dataframe = preencher_nulos(dataframe)
    dataframe = formatar_periodos(dataframe)
    dataframe = converter_tipos(dataframe)
    dataframe = limpa_bairros(dataframe)
    salvar_dados(dataframe)
    print('DataFrame Principal formatado com sucesso!')


if __name__ == "__main__":
    main()
