import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from colorama import Fore, Style
from src.utils.plots import salvar_grafico, ajustar_estilos_grafico, adicionar_valores_barras


class AnaliseTipoIngresso:
    def __init__(self, dataframe, pasta_graficos):
        """
        Inicializa a classe para análise de tipo de ingresso e executa os gráficos automaticamente.

        :param dataframe: DataFrame formatado com os dados.
        :param pasta_graficos: Caminho da pasta onde os gráficos serão salvos.
        """
        print(Fore.CYAN + "Iniciando análises de tipo de ingresso..." + Style.RESET_ALL)

        self.df = dataframe.copy()
        self.pasta_graficos = pasta_graficos
        self.categorizar_periodo_ingresso()  # Criar coluna categorizada dos períodos
        self.gerar_graficos()  # Gera os gráficos automaticamente

        print(Fore.GREEN + "Análises de tipo de ingresso concluídas!" + Style.RESET_ALL)

    def categorizar_periodo_ingresso(self):
        """
        Categoriza os períodos de ingresso em "Pré-Cota", "Pós-Cota", "Pandemia" e "Pós-Pandemia" na ordem correta.
        """

        def definir_categoria(periodo):
            if periodo <= 2013:
                return "Pré-Cota"
            elif 2014 <= periodo <= 2020:
                return "Pós-Cota"
            elif 2020.2 <= periodo <= 2022.2:
                return "Pandemia"
            else:
                return "Pós-Pandemia"

        self.df["PERIODO_CATEGORIZADO"] = self.df["ANO_PERIODO_INGRESSO"].apply(definir_categoria)

        # Definir a ordem correta dos períodos
        categorias_ordenadas = ["Pré-Cota", "Pós-Cota", "Pandemia", "Pós-Pandemia"]
        self.df["PERIODO_CATEGORIZADO"] = pd.Categorical(
            self.df["PERIODO_CATEGORIZADO"], categories=categorias_ordenadas, ordered=True
        )

    def gerar_graficos(self):
        """
        Executa os métodos de geração de gráficos.
        """
        self.grafico_cra_por_tipo_ingresso_e_periodo()
        self.grafico_distribuicao_geral_ingresso()

    def grafico_cra_por_tipo_ingresso_e_periodo(self):
        """
        Plota um gráfico de barras com o CRA médio por tipo de ingresso e período.
        """
        try:
            print(Fore.YELLOW + "Plotando gráfico de CRA por tipo de ingresso e período..." + Style.RESET_ALL)

            # Calcular a média do CRA por período e tipo de ingresso, mantendo duas casas decimais
            df_cra = self.df.groupby(["PERIODO_CATEGORIZADO", "FORMA_INGRESSO_SIMPLES"])["CRA"].mean().reset_index()
            df_cra["CRA"] = df_cra["CRA"].round(2)  # Arredondar para duas casas decimais

            # Criar o gráfico de barras
            plt.figure(figsize=(12, 6))
            ax = sns.barplot(
                x="PERIODO_CATEGORIZADO",
                y="CRA",
                hue="FORMA_INGRESSO_SIMPLES",
                data=df_cra,
                palette="coolwarm"
            )

            # Adicionar os valores no topo das barras, formatando corretamente
            for p in ax.patches:
                height = p.get_height()
                if height > 0:  # Evita adicionar valores em barras vazias
                    ax.text(
                        p.get_x() + p.get_width() / 2.,
                        height,
                        f"{height:.2f}",  # Formata com duas casas decimais
                        ha='center',
                        va='bottom',
                        fontsize=10
                    )

            # Ajustar estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title="CRA Médio por Tipo de Ingresso e Período",
                xlabel="Período de Ingresso",
                ylabel="CRA Médio"
            )

            salvar_grafico("cra_por_tipo_ingresso_e_periodo", self.pasta_graficos)
            plt.close()
            print(Fore.GREEN + "Gráfico gerado com sucesso!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Erro ao gerar gráfico de CRA por tipo de ingresso e período: {e}" + Style.RESET_ALL)

    def grafico_distribuicao_geral_ingresso(self):
        """
        Plota um gráfico de barras mostrando a distribuição geral das formas de ingresso,
        agrupando os ingressos antes de 2014 em "Ampla Concorrência - Antes das Cotas".
        """
        try:
            print(Fore.YELLOW + "Plotando gráfico de distribuição geral dos tipos de ingresso..." + Style.RESET_ALL)

            # Criar a nova categoria de ingresso agrupando 2008-2013 como "Ampla Concorrência - Antes das Cotas"
            self.df["CATEGORIA_INGRESSO"] = self.df.apply(
                lambda row: "Ampla Concorrência - Antes das Cotas" if row["ANO_PERIODO_INGRESSO"] <= 2013 else row["FORMA_INGRESSO"],
                axis=1
            )

            # Contagem de alunos por tipo de ingresso
            df_ingresso = self.df["CATEGORIA_INGRESSO"].value_counts().reset_index()
            df_ingresso.columns = ["Tipo de Ingresso", "Quantidade"]

            # Calcular percentual do total
            df_ingresso["Percentual"] = (df_ingresso["Quantidade"] / df_ingresso["Quantidade"].sum()) * 100

            # Criar gráfico de barras
            plt.figure(figsize=(16, 8))  # Aumentar altura do gráfico
            ax = sns.barplot(
                x="Quantidade",
                y="Tipo de Ingresso",
                data=df_ingresso,
                palette="Set2"
            )

            # Adicionar os valores ao lado direito das barras (Quantidade + %)
            for p in ax.patches:
                width = p.get_width()
                if width > 0:
                    ax.text(
                        width + 10,  # Posição do texto um pouco mais distante da barra
                        p.get_y() + p.get_height() / 2,
                        f"{int(width)} ({width / df_ingresso['Quantidade'].sum() * 100:.1f}%)",
                        ha='left',
                        va='center',
                        fontsize=10,
                        fontweight='bold',
                        color='black'
                    )

            # Ajustar estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title="Distribuição Geral das Formas de Ingresso",
                xlabel="Quantidade de Alunos",
                ylabel="Tipo de Ingresso"
            )

            # Ajustar os limites do eixo X para dar mais espaço à direita
            ax.set_xlim(0, df_ingresso["Quantidade"].max() * 1.2)  # Agora tem 20% de espaço extra

            # Remover a legenda
            ax.legend().remove()

            # Ajustar espaçamento para evitar cortes
            plt.tight_layout(pad=2)

            salvar_grafico("distribuicao_geral_ingresso", self.pasta_graficos)
            plt.close()
            print(Fore.GREEN + "Gráfico gerado com sucesso!" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"Erro ao gerar gráfico de distribuição geral dos tipos de ingresso: {e}" + Style.RESET_ALL)
