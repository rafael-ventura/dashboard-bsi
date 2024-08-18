import numpy as np
import pandas as pd
from src.utils.distancia import adicionar_distancia_ate_urca, inicializar_geolocator
from src.utils.localizacao import correcoes_bairros, agrupar_por_zona, correcoes_cidades, adicionar_cidade_estado
from src.utils.desempenho_academico import classificar_forma_ingresso, classificar_forma_evasao, arredondar_cra
from src.utils.temporal import remover_alunos_anteriores_2014, classificar_idade, calcular_tempo_curso
from src.utils.utils import carregar_dados, salvar_dados, pega_caminho_base, limpar_e_normalizar, corrigir_nomes_bairros, corrigir_nomes_cidades


def ler_dados_brutos(source):
    """
    Função para ler os dados brutos da planilha
    """
    df = pd.read_excel(source)
    return df


def remover_colunas(df, colunas_desnecessarias):
    """
    Função para remover colunas desnecessárias do DataFrame
    """
    return df.drop(colunas_desnecessarias, axis=1)


def preencher_nulos(df, substituicoes):
    """
    Função para preencher valores nulos com substituições
    """
    return df.fillna(substituicoes)


def formatar_periodos(df):
    """
    Função para formatar os períodos de ingresso e evasão
    """
    for periodo in ['PERIODO_EVASAO', 'PERIODO_INGRESSO']:
        df_temp = pd.DataFrame(df[periodo].str.split('/', expand=True))
        df_temp.columns = ['ANO', periodo]
        df_temp[periodo] = df_temp[periodo].str.extract('(\d+)', expand=False)
        df['{}_FORMATADO'.format(periodo)] = df_temp['ANO'] + '.' + df_temp[periodo]
        df[periodo] = df_temp[periodo]
        df['ANO_{}'.format(periodo)] = df_temp['ANO']

    df['PERIODO_INGRESSO_FORMATADO'] = df['PERIODO_INGRESSO_FORMATADO'].fillna('0.0')
    return df


def converter_tipos(df, tipo_campos):
    """
    Função para converter tipos de colunas no DataFrame.
    """
    df['CRA'] = df['CRA'].astype(float)
    df['DT_NASCIMENTO'] = pd.to_datetime(df['DT_NASCIMENTO'], errors='coerce', dayfirst=True)
    df['DT_EVASAO'] = pd.to_datetime(df['DT_EVASAO'], errors='coerce', dayfirst=True)
    return df.astype(tipo_campos)


def formatar_dados(source, incluir_outros=True, dados_anterior_2014=False):
    """
    Função principal para formatar os dados
    """
    df = ler_dados_brutos(source)
    df = remover_colunas(df, ['Seq.'])
    df = preencher_nulos(df, {'BAIRRO': 'Desconhecido', 'CIDADE': 'Desconhecido', 'ESTADO': 'Desconhecido'})
    df = formatar_periodos(df)

    # Aplicar a lógica de remoção de alunos anteriores a 2014
    if not dados_anterior_2014:
        df = remover_alunos_anteriores_2014(df)

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

    df = converter_tipos(df, tipo_campos)
    df = limpar_e_normalizar(df, 'BAIRRO', correcoes_bairros, case='title')
    df = limpar_e_normalizar(df, 'BAIRRO', correcoes_bairros, case='lower')
    df = corrigir_nomes_bairros(df, correcoes_bairros)
    df = limpar_e_normalizar(df, 'CIDADE', correcoes_cidades, case='title')
    df = limpar_e_normalizar(df, 'CIDADE', correcoes_cidades, case='lower')
    df = corrigir_nomes_cidades(df, correcoes_cidades)
    df = adicionar_cidade_estado(df)
    df = agrupar_por_zona(df)
    df = classificar_idade(df)
    df = classificar_forma_ingresso(df, incluir_outros)
    df = classificar_forma_evasao(df)
    df = arredondar_cra(df)
    df = calcular_tempo_curso(df)

    # Carregar DataFrame de distâncias e calcular/atualizar distâncias
    df_distancias = carregar_dados(pega_caminho_base() + '/dados/processado/dfDistancias.csv')

    geolocator = inicializar_geolocator()
    df, df_distancias = adicionar_distancia_ate_urca(df, df_distancias, geolocator)

    # Salvar o DataFrame principal e o DataFrame de distâncias atualizados
    salvar_dados(df_distancias, 'dados/processado/dfDistancias.csv')
    salvar_dados(df, 'dados/processado/dfPrincipal.csv')
    print('DataFrame formatado, classificado e salvo com sucesso!')
    return df


if __name__ == "__main__":
    caminho_arquivo = r'C:\Dev\dashboard-bsi\dados\bruto\PlanilhaNova.xlsx'
    formatar_dados(caminho_arquivo, incluir_outros=False, dados_anterior_2014=True)
