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
        self.gerar_graficos()

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
        self.grafico_status_alunos_por_periodo()
        self.grafico_tempo_medio_curso_por_tipo_ingresso()
        self.grafico_proporcao_concluintes_evasao_por_tempo_curso()
        self.grafico_cra_por_tempo_de_formacao()
        self.grafico_cra_por_idade_ingresso()
        self.grafico_cra_por_sexo()
        self.grafico_faixa_etaria_evasao()

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

    def grafico_status_alunos_por_periodo(self):
        """
        Plota um gráfico de barras empilhadas mostrando o status dos alunos por período de ingresso,
        incluindo o número absoluto e a porcentagem acima das barras.
        """
        try:
            print(Fore.YELLOW + "Plotando gráfico de status dos alunos por período de ingresso..." + Style.RESET_ALL)

            # Contar alunos por período e status (Cursando, Concluído, Evasão)
            df_status = self.df.groupby(["PERIODO_CATEGORIZADO", "STATUS_EVASAO"]).size().reset_index(name="Quantidade")

            # Calcular percentual dentro de cada período
            df_total_por_periodo = df_status.groupby("PERIODO_CATEGORIZADO")["Quantidade"].sum().reset_index()
            df_total_por_periodo = df_total_por_periodo.rename(columns={"Quantidade": "Total"})
            df_status = df_status.merge(df_total_por_periodo, on="PERIODO_CATEGORIZADO", how="left")
            df_status["Percentual"] = (df_status["Quantidade"] / df_status["Total"]) * 100

            # Criar gráfico de barras empilhadas
            plt.figure(figsize=(14, 7))
            ax = sns.barplot(
                x="PERIODO_CATEGORIZADO",
                y="Quantidade",
                hue="STATUS_EVASAO",
                data=df_status,
                palette="viridis"
            )

            # Adicionar os valores ACIMA das barras com o formato absoluto + percentual
            for p in ax.patches:
                altura = p.get_height()
                if altura > 0:  # Evita adicionar valores em barras vazias
                    # Encontrar o valor percentual correspondente à barra
                    periodo = ax.get_xticklabels()[int(p.get_x() + p.get_width() / 2)].get_text()
                    percentual = df_status[
                        (df_status["PERIODO_CATEGORIZADO"] == periodo) & (df_status["Quantidade"] == altura)
                        ]["Percentual"].values
                    percentual = percentual[0] if len(percentual) > 0 else 0

                    # Exibir o valor absoluto e a porcentagem ACIMA da barra
                    ax.text(
                        p.get_x() + p.get_width() / 2,
                        altura + (ax.get_ylim()[1] * 0.02),  # Posiciona acima da barra
                        f"{int(altura)} ({percentual:.1f}%)",
                        ha='center',
                        va='bottom',
                        fontsize=7,
                        fontweight='bold',
                        color='black'
                    )

            # Ajustar estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title="Status dos Alunos por Período de Ingresso",
                xlabel="Período de Ingresso",
                ylabel="Quantidade de Alunos"
            )

            # Posicionar a legenda no canto superior direito
            ax.legend(title="Status do Aluno", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

            # Ajustar os limites do eixo Y para dar mais espaço para os valores no topo
            ax.set_ylim(0, df_status["Quantidade"].max() * 1.15)

            # Ajustar espaçamento para evitar cortes
            plt.tight_layout(pad=3)

            salvar_grafico("status_alunos_por_periodo", self.pasta_graficos)
            plt.close()
            print(Fore.GREEN + "Gráfico gerado com sucesso!" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"Erro ao gerar gráfico de status dos alunos por período de ingresso: {e}" + Style.RESET_ALL)

    def grafico_tempo_medio_curso_por_tipo_ingresso(self):
        """
        Plota um gráfico de barras mostrando o tempo médio de curso por tipo de ingresso,
        excluindo os períodos de Pandemia e Pós-Pandemia, já que os alunos desses períodos ainda não concluíram.
        """
        try:
            print(Fore.YELLOW + "Plotando gráfico de tempo médio de curso por tipo de ingresso..." + Style.RESET_ALL)

            # Filtrar apenas os períodos que fazem sentido na análise (Pré-Cota e Pós-Cota)
            df_filtrado = self.df[self.df["PERIODO_CATEGORIZADO"].isin(["Pré-Cota", "Pós-Cota"])]

            # Calcular tempo médio de curso por período e tipo de ingresso
            df_tempo = df_filtrado.groupby(["PERIODO_CATEGORIZADO", "FORMA_INGRESSO_SIMPLES"])["TEMPO_CURSO"].mean().reset_index()
            df_tempo["TEMPO_CURSO"] = df_tempo["TEMPO_CURSO"].round(2)  # Arredondar para 2 casas decimais

            # Garantir que apenas os períodos desejados aparecem no gráfico e manter a ordem correta
            categorias_ordenadas = ["Pré-Cota", "Pós-Cota"]
            df_tempo["PERIODO_CATEGORIZADO"] = pd.Categorical(df_tempo["PERIODO_CATEGORIZADO"], categories=categorias_ordenadas, ordered=True)

            # Criar gráfico de barras
            plt.figure(figsize=(12, 6))
            ax = sns.barplot(
                x="PERIODO_CATEGORIZADO",
                y="TEMPO_CURSO",
                hue="FORMA_INGRESSO_SIMPLES",
                data=df_tempo,
                palette="muted"
            )

            # Função para converter anos decimais em formato "X anos e Y meses"
            def formatar_tempo(anos):
                anos_inteiros = int(anos)
                meses = int((anos - anos_inteiros) * 12)  # Converter a parte decimal para meses
                if meses == 0:
                    return f"{anos_inteiros} anos"
                return f"{anos_inteiros} anos e {meses} meses"

            # Adicionar os valores no topo das barras
            for p in ax.patches:
                height = p.get_height()
                if height > 0:
                    ax.text(
                        p.get_x() + p.get_width() / 2,
                        height,  # Posição ligeiramente acima da barra
                        formatar_tempo(height),  # Formatar para "X anos e Y meses"
                        ha='center',
                        va='bottom',
                        fontsize=10,
                        fontweight='bold'
                    )

            # Ajustar estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title="Tempo Médio de Curso por Tipo de Ingresso (Excluindo Pandemia)",
                xlabel="Período de Ingresso",
                ylabel="Tempo Médio de Curso"
            )

            # Ajustar os ticks do eixo X para mostrar apenas os períodos desejados
            ax.set_xticklabels(["Pré-Cota", "Pós-Cota"])

            # Salvar o gráfico
            salvar_grafico("tempo_medio_curso_por_tipo_ingresso", self.pasta_graficos)
            plt.close()
            print(Fore.GREEN + "Gráfico gerado com sucesso!" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"Erro ao gerar gráfico de tempo médio de curso: {e}" + Style.RESET_ALL)

    def grafico_proporcao_concluintes_evasao_por_tempo_curso(self):
        """
        Plota um histograma empilhado mostrando a distribuição do tempo de curso
        de alunos que concluíram ou evadiram, separando por tipo de ingresso.
        """
        try:
            print(Fore.YELLOW + "Plotando gráfico de proporção de concluintes e evasão por tempo de curso..." + Style.RESET_ALL)

            # Filtrar apenas os períodos relevantes e remover alunos ainda cursando
            df_filtrado = self.df[
                (self.df["PERIODO_CATEGORIZADO"].isin(["Pré-Cota", "Pós-Cota"])) &
                (self.df["STATUS_EVASAO"] != "Cursando")
                ]

            # Criar gráfico de histograma empilhado
            plt.figure(figsize=(12, 6))
            ax = sns.histplot(
                data=df_filtrado,
                x="TEMPO_CURSO",
                hue="STATUS_EVASAO",
                multiple="stack",
                palette="viridis",
                bins=20
            )

            # Ajustar estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title="Proporção de Concluintes e Evasão por Tempo de Curso",
                xlabel="Tempo de Curso (anos)",
                ylabel="Número de Alunos"
            )

            # Salvar gráfico
            salvar_grafico("proporcao_concluintes_evasao_por_tempo_curso", self.pasta_graficos)
            plt.close()
            print(Fore.GREEN + "Gráfico gerado com sucesso!" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"Erro ao gerar gráfico de proporção de concluintes e evasão: {e}" + Style.RESET_ALL)

    def grafico_cra_por_tempo_de_formacao(self):
        """
        Plota um gráfico mostrando a relação entre faixas de tempo de formação e a média do CRA.
        """
        try:
            print(Fore.YELLOW + "Plotando gráfico de CRA médio por faixas de tempo de formação..." + Style.RESET_ALL)

            # Filtrar apenas alunos que concluíram o curso
            df_concluintes = self.df[self.df["STATUS_EVASAO"] == "Concluído"].copy()

            # Criar a faixa de tempo de formação
            def categorizar_tempo_curso(tempo):
                if tempo < 4:
                    return "<4 anos"
                elif 4 <= tempo < 4.5:
                    return "4 - 4.5 anos"
                elif 4.5 <= tempo < 6:
                    return "4.5 - 6 anos"
                elif 6 <= tempo < 8:
                    return "6 - 8 anos"
                else:
                    return ">8 anos"

            df_concluintes["FAIXA_TEMPO_CURSO"] = df_concluintes["TEMPO_CURSO"].apply(categorizar_tempo_curso)

            # Agrupar por faixa de tempo e calcular a média do CRA
            df_faixas = df_concluintes.groupby("FAIXA_TEMPO_CURSO")["CRA"].mean().reset_index()

            # Ordenar as faixas na ordem correta
            categorias_ordenadas = ["<4 anos", "4 - 4.5 anos", "4.5 - 6 anos", "6 - 8 anos", ">8 anos"]
            df_faixas["FAIXA_TEMPO_CURSO"] = pd.Categorical(df_faixas["FAIXA_TEMPO_CURSO"], categories=categorias_ordenadas, ordered=True)

            # Criar o gráfico
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(
                x="FAIXA_TEMPO_CURSO",
                y="CRA",
                data=df_faixas,
                palette="coolwarm"
            )

            # Adicionar os valores no topo das barras
            for p in ax.patches:
                height = p.get_height()
                if height > 0:
                    ax.text(
                        p.get_x() + p.get_width() / 2,
                        height,
                        f"{height:.2f}",
                        ha="center",
                        va="bottom",
                        fontsize=10,
                        fontweight="bold"
                    )

            # Ajustar estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title="Média de CRA por Faixa de Tempo de Formação",
                xlabel="Faixa de Tempo de Formação",
                ylabel="CRA Médio"
            )

            # Salvar o gráfico
            salvar_grafico("cra_por_faixa_tempo_de_formacao", self.pasta_graficos)
            plt.close()
            print(Fore.GREEN + "Gráfico gerado com sucesso!" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"Erro ao gerar gráfico de CRA por faixa de tempo de formação: {e}" + Style.RESET_ALL)

    def grafico_cra_por_idade_ingresso(self):
        """
        Plota um gráfico de barras mostrando a média do CRA por faixa etária no ingresso.
        """
        try:
            print(Fore.YELLOW + "Plotando gráfico de CRA por idade no ingresso..." + Style.RESET_ALL)

            # Criar novas faixas etárias
            def categorizar_idade(idade):
                if idade < 18:
                    return "Menos de 18 anos"
                elif 18 <= idade < 20:
                    return "18-19 anos"
                elif 20 <= idade < 23:
                    return "20-22 anos"
                elif 23 <= idade < 26:
                    return "23-25 anos"
                elif 25 <= idade < 30:
                    return "25-30 anos"
                else:
                    return "Mais de 30 anos"

            self.df["FAIXA_IDADE_INGRESSO"] = self.df["IDADE_INGRESSO"].apply(categorizar_idade)

            # Ordenar categorias para exibição correta no gráfico
            categorias_ordenadas = [
                "Menos de 18 anos", "18-19 anos", "20-22 anos",
                "23-25 anos", "25-30 anos", "Mais de 30 anos"
            ]
            self.df["FAIXA_IDADE_INGRESSO"] = pd.Categorical(
                self.df["FAIXA_IDADE_INGRESSO"], categories=categorias_ordenadas, ordered=True
            )

            # Calcular média do CRA por faixa etária
            df_idade_cra = self.df.groupby("FAIXA_IDADE_INGRESSO")["CRA"].mean().reset_index()
            df_idade_cra["CRA"] = df_idade_cra["CRA"].round(2)  # Arredondar para 2 casas decimais

            # Criar gráfico de barras
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(
                x="FAIXA_IDADE_INGRESSO",
                y="CRA",
                data=df_idade_cra,
                palette="coolwarm"
            )

            # Adicionar os valores no topo das barras
            for p in ax.patches:
                height = p.get_height()
                ax.text(
                    p.get_x() + p.get_width() / 2,
                    height + 0.05,  # Pequena margem para não encostar na barra
                    f"{height:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontweight="bold"
                )

            # Ajustar estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title="Média do CRA por Faixa Etária no Ingresso",
                xlabel="Faixa Etária de Ingresso",
                ylabel="CRA Médio"
            )

            # Salvar o gráfico
            salvar_grafico("cra_por_idade_ingresso", self.pasta_graficos)
            plt.close()
            print(Fore.GREEN + "Gráfico gerado com sucesso!" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"Erro ao gerar gráfico de CRA por idade no ingresso: {e}" + Style.RESET_ALL)

    def grafico_cra_por_sexo(self):
        """
        Plota um boxplot mostrando a relação entre o sexo e o CRA.
        """
        try:
            print(Fore.YELLOW + "Plotando gráfico de CRA por sexo..." + Style.RESET_ALL)

            # Criar o boxplot do CRA por sexo
            plt.figure(figsize=(8, 6))
            ax = sns.boxplot(
                x="SEXO",
                y="CRA",
                data=self.df,
                palette="pastel",
                showfliers=True  # Mantém os outliers visíveis
            )

            # Ajustar estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title="Distribuição do CRA por Sexo",
                xlabel="Sexo",
                ylabel="CRA"
            )

            # Salvar o gráfico
            salvar_grafico("cra_por_sexo", self.pasta_graficos)
            plt.close()
            print(Fore.GREEN + "Gráfico gerado com sucesso!" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"Erro ao gerar gráfico de CRA por sexo: {e}" + Style.RESET_ALL)

    def grafico_faixa_etaria_evasao(self):
        """
        Plota um gráfico de barras mostrando a distribuição da faixa etária dos alunos no momento da evasão,
        incluindo valores absolutos e percentuais ao lado das barras.
        """
        try:
            print(Fore.YELLOW + "Plotando gráfico de faixa etária na evasão..." + Style.RESET_ALL)

            # Filtrar apenas alunos que evadiram e não pertencem aos períodos Pandemia/Pós-Pandemia
            df_evasao = self.df[
                (self.df["STATUS_EVASAO"] != "Cursando") &
                (self.df["PERIODO_CATEGORIZADO"].isin(["Pré-Cota", "Pós-Cota"]))
                ].copy()

            # Criar a faixa etária na evasão
            def categorizar_idade_evasao(idade):
                if idade < 20:
                    return "Menos de 20 anos"
                elif 20 <= idade < 25:
                    return "20-24 anos"
                elif 25 <= idade < 30:
                    return "25-29 anos"
                elif 30 <= idade < 35:
                    return "30-34 anos"
                else:
                    return "35+ anos"

            df_evasao["FAIXA_ETARIA_EVASAO"] = df_evasao["IDADE_EVASAO"].apply(categorizar_idade_evasao)

            # Contar quantidade de alunos por faixa etária
            df_contagem = df_evasao["FAIXA_ETARIA_EVASAO"].value_counts().reset_index()
            df_contagem.columns = ["Faixa Etária na Evasão", "Quantidade"]

            # Calcular percentual do total
            df_contagem["Percentual"] = (df_contagem["Quantidade"] / df_contagem["Quantidade"].sum()) * 100

            # Ordenar categorias
            categorias_ordenadas = ["Menos de 20 anos", "20-24 anos", "25-29 anos", "30-34 anos", "35+ anos"]
            df_contagem["Faixa Etária na Evasão"] = pd.Categorical(
                df_contagem["Faixa Etária na Evasão"], categories=categorias_ordenadas, ordered=True
            )
            df_contagem = df_contagem.sort_values("Faixa Etária na Evasão")

            # Criar gráfico de barras
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(
                x="Quantidade",
                y="Faixa Etária na Evasão",
                data=df_contagem,
                palette="viridis"
            )

            # Adicionar valores ao lado das barras (Quantidade + %)
            for p in ax.patches:
                width = p.get_width()
                faixa = p.get_y() + p.get_height() / 2
                percentual = df_contagem[df_contagem["Quantidade"] == width]["Percentual"].values[0]

                ax.text(
                    width + 5,  # Posição um pouco à direita da barra
                    faixa,
                    f"{int(width)} ({percentual:.1f}%)",
                    ha="left",
                    va="center",
                    fontsize=10,
                    fontweight="bold",
                    color="black"
                )

            # Ajustar estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title="Distribuição da Faixa Etária no Momento da Evasão",
                xlabel="Número de Alunos",
                ylabel="Faixa Etária na Evasão"
            )

            # Ajustar os limites do eixo X para dar mais espaço ao texto
            ax.set_xlim(0, df_contagem["Quantidade"].max() * 1.2)

            # Ajustar espaçamento para evitar cortes
            plt.tight_layout(pad=2)

            # Salvar o gráfico
            salvar_grafico("faixa_etaria_evasao", self.pasta_graficos)
            plt.close()
            print(Fore.GREEN + "Gráfico gerado com sucesso!" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"Erro ao gerar gráfico de faixa etária na evasão: {e}" + Style.RESET_ALL)
