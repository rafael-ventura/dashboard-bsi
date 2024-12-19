# src/scripts/AnaliseIngressoEvasao.py

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from colorama import Fore, init, Style
from src.utils.plots import salvar_grafico, adicionar_valores_barras, ajustar_estilos_grafico
from src.utils.config_cores import ConfigCores

# Inicializa o Colorama
init(autoreset=True)


class AnaliseIngressoEvasao:
    def __init__(self, dataframes, nome_pasta, config_cores=None):
        """
        Inicializa a classe com os dataframes de cada período e o nome da pasta para salvar os gráficos.

        :param dataframes: Dicionário com os dataframes segmentados por período.
        :param nome_pasta: Nome da pasta onde os gráficos serão salvos.
        :param config_cores: Instância da classe ConfigCores (opcional).
        """
        self.dataframes = dataframes
        self.nome_pasta = nome_pasta

        # Carrega as paletas de cores
        if config_cores is None:
            self.config_cores = ConfigCores()
        else:
            self.config_cores = config_cores

        self.cores_periodos = self.config_cores.get_cores_periodos()
        self.cores_forma_ingresso = self.config_cores.get_cores_forma_ingresso()

        # Define uma paleta de cores para os tipos de evasão detalhada
        self.cores_forma_evasao = self.config_cores.get_cores_forma_evasao()

        # Define uma paleta de cores para os status de evasão
        self.cores_status_evasao = self.config_cores.get_cores_status_evasao()

    def plot_evasao_detalhada_unificada_countplot(self):
        """
        Plota a distribuição das formas de evasão detalhada unificando todos os períodos,
        utilizando um countplot para mostrar a distribuição.
        """
        try:
            print(Fore.YELLOW + "Plotando Evasão Detalhada Unificada com Count Plot..." + Style.RESET_ALL)
            evasao_data = []

            for periodo, df in self.dataframes.items():
                # Verifica se as colunas necessárias existem
                if 'FORMA_EVASAO_DETALHADA' not in df.columns or 'FORMA_INGRESSO_SIMPLES' not in df.columns:
                    print(Fore.RED + f"As colunas necessárias não estão presentes no DataFrame para o período {periodo}." + Style.RESET_ALL)
                    continue

                # Filtra as formas de evasão relevantes
                evasao_filtrada = df[~df['FORMA_EVASAO_DETALHADA'].isin(['CON - Curso concluído', 'Sem evasão'])].copy()
                evasao_filtrada = evasao_filtrada[['FORMA_EVASAO_DETALHADA', 'FORMA_INGRESSO_SIMPLES']].copy()
                evasao_filtrada['Período'] = self._formatar_nome_periodo(periodo)

                # Simplifica os tipos de evasão detalhada
                evasao_filtrada['FORMA_EVASAO_DETALHADA'] = evasao_filtrada['FORMA_EVASAO_DETALHADA'].apply(
                    lambda x: 'DES' if 'Desistência' in x else (x.split()[0] if isinstance(x, str) and ' ' in x else 'DES')
                )
                evasao_data.append(evasao_filtrada)

            if not evasao_data:
                print(Fore.RED + "Nenhum dado de evasão filtrado encontrado para plotar." + Style.RESET_ALL)
                return

            evasao_combined = pd.concat(evasao_data, ignore_index=True)
            evasao_combined.dropna(subset=['FORMA_EVASAO_DETALHADA', 'FORMA_INGRESSO_SIMPLES', 'Período'], inplace=True)

            # Define a ordem das categorias de evasão detalhada
            ordem_evasao = ['DES', 'CAN', 'JUB', 'TIC', 'FAL', 'ABA']
            evasao_combined['FORMA_EVASAO_DETALHADA'] = pd.Categorical(
                evasao_combined['FORMA_EVASAO_DETALHADA'],
                categories=ordem_evasao,
                ordered=True
            )

            # Cria o gráfico de countplot
            plt.figure(figsize=(14, 8))
            sns.set(style="whitegrid")

            ax = sns.countplot(
                data=evasao_combined,
                x='Período',
                hue='FORMA_EVASAO_DETALHADA',
                palette=self.cores_forma_evasao
            )

            # Ajusta títulos e labels
            plt.title('Distribuição das Formas de Evasão Detalhada por Período Temporal')
            plt.xlabel('Período Temporal')
            plt.ylabel('Número de Alunos Evadidos')

            # Ajusta a legenda para evitar sobreposição
            plt.legend(title='Tipo de Evasão', bbox_to_anchor=(1.15, 1), loc='upper left')

            # Adiciona texto explicativo sobre as siglas
            plt.text(1.02, 0.6, "ABA = Abandono do Curso \nCAN = Cancelamento \nJUB = Jubilamento \nDES = Desistência \nTIC = Transferência Interna \nFAL = Falecimento do discente",
                     ha="left", fontsize=12, transform=plt.gca().transAxes)

            plt.tight_layout()
            salvar_grafico('evasao_detalhada_unificada_countplot', self.nome_pasta)
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em plot_evasao_detalhada_unificada_countplot: {e}" + Style.RESET_ALL)

    def plot_evasao_cumulativa_por_periodo(self):
        """
        Plota a evasão cumulativa por período do curso para destacar os primeiros períodos.
        """
        try:
            print(Fore.YELLOW + "Plotando Evasão Cumulativa por Período do Curso..." + Style.RESET_ALL)
            evasao_data = []

            for periodo, df in self.dataframes.items():
                if 'STATUS_EVASAO' not in df.columns or 'TEMPO_CURSO' not in df.columns or 'FORMA_INGRESSO_SIMPLES' not in df.columns:
                    print(Fore.RED + f"As colunas necessárias não estão presentes no DataFrame para o período {periodo}." + Style.RESET_ALL)
                    continue

                evasao_filtrada = df[df['STATUS_EVASAO'] == 'Evasão'].copy()
                evasao_filtrada['PERIODO_EVASAO'] = (evasao_filtrada['TEMPO_CURSO'] * 2).round().astype(int)

                # Filtra os períodos do curso entre 1 e 12
                evasao_filtrada = evasao_filtrada[
                    (evasao_filtrada['PERIODO_EVASAO'] >= 1) &
                    (evasao_filtrada['PERIODO_EVASAO'] <= 12)
                    ]

                evasao_filtrada = evasao_filtrada[['PERIODO_EVASAO']].copy()
                evasao_filtrada['Período'] = self._formatar_nome_periodo(periodo)
                evasao_data.append(evasao_filtrada)

            if not evasao_data:
                print(Fore.RED + "Nenhum dado de evasão filtrado encontrado para plotar evasão cumulativa." + Style.RESET_ALL)
                return

            evasao_combined = pd.concat(evasao_data, ignore_index=True)
            evasao_combined.dropna(subset=['PERIODO_EVASAO', 'Período'], inplace=True)

            # Agrupa os dados por PERIODO_EVASAO e Período Temporal
            evasao_agrupada = evasao_combined.groupby(['Período', 'PERIODO_EVASAO']).size().reset_index(name='Contagem')

            # Ordena os períodos do curso de 1 a 12
            evasao_agrupada['PERIODO_EVASAO'] = evasao_agrupada['PERIODO_EVASAO'].astype(int)
            evasao_agrupada = evasao_agrupada.sort_values('PERIODO_EVASAO')

            # Calcula a evasão cumulativa
            evasao_agrupada['Contagem_Cumulativa'] = evasao_agrupada.groupby('Período')['Contagem'].cumsum()

            # Cria o gráfico de linha
            plt.figure(figsize=(14, 8))
            sns.set(style="whitegrid")

            ax = sns.lineplot(
                data=evasao_agrupada,
                x='PERIODO_EVASAO',
                y='Contagem_Cumulativa',
                hue='Período',
                marker='o',
                palette=self.cores_periodos
            )

            plt.title('Evasão Cumulativa por Período do Curso e Período Temporal')
            plt.xlabel('Período do Curso')
            plt.ylabel('Número Cumulativo de Evasões')

            # Ajusta os ticks do eixo X para mostrar de 1 em 1
            plt.xticks(ticks=range(1, 13, 1))

            plt.legend(title='Período Temporal', bbox_to_anchor=(1.05, 1), loc='upper left')

            # Destacar os primeiros períodos com maior evasão
            for periodo in evasao_agrupada['Período'].unique():
                subset = evasao_agrupada[evasao_agrupada['Período'] == periodo]
                max_evasao = subset['Contagem_Cumulativa'].max()
                plt.text(subset['PERIODO_EVASAO'].iloc[-1], max_evasao, periodo,
                         horizontalalignment='left', size='medium',
                         color=self.cores_periodos.get(periodo, 'black'), weight='semibold')

            plt.tight_layout()
            salvar_grafico('evasao_cumulativa_por_periodo', self.nome_pasta)
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em plot_evasao_cumulativa_por_periodo: {e}" + Style.RESET_ALL)

    def plot_media_cra_unificada(self):
        """
        Plota a média do CRA por forma de ingresso unificando todos os períodos temporais,
        mantendo a legenda fora e ajustando o tamanho.
        """
        try:
            print(Fore.YELLOW + "Plotando Média do CRA por Forma de Ingresso Unificada..." + Style.RESET_ALL)
            media_cra_data = []

            for periodo, df in self.dataframes.items():
                if 'FORMA_INGRESSO_SIMPLES' not in df.columns or 'CRA' not in df.columns:
                    print(Fore.RED + f"As colunas necessárias não estão presentes no DataFrame para o período {periodo}." + Style.RESET_ALL)
                    continue

                # Calcula a média de CRA por forma de ingresso
                media_cra = df.groupby(['FORMA_INGRESSO_SIMPLES'])['CRA'].mean().reset_index()
                media_cra['Período'] = self._formatar_nome_periodo(periodo)
                media_cra_data.append(media_cra)

            if not media_cra_data:
                print(Fore.RED + "Nenhum dado de média de CRA encontrado para plotar." + Style.RESET_ALL)
                return

            media_cra_combined = pd.concat(media_cra_data, ignore_index=True)
            media_cra_combined.dropna(subset=['FORMA_INGRESSO_SIMPLES', 'CRA', 'Período'], inplace=True)

            # Cria o gráfico com tamanho ajustado
            plt.figure(figsize=(14, 8))  # Ajuste o tamanho conforme necessário
            sns.set(style="whitegrid")

            ax = sns.barplot(
                x='Período',
                y='CRA',
                hue='FORMA_INGRESSO_SIMPLES',
                data=media_cra_combined,
                palette=self.cores_forma_ingresso
            )

            # Adiciona valores nas barras
            adicionar_valores_barras(ax, exibir_percentual=False, fontsize=12)

            # Ajusta estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title='Média do CRA por Forma de Ingresso Unificada',
                xlabel='Período Temporal',
                ylabel='Média do CRA'
            )

            # Move a legenda para fora do gráfico
            plt.legend(title='Forma de Ingresso', loc='upper left', bbox_to_anchor=(1, 1))
            plt.tight_layout()

            salvar_grafico('media_cra_unificada', self.nome_pasta)
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em plot_media_cra_unificada: {e}" + Style.RESET_ALL)

    def plot_porcentagem_evasao_status_por_grupo_temporal(self):
        """
        Plota a porcentagem de alunos agrupados por 'STATUS_EVASAO' de acordo com os grupos temporais.
        """
        try:
            print(Fore.YELLOW + "Plotando Porcentagem de Evasão por Status e Grupo Temporal..." + Style.RESET_ALL)
            evasao_data = []

            for periodo, df in self.dataframes.items():
                periodo_nome = self._formatar_nome_periodo(periodo)
                print(Fore.BLUE + f"\nProcessando dados para o período: {periodo_nome}" + Style.RESET_ALL)

                # Verifica se as colunas necessárias existem
                if 'STATUS_EVASAO' not in df.columns:
                    print(Fore.RED + f"A coluna 'STATUS_EVASAO' não está presente no DataFrame para o período {periodo_nome}." + Style.RESET_ALL)
                    continue

                # Filtra apenas os registros com evasão nas categorias relevantes
                evasao_filtrada = df[df['STATUS_EVASAO'].isin(['Cursando', 'Evasão', 'Concluído'])].copy()

                if evasao_filtrada.empty:
                    print(Fore.RED + f"Não há registros de evasão para o período {periodo_nome}." + Style.RESET_ALL)
                    continue

                # Agrupa por 'STATUS_EVASao' e calcula a contagem
                contagem_evasao = evasao_filtrada['STATUS_EVASAO'].value_counts().reset_index()
                contagem_evasao.columns = ['STATUS_EVASAO', 'Contagem']

                # Calcula o total de evasões no período
                total_evasoes = contagem_evasao['Contagem'].sum()

                # Calcula a porcentagem
                contagem_evasao['Porcentagem'] = (contagem_evasao['Contagem'] / total_evasoes) * 100
                contagem_evasao['Período'] = periodo_nome

                evasao_data.append(contagem_evasao)

            if not evasao_data:
                print(Fore.RED + "Nenhum dado de evasão encontrado para plotar a porcentagem por status." + Style.RESET_ALL)
                return

            # Concatena todos os dados
            evasao_combined = pd.concat(evasao_data, ignore_index=True)

            # Define a ordem das categorias de evasão
            ordem_evasao = ['Cursando', 'Evasão', 'Concluído']
            evasao_combined['STATUS_EVASAO'] = pd.Categorical(
                evasao_combined['STATUS_EVASAO'],
                categories=ordem_evasao,
                ordered=True
            )

            # Cria o gráfico de barras agrupadas
            plt.figure(figsize=(16, 8))
            sns.set(style="whitegrid")

            ax = sns.barplot(
                data=evasao_combined,
                x='Período',
                y='Porcentagem',
                hue='STATUS_EVASAO',
                palette=self.cores_status_evasao
            )

            # Adiciona valores percentuais nas barras
            adicionar_valores_barras(ax, exibir_percentual=True, fontsize=12, offset=1.5)

            # Ajusta títulos e labels
            plt.title('Porcentagem de Alunos por Status de Evasão por Grupo Temporal')
            plt.xlabel('Grupo Temporal')
            plt.ylabel('Porcentagem (%)')

            # Ajusta a legenda para evitar sobreposição
            plt.legend(title='Status de Evasão', bbox_to_anchor=(1.05, 1), loc='upper left')

            plt.tight_layout()
            salvar_grafico('porcentagem_evasao_status_por_grupo_temporal', self.nome_pasta)
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em plot_porcentagem_evasao_status_por_grupo_temporal: {e}" + Style.RESET_ALL)

    def executar_analises(self):
        """
        Executa todas as análises de ingresso e evasão unificadas.
        """
        self.plot_media_cra_unificada()
        self.plot_evasao_detalhada_unificada_countplot()
        self.plot_evasao_cumulativa_por_periodo()
        self.plot_porcentagem_evasao_status_por_grupo_temporal()  # Chamada do novo método

    @staticmethod
    def _formatar_nome_periodo(periodo):
        """
        Formata o nome do período para correspondência com as cores.

        :param periodo: Identificador do período (ex: '1_antes_cotas').
        :return: Nome legível do período.
        """
        mapeamento = {
            '1_antes_cotas': 'Antes Cotas',
            '2_cotas_2014_2020': 'Cotas 2014-2020',
            '3_pandemia': 'Pandemia',
            '4_pos_pandemia': 'Pos Pandemia'
        }
        return mapeamento.get(periodo, 'Outro')
