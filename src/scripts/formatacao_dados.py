import numpy as np
import pandas as pd
import unidecode

from src.scripts.distancia import calcular_distancia_ate_urca, adicionar_distancia_ate_urca


# Função para ler os dados brutos da planilha
def ler_dados():
    caminho_arquivo = r'C:\Dev\dashboard-bsi\dados\bruto\planilhaJoinCriptografada.xlsx'
    df = pd.read_excel(caminho_arquivo)
    df['DT_NASCIMENTO'] = pd.to_datetime(df['DT_NASCIMENTO'], errors='coerce')
    df['DT_EVASAO'] = pd.to_datetime(df['DT_EVASAO'], errors='coerce')
    return df


def remover_colunas(df):
    """
    # Função para remover colunas desnecessárias do DataFrame.
    """
    colunas_desnecessarias = ['Unnamed: 0', 'ID_PESSOA', 'NOME_PESSOA', 'MATR_ALUNO', 'CPF_MASCARA']
    return df.drop(colunas_desnecessarias, axis=1)


def preencher_nulos(df):
    """
    Função para preencher valores nulos nas colunas de bairro, cidade e estado.
    """
    substituicoes = {'BAIRRO': 'Desconhecido',
                     'CIDADE': 'Desconhecido',
                     'ESTADO': 'Desconhecido'}
    return df.fillna(substituicoes)


def formatar_periodos(df):
    """
    Função para formatar os períodos de ingresso e evasão, separando o ano e o semestre.
    """
    for periodo in ['PERIODO_EVASAO', 'PERIODO_INGRESSO']:
        df_temp = pd.DataFrame(df[periodo].str.split('/', expand=True))
        df_temp.columns = ['ANO', periodo]
        df_temp[periodo] = df_temp[periodo].str.extract('(\d+)', expand=False)
        df[f'{periodo}_FORMATADO'] = df_temp['ANO'] + '.' + df_temp[periodo]
        df[periodo] = df_temp[periodo]
        df[f'ANO_{periodo}'] = df_temp['ANO']
    return df


def converter_tipos(df):
    """
    Função para converter os tipos das colunas do DataFrame.
    """
    tipo_campos = {
        'SEXO': str,
        'DT_NASCIMENTO': 'datetime64[ns]',
        'FORMA_INGRESSO': str,
        'FORMA_EVASAO': str,
        'PERIODO_INGRESSO': np.float64,
        'DT_EVASAO': 'datetime64[ns]',
        'PERIODO_EVASAO': np.float64,
        'ANO_PERIODO_EVASAO': np.float64,
        'PERIODO_INGRESSO_FORMATADO': str,
        'ANO_PERIODO_INGRESSO': np.float64
    }

    df['CRA'] = df['CRA'].str.replace(',', '.').astype(float)
    return df.astype(tipo_campos)


def limpar_bairros(df):
    """
    Função para limpar e normalizar os nomes dos bairros.
    """
    df['BAIRRO'] = df['BAIRRO'].apply(lambda bairro: unidecode.unidecode(bairro).lower().strip())
    correcoes_bairros = {'freguesia.*': 'freguesia (jacarepagua)'}
    for padrao, correcao in correcoes_bairros.items():
        df['BAIRRO'] = df['BAIRRO'].str.replace(padrao, correcao, regex=True)
    return df


def adicionar_cidade_estado(df):
    """
    Função para adicionar informações de cidade e estado com base nos bairros do Rio de Janeiro.
    """
    bairros_rj = [
        'tijuca', 'jardim botanico', 'santa teresa', 'leme', 'copacabana',
        'meier', 'vila da penha', 'botafogo', 'icarai', 'laranjeiras',
        'catete', 'rocinha', 'olaria', 'flamengo', 'madureira', 'urca', 'rocha'
    ]

    for bairro in bairros_rj:
        df.loc[(df['BAIRRO'] == bairro) & (
                (df['CIDADE'] == 'Desconhecido') | (df['ESTADO'] == 'Desconhecido')), ['CIDADE', 'ESTADO']] = [
            'Rio de Janeiro', 'Rio de Janeiro']

    bairros_duque_caxias = ['jardim olavo bilac', 'gramacho']
    for bairro in bairros_duque_caxias:
        df.loc[(df['BAIRRO'] == bairro) & (
                (df['CIDADE'] == 'Desconhecido') | (df['ESTADO'] == 'Desconhecido')), ['CIDADE', 'ESTADO']] = [
            'Duque de Caxias', 'Rio de Janeiro']

    return df


