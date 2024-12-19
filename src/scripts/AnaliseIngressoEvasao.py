# src/scripts/AnaliseIngressoEvasao.py

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from colorama import Fore, init, Style
from src.utils.plots import salvar_grafico, adicionar_valores_barras, ajustar_estilos_grafico
from src.utils.utils import carregar_dados
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

    def plot_evasao_detalhada_unificada(self):
        """
        Plota a distribuição das formas de evasão unificando todos os períodos.
        """
        print(Fore.YELLOW + "Plotando Evasão Detalhada Unificada..." + Style.RESET_ALL)
        evasao_data = []

        for periodo, df in self.dataframes.items():
            # Filtra os evadidos excluindo 'CON - Curso concluído' e 'Sem evasão'
            evasao_filtrada = df[~df['FORMA_EVASAO_DETALHADA'].isin(['CON - Curso concluído', 'Sem evasão'])]
            evasao_filtrada = evasao_filtrada[['FORMA_EVASAO_DETALHADA', 'FORMA_INGRESSO_SIMPLES']].copy()
            evasao_filtrada['Período'] = self._formatar_nome_periodo(periodo)
            evasao_data.append(evasao_filtrada)

        evasao_combined = pd.concat(evasao_data)

        # Calcula total de evasão
        total_evasao = len(evasao_combined)

        # Agrupa os dados
        evasao_agrupada = evasao_combined.groupby(['FORMA_EVASAO_DETALHADA', 'FORMA_INGRESSO_SIMPLES']).size().reset_index(name='contagem')
        evasao_agrupada['percentual'] = (evasao_agrupada['contagem'] / total_evasao) * 100
        evasao_agrupada['FORMA_EVASAO_DETALHADA'] = evasao_agrupada['FORMA_EVASAO_DETALHADA'].apply(lambda x: x.split()[0])

        # Ordena as categorias de evasão
        ordem_evasao = ['ABA', 'CAN', 'JUB', 'DES']
        evasao_agrupada['FORMA_EVASAO_DETALHADA'] = pd.Categorical(
            evasao_agrupada['FORMA_EVASAO_DETALHADA'],
            categories=ordem_evasao,
            ordered=True
        )

        # Cria o gráfico
        plt.figure(figsize=(12, 6))
        sns.set(style="whitegrid")

        ax = sns.barplot(
            x='FORMA_EVASAO_DETALHADA',
            y='percentual',
            hue='FORMA_INGRESSO_SIMPLES',
            data=evasao_agrupada,
            palette='pastel',
            order=ordem_evasao
        )

        # Adiciona valores nas barras com percentual
        adicionar_valores_barras(ax, exibir_percentual=True, total=total_evasao, fontsize=14)

        # Ajusta estilos do gráfico
        ajustar_estilos_grafico(
            ax,
            title='Evasão Detalhada',
            xlabel='Tipo de Evasão',
            ylabel='Porcentagem de Alunos (%)'
        )

        # Ajusta a legenda para não sobrepor o gráfico
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles=handles, labels=labels, title='Forma de Ingresso', loc='upper left', bbox_to_anchor=(1, 1))

        # Adiciona texto explicativo sobre as siglas
        plt.text(1.02, 0.6, "ABA = Abandono do Curso \nCAN = Cancelamento \nJUB = Jubilamento \nDES = Desistência",
                 ha="left", fontsize=17, transform=ax.transAxes)

        plt.tight_layout()
        salvar_grafico(f'evasao_detalhada_unificada', self.nome_pasta)

    def plot_evasao_cra_arredondado_unificada(self):
        """
        Plota a distribuição da evasão por faixas de CRA arredondado unificando todos os períodos.
        """
        print(Fore.YELLOW + "Plotando Evasão por CRA Arredondado Unificada..." + Style.RESET_ALL)
        evasao_data = []

        for periodo, df in self.dataframes.items():
            # Filtra os evadidos
            evadidos = df[df['STATUS_EVASAO'] == 'Evasão']
            evadidos = evadidos[['CRA_ARREDONDADO', 'FORMA_INGRESSO_SIMPLES']].copy()
            evadidos['Período'] = self._formatar_nome_periodo(periodo)
            evasao_data.append(evadidos)

        evasao_combined = pd.concat(evasao_data)

        # Agrupa os dados
        evasao_agrupada = evasao_combined.groupby(['Período', 'CRA_ARREDONDADO']).size().reset_index(name='Contagem')

        # Cria o gráfico
        plt.figure(figsize=(16, 10))
        sns.set(style="whitegrid")

        ax = sns.barplot(
            x='CRA_ARREDONDADO',
            y='Contagem',
            hue='Período',
            data=evasao_agrupada,
            palette=self.cores_periodos
        )

        # Adiciona valores nas barras
        adicionar_valores_barras(ax, exibir_percentual=False, fontsize=12)

        # Ajusta estilos do gráfico
        ajustar_estilos_grafico(
            ax,
            title='Distribuição da Evasão por CRA Arredondado por Período',
            xlabel='CRA Arredondado',
            ylabel='Número de Alunos Evadidos'
        )

        # Ajusta os ticks do eixo Y para incrementos de 1 até 10
        plt.yticks(ticks=range(0, evasao_agrupada['Contagem'].max() + 1, 1))

        # Ajusta a legenda para não sobrepor o gráfico
        plt.legend(title='Período Temporal', loc='upper right')
        plt.tight_layout()

        salvar_grafico(f'evasao_cra_arredondado_unificada', self.nome_pasta)

    def plot_evasao_por_periodo_curso_unificada(self):
        """
        Plota a distribuição da evasão por período do curso unificando todos os períodos.
        """
        print(Fore.YELLOW + "Plotando Evasão por Período do Curso Unificada..." + Style.RESET_ALL)
        evasao_data = []

        for periodo, df in self.dataframes.items():
            # Filtra os evadidos
            evasao_filtrada = df[df['STATUS_EVASAO'] == 'Evasão']
            evasao_filtrada = evasao_filtrada[['PERIODO_EVASAO', 'FORMA_INGRESSO_SIMPLES']].copy()
            evasao_filtrada['Período'] = self._formatar_nome_periodo(periodo)
            evasao_data.append(evasao_filtrada)

        evasao_combined = pd.concat(evasao_data)

        # Agrupa os dados
        evasao_agrupada = evasao_combined.groupby(['Período', 'PERIODO_EVASAO']).size().reset_index(name='Contagem')

        # Cria o gráfico de linha
        plt.figure(figsize=(16, 10))
        sns.set(style="whitegrid")

        ax = sns.lineplot(
            x='PERIODO_EVASAO',
            y='Contagem',
            hue='Período',
            data=evasao_agrupada,
            marker='o',
            palette=self.cores_periodos
        )

        ajustar_estilos_grafico(
            plt.gca(),
            title='Evasão por Período do Curso por Período Temporal',
            xlabel='Período do Curso',
            ylabel='Número de Alunos Evadidos'
        )

        # Ajusta a legenda para não sobrepor o gráfico
        plt.legend(title='Período Temporal', loc='upper left', bbox_to_anchor=(1, 1))
        plt.tight_layout()

        salvar_grafico(f'evasao_por_periodo_curso_unificada', self.nome_pasta)

    def plot_media_cra_unificada(self):
        """
        Plota a média do CRA por forma de ingresso unificando todos os períodos.
        """
        print(Fore.YELLOW + "Plotando Média do CRA por Forma de Ingresso Unificada..." + Style.RESET_ALL)
        media_cra_data = []

        for periodo, df in self.dataframes.items():
            # Calcula a média de CRA por forma de ingresso
            media_cra = df.groupby(['FORMA_INGRESSO_SIMPLES'])['CRA'].mean().reset_index()
            media_cra['Período'] = self._formatar_nome_periodo(periodo)
            media_cra_data.append(media_cra)

        media_cra_combined = pd.concat(media_cra_data)

        # Cria o gráfico com altura aumentada
        plt.figure(figsize=(16, 12))  # Aumenta a altura para 12
        sns.set(style="whitegrid")

        ax = sns.barplot(
            x='Período',
            y='CRA',
            hue='FORMA_INGRESSO_SIMPLES',
            data=media_cra_combined,
            palette=self.cores_forma_ingresso
        )

        # Adiciona valores nas barras
        adicionar_valores_barras(ax, exibir_percentual=False, fontsize=14)

        # Ajusta estilos do gráfico
        ajustar_estilos_grafico(
            ax,
            title='Média do CRA por Forma de Ingresso por Período Temporal',
            xlabel='Período Temporal',
            ylabel='Média do CRA'
        )

        # Move a legenda para fora do gráfico
        plt.legend(title='Forma de Ingresso', loc='upper left', bbox_to_anchor=(1, 1))
        plt.tight_layout()

        salvar_grafico(f'media_cra_unificada', self.nome_pasta)

    def executar_analises(self):
        """
        Executa todas as análises de ingresso e evasão unificadas.
        """
        self.plot_evasao_detalhada_unificada()
        self.plot_evasao_cra_arredondado_unificada()
        self.plot_evasao_por_periodo_curso_unificada()
        self.plot_media_cra_unificada()

    @staticmethod
    def _formatar_nome_periodo(periodo):
        """
        Formata o nome do período para correspondência com as cores.
        """
        mapeamento = {
            '1_antes_cotas': 'Antes Cotas',
            '2_cotas_2014_2020': 'Cotas 2014-2020',
            '3_pandemia': 'Pandemia',
            '4_pos_pandemia': 'Pos Pandemia'
        }
        return mapeamento.get(periodo, 'Outro')
