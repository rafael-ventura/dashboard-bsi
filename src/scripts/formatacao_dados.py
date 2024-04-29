import numpy as np
import pandas as pd
import unidecode

from src.utils.distancia import adicionar_distancia_ate_urca, inicializar_geolocator
from src.utils.utils import carregar_dados, pega_caminho_base, salvar_dados


# Função para ler os dados brutos da planilha
def ler_dados_brutos():
    """
    Função para ler os dados brutos da planilha.
    :return: DataFrame com os dados.
    """

    caminho_arquivo = r'C:\Dev\dashboard-bsi\dados\bruto\planilhaJoinCriptografada.xlsx'
    df = pd.read_excel(caminho_arquivo)
    df['DT_NASCIMENTO'] = pd.to_datetime(df['DT_NASCIMENTO'], errors='coerce')
    df['DT_EVASAO'] = pd.to_datetime(df['DT_EVASAO'], errors='coerce')
    return df


def remover_colunas(df):
    """
    # Função para remover colunas desnecessárias do DataFrame.
    :param df: DataFrame com os dados.
    :return: DataFrame atualizado.
    """
    colunas_desnecessarias = ['Unnamed: 0', 'ID_PESSOA', 'NOME_PESSOA', 'MATR_ALUNO', 'CPF_MASCARA']
    return df.drop(colunas_desnecessarias, axis=1)


def preencher_nulos(df):
    """
    Função para preencher valores nulos nas colunas de bairro, cidade e estado.
    :param df: DataFrame com os dados.
    :return: DataFrame atualizado.
    """
    substituicoes = {'BAIRRO': 'Desconhecido',
                     'CIDADE': 'Desconhecido',
                     'ESTADO': 'Desconhecido'}
    return df.fillna(substituicoes)


def formatar_periodos(df):
    """
    Função para formatar os períodos de ingresso e evasão, separando o ano e o semestre.
    :param df: DataFrame com os dados.
    :return: DataFrame atualizado.
    """
    for periodo in ['PERIODO_EVASAO', 'PERIODO_INGRESSO']:
        df_temp = pd.DataFrame(df[periodo].str.split('/', expand=True))
        df_temp.columns = ['ANO', periodo]
        df_temp[periodo] = df_temp[periodo].str.extract('(\d+)', expand=False)
        df['{}_FORMATADO'.format(periodo)] = df_temp['ANO'] + '.' + df_temp[periodo]
        df[periodo] = df_temp[periodo]
        df['ANO_{}'.format(periodo)] = df_temp['ANO']
    return df


def converter_tipos(df):
    """
    Função para converter os tipos das colunas do DataFrame.
    :param df: DataFrame com os dados.
    :return: DataFrame atualizado.
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
    :param df: DataFrame com os dados.
    :return: DataFrame atualizado.
    """
    df['BAIRRO'] = df['BAIRRO'].apply(lambda bairro: unidecode.unidecode(bairro).lower().strip())
    correcoes_bairros = {
        'freguesia.*': 'freguesia',
        'tanque.*': 'tanque'
    }

    for padrao, correcao in correcoes_bairros.items():
        df['BAIRRO'] = df['BAIRRO'].str.replace(padrao, correcao, regex=True)
    return df


def limpar_cidades(df):
    """
    Função para limpar e normalizar os nomes das cidades.
    :param df: DataFrame com os dados.
    :return: DataFrame atualizado.
    """
    df['CIDADE'] = df['CIDADE'].apply(lambda x: unidecode.unidecode(x).strip().upper())
    correcoes_cidades = {
        'RIO DE JANEIRO': ['RIO DE JANEIRO', 'RIO DE JANERO', 'RIO D JANEIRO'],  # exemplo de correção
        'NITEROI': ['NITEROI', 'NITERÓI'],
        'MARICA': ['MARICA', 'MARICÁ'],
        'VITORIA': ['VITORIA', 'VITÓRIA'],
        'BELO HORIZONTE': ['BELO HORIZONTE', 'BELO HORIZONTE MG'],  # outro exemplo
        'BRASILIA': ['BRASILIA', 'BRASÍLIA']
    }

    for correct, variations in correcoes_cidades.items():
        for var in variations:
            df['CIDADE'] = df['CIDADE'].replace(var, correct)

    return df


