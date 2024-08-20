import numpy as np
import pandas as pd
from src.utils.distancia import adicionar_distancia_ate_urca, inicializar_geolocator, salvar_bairros_falha, carregar_bairros_falha
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


from colorama import Fore, Style


def formatar_dados(source, incluir_outros=True, dados_anterior_2014=False):
    """
    Função principal para formatar os dados.
    """

    print(Fore.CYAN + "\n=== INICIANDO FORMATAÇÃO DE DADOS ===" + Style.RESET_ALL)

    # Carregar os dados brutos da planilha
    df = ler_dados_brutos(source)
    print(f"Total de registros após leitura do arquivo: {len(df)}")

    # Checando registros nulos ou inválidos nas colunas principais
    colunas_verificacao = ['CRA', 'BAIRRO', 'CIDADE', 'ESTADO', 'FORMA_INGRESSO', 'FORMA_EVASAO']
    for coluna in colunas_verificacao:
        nulos = df[coluna].isna().sum()
        vazios = (df[coluna] == '').sum()
        if nulos > 0 or vazios > 0:
            print(Fore.RED + f"Atenção: {nulos + vazios} registros com {coluna} nulo ou vazio." + Style.RESET_ALL)

    # Remover colunas desnecessárias
    df = remover_colunas(df, ['Seq.'])
    print(f"Total de registros após remover colunas desnecessárias: {len(df)}")

    # Preencher valores nulos
    df = preencher_nulos(df, {'BAIRRO': 'Desconhecido', 'CIDADE': 'Desconhecido', 'ESTADO': 'Desconhecido'})
    print(Fore.GREEN + f"Preenchimento de nulos para BAIRRO, CIDADE, ESTADO concluído." + Style.RESET_ALL)
    print(f"Total de registros após preencher nulos: {len(df)}")

    # Formatar os períodos de ingresso e evasão
    df = formatar_periodos(df)
    print(f"Total de registros após formatar períodos: {len(df)}")

    # Aplicar a lógica de remoção de alunos anteriores a 2014
    if not dados_anterior_2014:
        registros_antes_remocao = len(df)
        df = remover_alunos_anteriores_2014(df)
        registros_removidos = registros_antes_remocao - len(df)
        print(f"Registros removidos (anteriores a 2014): {registros_removidos}")
        print(f"Total de registros após remover alunos anteriores a 2014: {len(df)}")

    # Converter tipos de colunas
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
    print(f"Total de registros após converter tipos: {len(df)}")

    # Normalizar e corrigir bairros
    df = limpar_e_normalizar(df, 'BAIRRO', correcoes_bairros, case='title')
    df = limpar_e_normalizar(df, 'BAIRRO', correcoes_bairros, case='lower')
    df = corrigir_nomes_bairros(df, correcoes_bairros)
    print(Fore.GREEN + f"Correção e normalização de bairros concluída." + Style.RESET_ALL)
    print(f"Total de registros após normalizar e corrigir bairros: {len(df)}")

    # Normalizar e corrigir cidades
    df = limpar_e_normalizar(df, 'CIDADE', correcoes_cidades, case='title')
    df = limpar_e_normalizar(df, 'CIDADE', correcoes_cidades, case='lower')
    df = corrigir_nomes_cidades(df, correcoes_cidades)
    print(Fore.GREEN + f"Correção e normalização de cidades concluída." + Style.RESET_ALL)
    print(f"Total de registros após normalizar e corrigir cidades: {len(df)}")

    # Adicionar cidade e estado
    df = adicionar_cidade_estado(df)
    print(f"Total de registros após adicionar cidade e estado: {len(df)}")

    # Agrupar por zona geográfica
    df = agrupar_por_zona(df)
    print(f"Total de registros após agrupar por zona: {len(df)}")

    # Classificar idade, forma de ingresso e forma de evasão
    df = classificar_idade(df)
    df = classificar_forma_ingresso(df, incluir_outros)
    df = classificar_forma_evasao(df)
    print(f"Total de registros após classificar idade, forma de ingresso e forma de evasão: {len(df)}")

    # Arredondar CRA
    df = arredondar_cra(df)
    print(f"Total de registros após arredondar CRA: {len(df)}")

    # Calcular tempo de curso
    df = calcular_tempo_curso(df)
    print(f"Total de registros após calcular tempo de curso: {len(df)}")

    # Carregar DataFrame de distâncias e calcular distâncias para Urca
    df_distancias = carregar_dados(pega_caminho_base() + '/dados/processado/dfDistancias.csv')
    bairros_falha_existentes = carregar_bairros_falha()
    geolocator = inicializar_geolocator()

    print(Fore.CYAN + f"\nIniciando cálculo de distâncias para Urca..." + Style.RESET_ALL)
    df, df_distancias, bairros_falha_atualizado = adicionar_distancia_ate_urca(df, df_distancias, geolocator, bairros_falha_existentes)
    print(Fore.GREEN + f"Total de registros após adicionar distâncias: {len(df)}" + Style.RESET_ALL)

    salvar_dados(df_distancias, 'dados/processado/dfDistancias.csv')
    salvar_bairros_falha(bairros_falha_atualizado)  # Salvar a lista atualizada de bairros falhos
    salvar_dados(df, 'dados/processado/dfPrincipal.csv')

    print(Fore.GREEN + 'DataFrame formatado, classificado e salvo com sucesso!' + Style.RESET_ALL)

    return df


if __name__ == "__main__":
    caminho_arquivo = r'C:\Dev\dashboard-bsi\dados\bruto\PlanilhaNova.xlsx'
    formatar_dados(caminho_arquivo, incluir_outros=False, dados_anterior_2014=True)
