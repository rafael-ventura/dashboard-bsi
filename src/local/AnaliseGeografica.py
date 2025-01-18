# src/scripts/AnaliseGeografica.py

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from colorama import Fore, Style
from src.utils.plots import (
    salvar_grafico,
    ajustar_estilos_grafico,
    adicionar_valores_barras
)
from src.utils.utils import (
    remover_acentos_e_maiusculas,
    pega_caminho_base
)
from src.formatacao.zonas_geograficas import (
    zona_norte,
    zona_oeste,
    zona_sul,
    bairros_centro,
    baixada_fluminense,
    regiao_volta_redonda,
    niteroi_sao_goncalo,
    regiao_serrana,
    regiao_campos,
    regiao_dos_lagos
)

# Inicializa o Colorama
from colorama import init

init(autoreset=True)


class AnaliseGeografica:
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
            from src.utils.config_cores import ConfigCores
            self.config_cores = ConfigCores()
        else:
            self.config_cores = config_cores

        self.cores_periodos = self.config_cores.get_cores_periodos()
        self.cores_forma_ingresso = self.config_cores.get_cores_forma_ingresso()
        self.cores_grupo = self.config_cores.get_cores_grupo()

    # -----------------------------------
    # Método Principal para Executar Análises Geográficas Unificadas
    # -----------------------------------

    def executar_analises_geograficas(self):
        """
        Executa todas as análises geográficas unificadas, combinando os quatro períodos temporais em cada gráfico.
        """
        try:
            print(Fore.BLUE + "\nIniciando Análises Geográficas Unificadas..." + Style.RESET_ALL)

            # Preparar dados unificados
            df_unificado = self.preparar_dados_unificados()

            if df_unificado.empty:
                print(Fore.RED + "Nenhum dado disponível para gerar os gráficos unificados." + Style.RESET_ALL)
                return

            # Plotagem de Gráficos Unificados
            self.plot_top_bairros_com_mais_alunos(df_unificado)
            self.plot_distribuicao_alunos_por_zona_unificada(df_unificado)
            self.plot_correlacao_cra_alunos_concluintes(df_unificado)
            self.plot_heatmap_faceted(df_unificado)

            print(Fore.GREEN + "Análises Geográficas Unificadas Concluídas!" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em executar_analises_geograficas: {e}" + Style.RESET_ALL)

    # -----------------------------------
    # Métodos de Preparação de Dados Unificados
    # -----------------------------------

    def preparar_dados_unificados(self):
        """
        Consolida os dados de todos os períodos temporais em um único DataFrame para análise unificada.

        :return: DataFrame consolidado com todos os períodos.
        """
        try:
            print(Fore.CYAN + "Preparando dados unificados para análise..." + Style.RESET_ALL)
            dados_unificados = []

            for periodo, df in self.dataframes.items():
                periodo_nome = self._formatar_nome_periodo(periodo)
                print(Fore.BLUE + f"Processando período: {periodo_nome}" + Style.RESET_ALL)

                # Remover alunos com bairro desconhecido e fora do Rio de Janeiro
                df_periodo = df[(df['BAIRRO'] != 'desconhecido') & (df['CIDADE'] == 'rio de janeiro')]

                # Verifica se existem alunos no período
                if df_periodo.empty:
                    print(Fore.RED + f"Sem dados de alunos para o período: {periodo_nome}" + Style.RESET_ALL)
                    continue

                # Normaliza os nomes dos bairros
                df_periodo['BAIRRO'] = df_periodo['BAIRRO'].apply(remover_acentos_e_maiusculas)

                # Categorização da Zona Geográfica
                df_periodo['ZONA_GEOGRAFICA'] = df_periodo['BAIRRO'].apply(self.categorizar_zona)

                # Adiciona o nome do período
                df_periodo['Período'] = periodo_nome

                dados_unificados.append(df_periodo)

            if not dados_unificados:
                print(Fore.RED + "Nenhum dado unificado foi preparado." + Style.RESET_ALL)
                return pd.DataFrame()

            df_unificado = pd.concat(dados_unificados, ignore_index=True)
            print(Fore.CYAN + "Dados unificados preparados com sucesso." + Style.RESET_ALL)
            return df_unificado

        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro em preparar_dados_unificados: {e}" + Style.RESET_ALL)
            return pd.DataFrame()

    def categorizar_zona(self, bairro):
        """
        Categoriza o bairro em uma zona geográfica predefinida.

        :param bairro: Nome do bairro.
        :return: Nome da zona geográfica.
        """
        bairro_normalizado = remover_acentos_e_maiusculas(bairro)
        if bairro_normalizado in [remover_acentos_e_maiusculas(b) for b in zona_norte]:
            return 'Zona Norte'
        elif bairro_normalizado in [remover_acentos_e_maiusculas(b) for b in zona_oeste]:
            return 'Zona Oeste'
        elif bairro_normalizado in [remover_acentos_e_maiusculas(b) for b in zona_sul]:
            return 'Zona Sul'
        elif bairro_normalizado in [remover_acentos_e_maiusculas(b) for b in bairros_centro]:
            return 'Centro'
        elif bairro_normalizado in [remover_acentos_e_maiusculas(b) for b in baixada_fluminense]:
            return 'Baixada Fluminense'
        elif bairro_normalizado in [remover_acentos_e_maiusculas(b) for b in regiao_volta_redonda]:
            return 'Região Volta Redonda'
        elif bairro_normalizado in [remover_acentos_e_maiusculas(b) for b in niteroi_sao_goncalo]:
            return 'Niterói/São Gonçalo'
        elif bairro_normalizado in [remover_acentos_e_maiusculas(b) for b in regiao_serrana]:
            return 'Região Serrana'
        elif bairro_normalizado in [remover_acentos_e_maiusculas(b) for b in regiao_campos]:
            return 'Região Campos'
        elif bairro_normalizado in [remover_acentos_e_maiusculas(b) for b in regiao_dos_lagos]:
            return 'Região dos Lagos'
        else:
            return 'Fora do Estado'

    # -----------------------------------
    # Métodos de Plotagem Geográfica Unificados
    # -----------------------------------

    def plot_top_bairros_com_mais_alunos(self, df_unificado, top_n=3):
        """
        Plota os bairros com maior número de alunos, indicando a concentração em poucos bairros.

        :param df_unificado: DataFrame consolidado com todos os períodos.
        :param top_n: Número de bairros a serem exibidos.
        """
        try:
            print(Fore.YELLOW + "Plotando Top Bairros com Mais Alunos (Unificado)..." + Style.RESET_ALL)

            # Contagem total de alunos por bairro
            contagem_total = df_unificado['BAIRRO'].value_counts().reset_index()
            contagem_total.columns = ['BAIRRO', 'QUANTIDADE']

            # Seleciona os top_n bairros
            top_bairros = contagem_total.head(top_n)

            # Adiciona 'Outros' para os demais bairros
            outros = contagem_total['QUANTIDADE'].sum() - top_bairros['QUANTIDADE'].sum()
            top_bairros = top_bairros.append({'BAIRRO': 'Outros', 'QUANTIDADE': outros}, ignore_index=True)

            plt.figure(figsize=(12, 8))
            sns.set(style="whitegrid")

            ax = sns.barplot(
                x='BAIRRO',
                y='QUANTIDADE',
                data=top_bairros,
                palette=self.cores_periodos[:top_n] + ['grey']  # Adiciona cor cinza para 'Outros'
            )

            adicionar_valores_barras(ax, exibir_percentual=False, fontsize=12)

            ajustar_estilos_grafico(
                ax,
                title=f'Top {top_n} Bairros com Mais Alunos - Unificado por Período',
                xlabel='Bairro',
                ylabel='Quantidade de Alunos'
            )

            plt.tight_layout()

            salvar_grafico(f'top_{top_n}_bairros_com_mais_alunos_unificado', self.nome_pasta)
            plt.close()
            print(Fore.CYAN + "Gráfico de Top Bairros com Mais Alunos (Unificado) salvo com sucesso." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em plot_top_bairros_com_mais_alunos: {e}" + Style.RESET_ALL)

    def plot_distribuicao_alunos_por_zona_unificada(self, df_unificado):
        """
        Plota a distribuição dos alunos por zona geográfica unificada.

        :param df_unificado: DataFrame consolidado com todos os períodos.
        """
        try:
            print(Fore.YELLOW + "Plotando Distribuição de Alunos por Zona Geográfica (Unificado)..." + Style.RESET_ALL)

            # Contagem de alunos por zona e período
            contagem_zona = df_unificado.groupby(['Período', 'ZONA_GEOGRAFICA']).size().reset_index(name='QUANTIDADE')

            # Calcular o percentual por período
            contagem_zona['TOTAL_PERIODO'] = contagem_zona.groupby('Período')['QUANTIDADE'].transform('sum')
            contagem_zona['PERCENTUAL'] = (contagem_zona['QUANTIDADE'] / contagem_zona['TOTAL_PERIODO']) * 100

            plt.figure(figsize=(16, 10))
            sns.set(style="whitegrid")

            ax = sns.barplot(
                x='ZONA_GEOGRAFICA',
                y='PERCENTUAL',
                hue='Período',
                data=contagem_zona,
                palette=self.cores_periodos
            )

            adicionar_valores_barras(ax, exibir_percentual=True, fontsize=12)

            ajustar_estilos_grafico(
                ax,
                title='Distribuição Percentual de Alunos por Zona Geográfica - Unificado por Período',
                xlabel='Zona Geográfica',
                ylabel='Percentual de Alunos (%)'
            )

            plt.legend(title='Período Temporal', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()

            salvar_grafico('distribuicao_alunos_por_zona_unificada', self.nome_pasta)
            plt.close()
            print(Fore.CYAN + "Gráfico de Distribuição de Alunos por Zona Geográfica (Unificado) salvo com sucesso." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em plot_distribuicao_alunos_por_zona_unificada: {e}" + Style.RESET_ALL)

    def plot_correlacao_cra_alunos_concluintes(self, df_unificado):
        """
        Plota a correlação entre CRA e outra variável relevante para alunos que concluíram a faculdade.

        :param df_unificado: DataFrame consolidado com todos os períodos.
        """
        try:
            print(Fore.YELLOW + "Plotando Correlação do CRA dos Alunos que Concluíram a Faculdade..." + Style.RESET_ALL)

            # Filtrar alunos que concluíram a faculdade
            df_concluintes = df_unificado[df_unificado['STATUS_EVASAO'] == 'Concluído']

            if df_concluintes.empty:
                print(Fore.RED + "Nenhum dado disponível para alunos concluintes." + Style.RESET_ALL)
                return

            # Supondo que exista uma coluna 'DISTANCIA_URCA' para correlacionar com CRA
            if 'DISTANCIA_URCA' not in df_concluintes.columns:
                print(Fore.RED + "A coluna 'DISTANCIA_URCA' não está presente no DataFrame." + Style.RESET_ALL)
                return

            plt.figure(figsize=(14, 10))
            sns.set(style="whitegrid")

            ax = sns.scatterplot(
                x='DISTANCIA_URCA',
                y='CRA',
                hue='Período',
                data=df_concluintes,
                palette=self.cores_periodos,
                alpha=0.6
            )

            # Calcular e exibir a correlação
            correlacao = df_concluintes[['DISTANCIA_URCA', 'CRA']].corr().iloc[0, 1]
            plt.annotate(f'Correlação: {correlacao:.2f}', xy=(0.05, 0.95), xycoords='axes fraction',
                         fontsize=14, color='black', backgroundcolor='white')

            ajustar_estilos_grafico(
                ax,
                title='Correlação entre Distância da Urca e CRA dos Alunos Concluintes - Unificado por Período',
                xlabel='Distância até a Urca (km)',
                ylabel='CRA'
            )

            plt.legend(title='Período Temporal', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()

            salvar_grafico('correlacao_cra_alunos_concluintes_unificado', self.nome_pasta)
            plt.close()
            print(Fore.CYAN + "Gráfico de Correlação do CRA dos Alunos Concluintes (Unificado) salvo com sucesso." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em plot_correlacao_cra_alunos_concluintes: {e}" + Style.RESET_ALL)

    def plot_heatmap_faceted(self, df_unificado):
        """
        Plota um heatmap facetado para melhorar a visualização.

        :param df_unificado: DataFrame consolidado com todos os períodos.
        """
        try:
            print(Fore.YELLOW + "Plotando Heatmap Faceted..." + Style.RESET_ALL)

            # Supondo que queremos um heatmap da contagem de alunos por bairro e período
            contagem_heatmap = df_unificado.groupby(['Período', 'BAIRRO']).size().reset_index(name='QUANTIDADE')

            # Pivotar para formato adequado para heatmap
            pivot_heatmap = contagem_heatmap.pivot("BAIRRO", "Período", "QUANTIDADE")

            plt.figure(figsize=(20, 15))
            sns.set(style="white")

            ax = sns.heatmap(pivot_heatmap, annot=True, fmt="d", cmap="YlGnBu", linewidths=.5)

            ajustar_estilos_grafico(
                ax,
                title='Heatmap de Quantidade de Alunos por Bairro e Período',
                xlabel='Período Temporal',
                ylabel='Bairro'
            )

            plt.tight_layout()

            salvar_grafico('heatmap_quantidade_alunos_por_bairro_e_periodo', self.nome_pasta)
            plt.close()
            print(Fore.CYAN + "Heatmap Faceted salvo com sucesso." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em plot_heatmap_faceted: {e}" + Style.RESET_ALL)

    # -----------------------------------
    # Métodos Auxiliares
    # -----------------------------------

    def preparar_dados_bairros(self, df, bairros_rj):
        """
        Prepara os dados de bairros para plotagem, lidando com casos de bairros desconhecidos ou fora do RJ.

        :param df: DataFrame filtrado para o período.
        :param bairros_rj: GeoDataFrame com os dados geográficos dos bairros do RJ.
        :return: GeoDataFrame preparado com contagem de alunos por bairro.
        """
        try:
            print(Fore.CYAN + "Preparando dados de bairros..." + Style.RESET_ALL)

            # Normaliza os nomes dos bairros para garantir correspondência
            df['BAIRRO'] = df['BAIRRO'].apply(remover_acentos_e_maiusculas)
            bairros_rj['nome'] = bairros_rj['nome'].apply(remover_acentos_e_maiusculas)

            # Faz a contagem de alunos por bairro
            contagem_alunos = df['BAIRRO'].value_counts().reset_index()
            contagem_alunos.columns = ['nome', 'ALUNOS']

            # Identifica os bairros que estão no GeoDataFrame, mas não no DataFrame de alunos
            bairros_faltantes = set(bairros_rj['nome']) - set(contagem_alunos['nome'])
            print("\nBairros faltantes no DataFrame de alunos:")
            print(bairros_faltantes)

            # Adiciona os bairros faltantes com contagem 0 ao DataFrame de contagem de alunos
            if bairros_faltantes:
                bairros_faltantes_df = pd.DataFrame({
                    'nome': list(bairros_faltantes),
                    'ALUNOS': [0] * len(bairros_faltantes)
                })
                contagem_alunos = pd.concat([contagem_alunos, bairros_faltantes_df], ignore_index=True)

            # Faz o merge dos bairros, garantindo que todos os bairros tenham uma contagem
            bairros_rj_merged = bairros_rj.merge(contagem_alunos, on='nome', how='left')

            # Preenche os valores NaN na coluna 'ALUNOS' com 0
            bairros_rj_merged['ALUNOS'] = bairros_rj_merged['ALUNOS'].fillna(0).astype(int)

            print("\nDataFrame final de 'bairros_rj_merged' com contagem de alunos:")
            print(bairros_rj_merged[['nome', 'ALUNOS']].head())

            return bairros_rj_merged
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em preparar_dados_bairros: {e}" + Style.RESET_ALL)
            return bairros_rj

    def consolidar_ilha_do_governador(self, bairros_rj):
        """
        Consolida a Ilha do Governador em uma única região administrativa.

        :param bairros_rj: GeoDataFrame com os dados geográficos dos bairros do RJ.
        :return: GeoDataFrame consolidado.
        """
        try:
            print(Fore.CYAN + "Consolidando Ilha do Governador..." + Style.RESET_ALL)
            ilha = bairros_rj[bairros_rj['regiao_adm'].str.contains('ILHA DO GOVERNADOR', na=False)]
            if not ilha.empty:
                ilha_consolidada = ilha.dissolve(by='regiao_adm')
                ilha_consolidada['nome'] = 'ILHA DO GOVERNADOR'
                bairros_rj = bairros_rj[~bairros_rj['regiao_adm'].str.contains('ILHA DO GOVERNADOR', na=False)]
                bairros_rj = pd.concat([bairros_rj, ilha_consolidada], ignore_index=True)
            else:
                print(Fore.YELLOW + "Aviso: Nenhuma entrada encontrada para 'ILHA DO GOVERNADOR' na região administrativa." + Style.RESET_ALL)
            return bairros_rj
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro inesperado em consolidar_ilha_do_governador: {e}" + Style.RESET_ALL)
            return bairros_rj

    def carregar_bairros_rj(self):
        """
        Carrega os dados geográficos dos bairros do Rio de Janeiro.

        :return: GeoDataFrame com os dados dos bairros do RJ.
        """
        try:
            print(Fore.CYAN + "Carregando dados geográficos dos bairros do RJ..." + Style.RESET_ALL)
            caminho_geojson = os.path.join(pega_caminho_base(), 'dados', 'Limite_de_Bairros.geojson')
            bairros_rj = gpd.read_file(caminho_geojson)
            print(Fore.GREEN + "Dados geográficos carregados com sucesso." + Style.RESET_ALL)
            return bairros_rj
        except Exception as e:
            print(Fore.RED + f"Ocorreu um erro ao carregar bairros_rj: {e}" + Style.RESET_ALL)
            return gpd.GeoDataFrame()

    # -----------------------------------
    # Métodos Auxiliares
    # -----------------------------------

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