def adicionar_cidade_estado(df):
    """
    Função para adicionar a cidade e o estado para alguns bairros do Rio de Janeiro.
    :param df: DataFrame com os dados.
    :return: DataFrame atualizado.
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

    df = df[df['BAIRRO'] != 'Desconhecido']
    df = df[df['CIDADE'] != 'Desconhecido']
    df = df[df['ESTADO'] != 'Desconhecido']
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
        'braz de pina': 'bras de pina',
        'vila isabe': 'vila isabel',
        'marcahl hermes': 'marechal hermes',
        'setor habitacional jardim botanico (lago sul)': 'jardim botanico',
        'sao corrado': 'sao conrado',
        'vila abolicao': 'abolição',
        'huimaita': 'humaita',

    }
    df['BAIRRO'] = df['BAIRRO'].apply(lambda b: correcoes.get(b, b))
    return df


def arredondar_cra(df):
    """
    Função para arredondar o CRA dos alunos para a escala de 0,5.
    """
    df['CRA_ARREDONDADO'] = (df['CRA'] * 2).round() / 2
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


def classificar_forma_ingresso(df, incluir_outros=True):
    """
    Função para classificar os alunos em cotistas, ampla concorrência e outros.
    """
    cotas = ['SISU Escola Publica - Indep. de Renda',
             'SISU Escola Pública até 1,5 S.M Índio',
             'SISU Escola Pública até 1,5 S.M Preto e Pardo',
             'SISU Escola Pública até 1,5 S.M.',
             'SISU Escola Pública até 1,5 S.M. Preto, Pardo, Indígena',
             'SISU Escola Pública, Indep. de Renda: Preto, Pardo, Indígena',
             'SISU Escola Pública, Indep. de Renda: Índio',
             'SISU Escola Pública, Indep. de Renda: Preto e Pardo']
    ampla_concorrencia = ['VE - Vestibular', 'EN - ENEM', 'SISU Ampla Concorrencia']
    df['FORMA_INGRESSO_SIMPLES'] = df['FORMA_INGRESSO'].apply(
        lambda x: 'Cotas' if x in cotas else 'Ampla Concorrência' if x in ampla_concorrencia else 'Outros')
    if not incluir_outros:
        df = df[(df['FORMA_INGRESSO_SIMPLES'] == 'Cotas') | (df['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrência')]

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


def salvar_df(df):
    """
    Função para salvar o DataFrame formatado em um arquivo CSV.
    """
    df.to_csv(r'C:\Dev\dashboard-bsi\dados\processado\dfPrincipal.csv', index=False)


def remover_alunos_anteriores_2013(df, dados_anterior_2013):
    """
    Função para remover alunos que ingressaram antes de 2013.
    """
    if dados_anterior_2013:
        df = df[df['ANO_PERIODO_INGRESSO'].astype(float) >= 2014]
    return df


def agrupar_bairros_por_zona(df):
    """
    Função para agrupar os bairros do Rio de Janeiro por zona.
    """
    zona_norte = ['Abolição', 'Acari', 'Água Santa', 'Alto da Boa Vista', 'Anchieta', 'Andaraí', 'Bancários',
                  'Barros Filho', 'Benfica', 'Bento Ribeiro', 'Bonsucesso', 'Brás de Pina', 'Cachambi', 'Cacuia',
                  'Caju', 'Campinho', 'Cascadura', 'Catumbi', 'Cavalcanti', 'Cidade Universitária', 'Cocotá',
                  'Coelho Neto', 'Colégio', 'Complexo do Alemão', 'Cordovil', 'Costa Barros', 'Del Castilho',
                  'Encantado', 'Engenheiro Leal', 'Engenho da Rainha', 'Engenho de Dentro', 'Engenho Novo', 'Estácio',
                  'Ilha do Governador', 'Galeão', 'Grajaú', 'Guadalupe', 'Higienópolis', 'Honório Gurgel', 'Inhaúma',
                  'Irajá', 'Jacaré', 'Jacarezinho', 'Jardim América', 'Jardim Carioca', 'Jardim Guanabara',
                  'Lins de Vasconcelos', 'Madureira', 'Manguinhos', 'Maracanã', 'Maré', 'Marechal Hermes',
                  'Mangueira', 'Maria da Graça', 'Méier', 'Moneró', 'Olaria', 'Oswaldo Cruz', 'Parada de Lucas',
                  'Parque Anchieta', 'Parque Colúmbia', 'Pavuna', 'Penha', 'Penha Circular', 'Piedade', 'Pilares',
                  'Pitangueiras', 'Portuguesa', 'Praça da Bandeira', 'Praia da Bandeira', 'Quintino Bocaiúva', 'Ramos',
                  'Riachuelo', 'Ribeiro', 'Ricardo de Albuquerque', 'Rocha', 'Rocha Miranda', 'Rocha Neto', 'Sampaio',
                  'Rio Comprido', 'Vasco da Gama', 'São Cristóvão', 'São Francisco Xavier', 'Tauá', 'Tijuca',
                  'Todos os Santos', 'Tomás Coelho', 'Turiaçu', 'Vaz Lobo', 'Vicente de Carvalho', 'Vigário Geral',
                  'Vila Isabel', 'Vila Kosmos', 'Vila da Penha', 'Vista Alegre', 'Vila Kosmos', 'Zumbi']
    zona_oeste = ['Anil', 'Bangu', 'Barra da Tijuca', 'Barra de Guaratiba', 'Camorim', 'Campo dos Afonsos',
                  'Campo Grande', 'Cidade de Deus', 'Cosmos', 'Curicica', 'Deodoro', 'Freguesia (Jacarepaguá)',
                  'Gardênia Azul', 'Gericinó', 'Grumari', 'Guaratiba', 'Ilha de Guaratiba', 'Inhoaíba', 'Itanhangá',
                  'Jabour', 'Jacarepaguá', 'Jardim Sulacap', 'Joá', 'Magalhães Bastos', 'Paciência', 'Padre Miguel',
                  'Pechincha', 'Pedra de Guaratiba', 'Praça Seca', 'Realengo', 'Recreio dos Bandeirantes', 'Santa Cruz',
                  'Santíssimo', 'Senador Camará', 'Senador Vasconcelos', 'Sepetiba', 'Tanque', 'Taquara',
                  'Vargem Grande', 'Vargem Pequena', 'Vila Kennedy', 'Vila Militar', 'Vila Valqueire']

    zona_sul = ['Ipanema', 'Botafogo', 'Catete', 'Copacabana', 'Lagoa', 'Flamengo', 'Gávea', 'Humaitá',
                'Jardim Botânico', 'Laranjeiras', 'Leme', 'Urca', 'Vidigal', 'Cosme Velo', 'São Conrado',
                'Rocinha', 'Leblon']
    baixada_fluminense = ['nova iguacu', 'duque de caxias', 'belford roxo', 'sao joao de meriti', 'nilopolis',
                          'mesquita']
    bairros_centro = ['Gamboa', 'Centro do Rio', 'Lapa', 'Saúde', 'Cidade Nova', 'Santa Teresa', 'Estácio', 'Catumbi',
                      'Santo Cristo', 'Paquetá', 'Glória']

    regiao_serrana = ['Bom Jardim', 'Cantagalo', 'Carmo', 'Cordeiro', 'Duas Barras', 'Macuco', 'Nova Friburgo',
                      'Petrópolis', ' São José do Vale do Rio Preto', 'São Sebastião do Alto', 'Santa Maria Madalena',
                      'Sumidouro', 'Teresópolis' 'Trajano de Morais']

    regiao_dos_lagos = ['cabo frio', 'arraial do cabo', 'araruama', 'saquarema', 'iguaba grande']


def formatar(incluir_outros=True, dados_anterior_2013=False):
    """
    Função principal para formatar e classificar os dados brutos.
    """
    df = ler_dados_brutos()
    df = remover_colunas(df)
    df = preencher_nulos(df)
    df = formatar_periodos(df)
    if dados_anterior_2013:
        df = remover_alunos_anteriores_2013(df, dados_anterior_2013)
    df = converter_tipos(df)
    df = limpar_bairros(df)
    df = limpar_cidades(df)
    df = adicionar_cidade_estado(df)
    df = normalizar_bairros(df)
    df = classificar_idade(df)
    df = classificar_forma_ingresso(df, incluir_outros)
    df = classificar_forma_evasao(df)
    df = arredondar_cra(df)
    df = calcular_tempo_curso(df)

    # Carregar DataFrame de distâncias e calcular/atualizar distâncias
    print('Carregando DataFrame de distâncias do caminho:', pega_caminho_base() + '/dados/processado/dfDistancias.csv')
    df_distancias = carregar_dados(pega_caminho_base() + '/dados/processado/dfDistancias.csv')

    geolocator = inicializar_geolocator()
    df, df_distancias = adicionar_distancia_ate_urca(df, df_distancias, geolocator)

    # Salvar o DataFrame principal e o DataFrame de distâncias atualizados
    salvar_dados(df_distancias, 'dados/processado/dfDistancias.csv')
    salvar_df(df)
    print('DataFrame formatado, classificado e salvo com sucesso!')
    return df


if __name__ == "__main__":
    formatar(False, False)
