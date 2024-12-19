# src/scripts/AnaliseDesempenhoAcademico.py

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from colorama import Fore, init, Style
from src.utils.plots import (
    salvar_grafico,
    adicionar_valores_barras,
    ajustar_estilos_grafico
)
from src.utils.config_cores import ConfigCores

# Inicializa o Colorama
init(autoreset=True)


class AnaliseDesempenhoAcademico:
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

        self.cores_forma_ingresso = self.config_cores.get_cores_forma_ingresso()
        self.cores_grupo = self.config_cores.get_cores_grupo()  # Cores para grupos (Cotistas vs Não Cotistas)
        self.cores_periodos = self.config_cores.get_cores_periodos()  # Cores para períodos temporais
        self.cores_forma_evasao = self.config_cores.get_cores_forma_evasao()  # Cores para formas de evasão

    # ------------------------------
    # Métodos de Plotagem Unificados
    # ------------------------------

    def plot_cras_oscila_periodo_unificado(self):
        """
        Plota um gráfico unificado mostrando a oscilação do CRA médio geral ao longo dos anos de ingresso,
        consolidando todos os períodos temporais.
        """
        try:
            print(Fore.YELLOW + "Plotando Oscilação do CRA Médio Geral ao Longo dos Anos de Ingresso..." + Style.RESET_ALL)

            dados_consolidados = []

            for periodo, df in self.dataframes.items():
                periodo_nome = self._formatar_nome_periodo(periodo)
                print(Fore.BLUE + f"\nProcessando dados para o período: {periodo_nome}" + Style.RESET_ALL)

                dataframe_filtrado = self._filtrar_cra(df)
                if dataframe_filtrado.empty:
                    print(Fore.RED + f"Sem dados válidos para o período {periodo_nome}." + Style.RESET_ALL)
                    continue

                # Calcular a média geral de CRA por ano de ingresso
                cra_medio_geral = dataframe_filtrado.groupby('ANO_PERIODO_INGRESSO')['CRA'].mean().reset_index()
                cra_medio_geral['Período'] = periodo_nome

                # Concatenar os dados
                dados_consolidados.append(cra_medio_geral)

            if not dados_consolidados:
                print(Fore.RED + "Nenhum dado válido encontrado para plotar a oscilação do CRA." + Style.RESET_ALL)
                return

            cra_combined = pd.concat(dados_consolidados, ignore_index=True)

            plt.figure(figsize=(16, 8))
            sns.lineplot(
                data=cra_combined,
                x='ANO_PERIODO_INGRESSO',
                y='CRA',
                hue='Período',
                marker='o',
                palette=self.cores_periodos
            )

            ajustar_estilos_grafico(
                plt.gca(),
                title='Oscilação do CRA Médio Geral ao Longo dos Anos de Ingresso',
                xlabel='Ano de Ingresso',
                ylabel='CRA Médio'
            )
            salvar_grafico('cra_oscila_periodo_unificado', self.nome_pasta)
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em plot_cras_oscila_periodo_unificado: {e}" + Style.RESET_ALL)

    def plot_media_tempo_termino_curso_unificado(self):
        """
        Plota a média de tempo de término do curso unificada, agrupando por período temporal e forma de ingresso.
        """
        try:
            print(Fore.YELLOW + "Plotando Média de Tempo de Término do Curso Unificada..." + Style.RESET_ALL)

            dados_consolidados = []

            for periodo, df in self.dataframes.items():
                periodo_nome = self._formatar_nome_periodo(periodo)
                print(Fore.BLUE + f"\nProcessando dados para o período: {periodo_nome}" + Style.RESET_ALL)

                # Filtra os alunos que concluíram o curso
                dataframe_filtrado = df[(df['STATUS_EVASAO'] == 'Concluído') & df['TEMPO_CURSO'].notnull()]
                if dataframe_filtrado.empty:
                    print(Fore.RED + f"Sem dados válidos para plotar o tempo de término no período {periodo_nome}." + Style.RESET_ALL)
                    continue

                # Calcular a média de tempo de curso por forma de ingresso
                tempo_medio = dataframe_filtrado.groupby('FORMA_INGRESSO_SIMPLES')['TEMPO_CURSO'].mean().reset_index()
                tempo_medio['Período'] = periodo_nome

                dados_consolidados.append(tempo_medio)

            if not dados_consolidados:
                print(Fore.RED + "Nenhum dado válido encontrado para plotar a média de tempo de término do curso." + Style.RESET_ALL)
                return

            tempo_combined = pd.concat(dados_consolidados, ignore_index=True)

            plt.figure(figsize=(14, 8))
            sns.set(style="whitegrid")

            ax = sns.barplot(
                x='Período',
                y='TEMPO_CURSO',
                hue='FORMA_INGRESSO_SIMPLES',
                data=tempo_combined,
                palette=self.cores_forma_ingresso
            )

            # Adiciona valores nas barras
            adicionar_valores_barras(ax, exibir_percentual=False, fontsize=12)

            # Ajusta estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title='Média de Tempo de Término do Curso Unificada',
                xlabel='Período Temporal',
                ylabel='Média de Tempo de Curso (Anos)'
            )

            # Move a legenda para fora do gráfico
            plt.legend(title='Forma de Ingresso', loc='upper left', bbox_to_anchor=(1, 1))
            plt.tight_layout()

            salvar_grafico('media_tempo_termino_curso_unificado', self.nome_pasta)
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em plot_media_tempo_termino_curso_unificado: {e}" + Style.RESET_ALL)

    def plot_media_cra_unificada(self):
        """
        Plota a média do CRA por período temporal, consolidando todos os grupos.
        """
        try:
            print(Fore.YELLOW + "Plotando Média do CRA Unificada por Período Temporal..." + Style.RESET_ALL)

            media_cra_data = []

            for periodo, df in self.dataframes.items():
                periodo_nome = self._formatar_nome_periodo(periodo)
                print(Fore.BLUE + f"\nProcessando dados para o período: {periodo_nome}" + Style.RESET_ALL)

                if 'FORMA_INGRESSO_SIMPLES' not in df.columns or 'CRA' not in df.columns:
                    print(Fore.RED + f"As colunas necessárias não estão presentes no DataFrame para o período {periodo_nome}." + Style.RESET_ALL)
                    continue

                # Calcula a média de CRA geral (sem considerar forma de ingresso)
                cra_medio = df.groupby(['Período Temporal'])['CRA'].mean().reset_index()
                cra_medio['Período'] = periodo_nome
                media_cra_data.append(cra_medio)

            if not media_cra_data:
                print(Fore.RED + "Nenhum dado de média de CRA encontrado para plotar." + Style.RESET_ALL)
                return

            media_cra_combined = pd.concat(media_cra_data, ignore_index=True)
            media_cra_combined.dropna(subset=['CRA', 'Período'], inplace=True)

            plt.figure(figsize=(14, 8))
            sns.set(style="whitegrid")

            ax = sns.barplot(
                x='Período',
                y='CRA',
                data=media_cra_combined,
                palette=self.cores_periodos
            )

            # Adiciona valores nas barras
            adicionar_valores_barras(ax, exibir_percentual=False, fontsize=12)

            # Ajusta estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title='Média do CRA Unificada por Período Temporal',
                xlabel='Período Temporal',
                ylabel='Média do CRA'
            )

            # Move a legenda para fora do gráfico (não há hue, então não é necessário)
            plt.tight_layout()

            salvar_grafico('media_cra_unificada', self.nome_pasta)
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em plot_media_cra_unificada: {e}" + Style.RESET_ALL)

    # ------------------------------
    # Métodos de Análise de Resultados Gerais
    # ------------------------------

    def plot_distribuicao_alunos_por_zona_unificada(self):
        """
        Plota a distribuição percentual de alunos por zona geográfica unificada, segmentado por cotistas e não cotistas.
        """
        try:
            print(Fore.YELLOW + "Plotando Distribuição de Alunos por Zona Geográfica Unificada..." + Style.RESET_ALL)
            dados_consolidados = []

            for periodo, df in self.dataframes.items():
                periodo_nome = self._formatar_nome_periodo(periodo)
                print(Fore.BLUE + f"\nProcessando dados para o período: {periodo_nome}" + Style.RESET_ALL)

                if 'ZONA' not in df.columns or 'FORMA_INGRESSO_SIMPLES' not in df.columns:
                    print(Fore.RED + f"As colunas 'ZONA' ou 'FORMA_INGRESSO_SIMPLES' não existem no DataFrame para o período {periodo_nome}." + Style.RESET_ALL)
                    continue

                grupo_cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Cotas']
                grupo_nao_cotistas = df[df['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia']

                zonas = df['ZONA'].unique()

                for zona in zonas:
                    total_cotistas_zona = grupo_cotistas[grupo_cotistas['ZONA'] == zona].shape[0]
                    total_nao_cotistas_zona = grupo_nao_cotistas[grupo_nao_cotistas['ZONA'] == zona].shape[0]

                    total_cotistas = grupo_cotistas.shape[0]
                    total_nao_cotistas = grupo_nao_cotistas.shape[0]

                    porcentagem_cotistas = (total_cotistas_zona / total_cotistas) * 100 if total_cotistas > 0 else 0
                    porcentagem_nao_cotistas = (total_nao_cotistas_zona / total_nao_cotistas) * 100 if total_nao_cotistas > 0 else 0

                    dados_consolidados.append({
                        'Zona': zona,
                        'Grupo': 'Cotistas',
                        'Porcentagem': porcentagem_cotistas,
                        'Período': periodo_nome
                    })
                    dados_consolidados.append({
                        'Zona': zona,
                        'Grupo': 'Não Cotistas',
                        'Porcentagem': porcentagem_nao_cotistas,
                        'Período': periodo_nome
                    })

            if not dados_consolidados:
                print(Fore.RED + "Nenhum dado válido encontrado para plotar a distribuição por zona." + Style.RESET_ALL)
                return

            df_consolidado_zona = pd.DataFrame(dados_consolidados)

            plt.figure(figsize=(16, 8))
            sns.set(style="whitegrid")

            ax = sns.barplot(
                x='Zona',
                y='Porcentagem',
                hue='Grupo',
                data=df_consolidado_zona,
                palette=self.cores_grupo,
                ci=None
            )

            # Adiciona valores nas barras
            adicionar_valores_barras(ax, exibir_percentual=True, fontsize=12, offset=8)

            # Ajusta estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title='Distribuição de Alunos por Zona Geográfica Unificada',
                xlabel='Zona Geográfica',
                ylabel='Porcentagem (%)'
            )

            # Move a legenda para fora do gráfico
            plt.legend(title='Grupo', loc='upper left', bbox_to_anchor=(1, 1))
            plt.tight_layout()

            salvar_grafico('distribuicao_alunos_por_zona_unificada', self.nome_pasta)
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em plot_distribuicao_alunos_por_zona_unificada: {e}" + Style.RESET_ALL)

    # -----------------------------------
    # Métodos Auxiliares
    # -----------------------------------

    def _filtrar_cra(self, df):
        """
        Filtra o DataFrame para remover registros com CRA nulo.
        :param df: DataFrame original.
        :return: DataFrame filtrado.
        """
        return df[df['CRA'].notnull()]

    def _calcular_media_cra_por_ano_ingresso(self, df):
        """
        Calcula a média do CRA agrupando por ano de ingresso e forma de ingresso.
        :param df: DataFrame filtrado.
        :return: DataFrame com a média do CRA.
        """
        return df.groupby(['ANO_PERIODO_INGRESSO', 'FORMA_INGRESSO_SIMPLES'])['CRA'].mean().reset_index()

    # -----------------------------------
    # Método Principal para Executar Análises
    # -----------------------------------

    def executar_analises(self):
        """
        Executa todas as análises de desempenho acadêmico unificadas.
        """
        # Plotagem unificada do CRA médio geral
        self.plot_cras_oscila_periodo_unificado()

        # Plotagem unificada da média de tempo de término do curso
        self.plot_media_tempo_termino_curso_unificado()

        # Plotagem unificada da média do CRA
        self.plot_media_cra_unificada()

        # Plotagem unificada da distribuição de alunos por zona geográfica
        self.plot_distribuicao_alunos_por_zona_unificada()

        # Removidos os gráficos indesejados:
        # self.plot_distribuicao_cra()
        # self.plot_distribuicao_cra_sexo()
        # self.plot_impacto_cra_evasao()

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