def normalizar_bairros(df):
    """
    Função para normalizar os nomes dos bairros.
    """
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
        'braz de pina': 'bras de pina'
    }
    df['BAIRRO'] = df['BAIRRO'].apply(lambda b: correcoes.get(b, b))
    return df


def arredondar_cra(df):
    """
    Função para arredondar o CRA dos alunos para a escala de 0.5.
    """
    df['CRA_arredondado'] = (df['CRA'] * 2).round() / 2
    return df


def classificar_idade(df):
    """
    Função para classificar a idade dos alunos no momento do ingresso.
    """
    df['IDADE_INGRESSO'] = df.apply(calcular_idade_ingresso, axis=1)
    return df


def calcular_idade_ingresso(row):
    """
    Função para calcular a idade do aluno no momento do ingresso.:
    """
    ano_ingresso, semestre_ingresso = map(int, row['PERIODO_INGRESSO_FORMATADO'].split('.'))
    mes_ingresso = 1 if semestre_ingresso == 1 else 7
    data_ingresso = pd.Timestamp(year=ano_ingresso, month=mes_ingresso, day=1)
    idade_ingresso = data_ingresso.year - row['DT_NASCIMENTO'].year - (
            (data_ingresso.month, data_ingresso.day) < (row['DT_NASCIMENTO'].month, row['DT_NASCIMENTO'].day))
    return idade_ingresso


def classificar_forma_ingresso(df):
    """
    Função para classificar os alunos em cotistas, ampla concorrência e outros.
    """
    cotas = ['SISU Escola Publica - Indep. de Renda', 'SISU Escola Publica até 1,5 S.M.']
    ampla_concorrencia = ['VE - Vestibular', 'EN - ENEM', 'SISU Ampla Concorrencia']
    df['FORMA_INGRESSO_SIMPLES'] = df['FORMA_INGRESSO'].apply(
        lambda x: 'Cotas' if x in cotas else 'Ampla Concorrência' if x in ampla_concorrencia else 'Outros')
    return df


def classificar_forma_evasao(df):
    """
    Função para classificar os alunos em Evasão, Concluído ou Cursando.
    """
    condicoes = [
        df['FORMA_EVASAO'].str.contains('ABA|APO|Desistência SiSU|JUB|CAN', na=False),
        df['FORMA_EVASAO'].str.contains('CON', na=False),
        df['FORMA_EVASAO'].str.contains('Sem evasão', na=False)
    ]
    categorias = ['Evasão', 'Concluído', 'Cursando']
    df['STATUS_EVASAO'] = np.select(condicoes, categorias, default='Evasão')
    return df


def extrair_data_ingresso(row):
    """
    Função para extrair a data de ingresso do aluno.
    """
    ano_ingresso, semestre_ingresso = map(int, row['PERIODO_INGRESSO_FORMATADO'].split('.'))
    mes_ingresso = 1 if semestre_ingresso == 1 else 7
    return pd.Timestamp(year=ano_ingresso, month=mes_ingresso, day=1)


def calcular_tempo_curso(df):
    """
    Função para calcular o tempo de curso dos alunos concluídos.
    """
    df_concluidos = df[df['STATUS_EVASAO'] == 'Concluído'].copy()
    df_concluidos['TEMPO_CURSO'] = df_concluidos.apply(lambda row: ((extrair_data_ingresso(row).year - int(
        row['ANO_PERIODO_INGRESSO'])) * 12 + extrair_data_ingresso(row).month - (
                                                                        1 if row['PERIODO_INGRESSO_FORMATADO'].endswith(
                                                                            '.1') else 7)) // 6, axis=1)
    df['TEMPO_CURSO'] = df_concluidos['TEMPO_CURSO']
    return df


def salvar_dados(df):
    """
    Função para salvar o DataFrame formatado em um arquivo CSV.
    """
    df.to_csv(r'C:\Dev\dashboard-bsi\dados\processado\dfPrincipal.csv', index=False)


def formatar():
    """
    Função principal para formatar e classificar os dados brutos.
    """
    df = ler_dados()
    df = remover_colunas(df)
    df = preencher_nulos(df)
    df = formatar_periodos(df)
    df = converter_tipos(df)
    df = limpar_bairros(df)
    df = adicionar_cidade_estado(df)
    df = normalizar_bairros(df)
    df = classificar_idade(df)
    df = classificar_forma_ingresso(df)
    df = classificar_forma_evasao(df)
    df = arredondar_cra(df)
    df = calcular_tempo_curso(df)
    #df = adicionar_distancia_ate_urca(df)
    salvar_dados(df)
    print('DataFrame formatado, classificado e salvo com sucesso!')
    return df


if __name__ == "__main__":
    formatar()
