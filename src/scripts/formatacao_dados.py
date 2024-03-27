import numpy as np
import pandas as pd
import unidecode
from classificacao import classificar_forma_ingresso, classificar_forma_evasao, classificar_idade


def ler_dados():
    caminho_arquivo = r'C:\Dev\dashboard-bsi\dados\bruto\planilhaJoinCriptografada.xlsx'
    dataframe = pd.read_excel(caminho_arquivo)

    # Converter colunas de data para o tipo datetime logo após a leitura
    dataframe['DT_NASCIMENTO'] = pd.to_datetime(dataframe['DT_NASCIMENTO'], errors='coerce')
    dataframe['DT_EVASAO'] = pd.to_datetime(dataframe['DT_EVASAO'], errors='coerce')
    return dataframe


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


# TODO: implementar no arquivo formatacao_dados uma conversão do campo ANO_PERIODO_INGRESSO de float para date.year
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


def limpar_bairros(dataframe):
    dataframe['BAIRRO'] = dataframe['BAIRRO'].apply(lambda bairro: unidecode.unidecode(bairro).lower().strip())

    correcoes_bairros = {
        'freguesia.*': 'freguesia (jacarepagua)',

    }
    for padrao, correcao in correcoes_bairros.items():
        dataframe['BAIRRO'] = dataframe['BAIRRO'].str.replace(padrao, correcao, regex=True, case=False)
    return dataframe


def adicionar_cidade_estado(dataframe):
    bairros_rj = [
        'tijuca', 'jardim botanico', 'santa teresa', 'leme', 'copacabana',
        'meier', 'vila da penha', 'botafogo', 'icarai', 'laranjeiras',
        'catete', 'rocinha', 'olaria', 'flamengo', 'madureira', 'urca', 'rocha'
    ]

    # Atualizar cidade e estado para registros com bairros específicos e cidade/estado desconhecidos
    for bairro in bairros_rj:
        dataframe.loc[(dataframe['BAIRRO'] == bairro) & (
                (dataframe['CIDADE'] == 'Desconhecido') | (dataframe['ESTADO'] == 'Desconhecido')), ['CIDADE',
                                                                                                     'ESTADO']] = [
            'Rio de Janeiro', 'Rio de Janeiro']

    # Tratamento especial para 'Jardim Olavo Bilac' e 'Gramacho', que estão em Duque de Caxias
    bairros_duque_caxias = ['jardim olavo bilac', 'gramacho']
    for bairro in bairros_duque_caxias:
        dataframe.loc[(dataframe['BAIRRO'] == bairro) & (
                (dataframe['CIDADE'] == 'Desconhecido') | (dataframe['ESTADO'] == 'Desconhecido')), ['CIDADE',
                                                                                                     'ESTADO']] = [
            'Duque de Caxias', 'Rio de Janeiro']

    dataframe.loc[dataframe['BAIRRO'] == 'centro/nova iguacu', 'CIDADE'] = 'Nova Iguaçu'

    return dataframe


def normalizar_bairros(dataframe):
    correcoes = {
        'cosme velh': 'cosme velho',
        'iraja!': 'iraja',
        'jardim guanabara/ilha do governador': 'jardim guanabara',
        'jardim guanabara / ilha do governador': 'jardim guanabara',
        'taquara-jacarepagua': 'taquara',
        'pechincha / jacarepagua': 'pechincha',
        'praassa da bandeira': 'praca da bandeira',
        'praassa seca': 'praca seca',
        'maracanaps': 'maracana',
        'sapso francisco xavier': 'sao francisco xavier',
        'inhaaoma': 'inhauma',
        'jadim boa esperanca': 'jardim boa esperanca',
        'vila carvalho (vila inhomirim)': 'vila inhomirim',
        'barra': 'barra da tijuca',
        'alto': 'alto da boa vista',
        'coelho': 'coelho neto',
        'jardim olavo': 'jardim olavo bilac',
        'gramacho': 'jardim gramacho',
        'itopeba': 'itapeba',
        'higianopolis': 'higienopolis',
        'pca da bandeira': 'praca da bandeira',
        'recreio': 'recreio dos bandeirantes',
        'sauassu ': 'sauaçu',
        'parque maita (vila inhomirim)': 'vila inhomirim',
        'vila brasil (manilha)': 'vila brasil',
        'santa tereza': 'santa teresa',
        'quintino': 'quintino bocaiuva',
        'laranjeira': 'laranjeiras',
        'bonsuceso': 'bonsucesso',
        'braz de pina': 'bras de pina',

    }

    dataframe['BAIRRO'] = dataframe['BAIRRO'].apply(lambda b: correcoes.get(b, b))
    return dataframe


def classificar(dataframe):

    print("Iniciando classificação dos dados...")
    # Classifica a forma de ingresso
    dataframe = classificar_forma_ingresso(dataframe)

    # Classifica a forma de evasão e faz ajustes adicionais, incluindo ANO_EVASAO
    dataframe = classificar_forma_evasao(dataframe)
    # Classifica a idade
    dataframe = classificar_idade(dataframe)
    return dataframe


# Adicione as funções que você já definiu aqui

def formatar_e_classificar_dados():
    df = ler_dados()
    df = remover_colunas(df)
    df = preencher_nulos(df)
    df = formatar_periodos(df)
    df = converter_tipos(df)
    df = limpar_bairros(df)
    df = adicionar_cidade_estado(df)
    df = normalizar_bairros(df)
    df = classificar(df)
    salvar_dados(df)
    print('DataFrame formatado, classificado e salvo com sucesso!')
    return df

