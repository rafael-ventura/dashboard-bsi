import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from colorama import Fore, Style
from src.utils.plots import salvar_grafico, ajustar_estilos_grafico
import matplotlib.patches as mpatches


class AnaliseTipoIngresso:
    def __init__(self, dataframe, pasta_graficos):
        """
        Inicializa a classe para análise de tipo de ingresso.

        :param dataframe: DataFrame formatado com os dados.
        :param pasta_graficos: Caminho da pasta onde os gráficos serão salvos.
        """
        self.df = dataframe.copy()
        self.pasta_graficos = pasta_graficos

        # Unificar categorias específicas
        self.df['FORMA_INGRESSO_SIMPLES'] = self.df['FORMA_INGRESSO_SIMPLES'].replace(
            {'SISU': 'SISU Ampla Concorrência', 'ENEM': 'SISU Ampla Concorrência', 'Vestibular': 'SISU Ampla Concorrência'}
        )

    def executar_analises(self):
        """
        Executa as análises relacionadas ao tipo de ingresso.
        """
        print(Fore.CYAN + "Iniciando análises de tipo de ingresso..." + Style.RESET_ALL)

        # Geração dos gráficos e análises
        self.grafico_distribuicao_tipo_ingresso()
        self.grafico_cra_por_tipo_ingresso()
        self.grafico_status_por_tipo_ingresso()
        self.grafico_detalhamento_tipo_ingresso_sem_eixo_x()

        print(Fore.GREEN + "Análises de tipo de ingresso concluídas!" + Style.RESET_ALL)

    def grafico_distribuicao_tipo_ingresso(self):
        """
        Plota a distribuição de alunos por tipo de ingresso.
        """
        try:
            print(Fore.YELLOW + "Plotando gráfico de distribuição de tipo de ingresso..." + Style.RESET_ALL)
            contagem = self.df['FORMA_INGRESSO_SIMPLES'].value_counts().reset_index()
            contagem.columns = ['Tipo de Ingresso', 'Quantidade']
            contagem['Percentual'] = (contagem['Quantidade'] / contagem['Quantidade'].sum()) * 100

            plt.figure(figsize=(10, 6))
            ax = sns.barplot(
                x='Tipo de Ingresso',
                y='Quantidade',
                data=contagem,
                palette='pastel'
            )
            for i, row in contagem.iterrows():
                ax.text(i, row['Quantidade'], f"{row['Quantidade']} ({row['Percentual']:.1f}%)", ha='center', va='bottom')

            ajustar_estilos_grafico(
                ax,
                title='Distribuição de Alunos por Tipo de Ingresso',
                xlabel='Tipo de Ingresso',
                ylabel='Quantidade de Alunos'
            )
            salvar_grafico('distribuicao_tipo_ingresso', self.pasta_graficos)
            plt.close()
        except Exception as e:
            print(Fore.RED + f"Erro ao gerar gráfico de distribuição de tipo de ingresso: {e}" + Style.RESET_ALL)

    def grafico_cra_por_tipo_ingresso(self):
        """
        Plota a distribuição do CRA médio por tipo de ingresso.
        """
        try:
            print(Fore.YELLOW + "Plotando gráfico de CRA por tipo de ingresso..." + Style.RESET_ALL)

            # Calcula o CRA médio por tipo de ingresso
            cra_por_tipo = self.df.groupby('FORMA_INGRESSO_SIMPLES')['CRA'].mean().reset_index()
            cra_por_tipo = cra_por_tipo.sort_values(by='CRA', ascending=False)  # Ordena pela média do CRA

            # Configura o tamanho do gráfico
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(
                x='FORMA_INGRESSO_SIMPLES',
                y='CRA',
                data=cra_por_tipo,
                palette='coolwarm'
            )

            # Adiciona os valores no topo das barras
            for p in ax.patches:
                height = p.get_height()
                if height > 0:  # Evita texto para barras vazias
                    ax.text(
                        p.get_x() + p.get_width() / 2.,  # Posição X
                        height,  # Altura da barra
                        f"{height:.4f}",  # Valor formatado com 4 casas decimais
                        ha='center',  # Alinhamento horizontal
                        va='bottom',  # Posiciona o texto acima da barra
                        fontsize=10  # Tamanho da fonte
                    )

            # Ajusta os estilos do gráfico
            ajustar_estilos_grafico(
                ax,
                title='CRA Médio por Tipo de Ingresso',
                xlabel='Tipo de Ingresso',
                ylabel='CRA Médio'
            )

            salvar_grafico('cra_por_tipo_ingresso', self.pasta_graficos)
            plt.close()

        except Exception as e:
            print(Fore.RED + f"Erro ao gerar gráfico de CRA por tipo de ingresso: {e}" + Style.RESET_ALL)

    def grafico_detalhamento_tipo_ingresso_sem_eixo_x(self):
        """
        Plota um gráfico de barras onde os rótulos são exibidos apenas na legenda.
        Inclui a união de categorias específicas e ajusta a largura do gráfico.
        """
        try:
            print(Fore.YELLOW + "Plotando detalhamento de tipo de ingresso com rótulos apenas na legenda..." + Style.RESET_ALL)

            # Unificar categorias específicas
            self.df['FORMA_INGRESSO'] = self.df['FORMA_INGRESSO'].replace(
                {'SISU': 'SISU Ampla Concorrencia', 'ENEM': 'SISU Ampla Concorrencia', 'Vestibular': 'SISU Ampla Concorrencia',
                 'VE - Vestibular': 'SISU Ampla Concorrencia', 'EN - ENEM': 'SISU Ampla Concorrencia'}
            )

            # Calcular proporções diretamente da coluna original
            detalhamento = self.df['FORMA_INGRESSO'].value_counts().reset_index()
            detalhamento.columns = ['Tipo Simplificado', 'Quantidade']
            detalhamento['Percentual'] = (detalhamento['Quantidade'] / detalhamento['Quantidade'].sum()) * 100

            # Log de valores para depuração
            print(Fore.CYAN + "Valores encontrados para a legenda:" + Style.RESET_ALL)
            print(detalhamento[['Tipo Simplificado', 'Quantidade', 'Percentual']].to_string(index=False))

            # Criar paleta de cores com tons de 'viridis'
            cores = sns.color_palette('viridis', len(detalhamento))

            # Configurar o gráfico com largura ajustada
            plt.figure(figsize=(14, 6))  # Aumentando a largura para 14
            barras = plt.bar(
                range(len(detalhamento)),  # Índices genéricos para o eixo X
                detalhamento['Quantidade'],
                color=cores
            )

            # Adicionar valores no topo das barras
            for i, bar in enumerate(barras):
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f"{detalhamento['Quantidade'][i]} ({detalhamento['Percentual'][i]:.1f}%)",
                    ha='center',
                    va='bottom',
                    fontsize=10
                )

            # Criar legenda manualmente
            legend_patches = [
                mpatches.Patch(color=cores[i], label=detalhamento['Tipo Simplificado'][i])
                for i in range(len(detalhamento))
            ]
            plt.legend(handles=legend_patches, title='Tipos de Ingresso', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

            # Ajustar estilos do gráfico
            plt.title('Detalhamento de Tipos de Ingresso', fontsize=14)
            plt.ylabel('Quantidade de Alunos', fontsize=12)
            plt.xticks([], [])  # Remover rótulos do eixo X
            plt.tight_layout()

            # Salvar gráfico
            salvar_grafico('detalhamento_tipo_ingresso_sem_eixo_x', self.pasta_graficos)
            plt.close()
            print(Fore.GREEN + "Gráfico gerado com sucesso!" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"Erro ao gerar gráfico: {e}" + Style.RESET_ALL)

    def grafico_status_por_tipo_ingresso(self):
        """
        Plota o status dos alunos (Cursando, Evasão, Concluído) por tipo de ingresso,
        mostrando a porcentagem relativa ao grupo (máximo 100% por grupo) e ajusta a largura.
        """
        try:
            print(Fore.YELLOW + "Plotando gráfico de status por tipo de ingresso com porcentagens e legenda corrigidas..." + Style.RESET_ALL)

            # Unificar categorias específicas
            self.df['FORMA_INGRESSO_SIMPLES'] = self.df['FORMA_INGRESSO_SIMPLES'].replace(
                {'SISU': 'SISU Ampla Concorrência', 'ENEM': 'SISU Ampla Concorrência', 'Vestibular': 'SISU Ampla Concorrência',
                 'VE - Vestibular': 'SISU Ampla Concorrência', 'EN - ENEM': 'SISU Ampla Concorrência'}
            )

            # Agrupar e calcular a soma por categoria e status
            status_por_tipo = self.df.groupby(['FORMA_INGRESSO_SIMPLES', 'STATUS_EVASAO']).size().reset_index(name='Quantidade')
            total_por_tipo = self.df.groupby('FORMA_INGRESSO_SIMPLES').size().reset_index(name='Total')
            status_por_tipo = status_por_tipo.merge(total_por_tipo, on='FORMA_INGRESSO_SIMPLES')
            status_por_tipo['Percentual'] = (status_por_tipo['Quantidade'] / status_por_tipo['Total']) * 100

            # Plotar gráfico com largura ajustada
            plt.figure(figsize=(14, 8))  # Aumentando a largura para 14
            ax = sns.barplot(
                x='FORMA_INGRESSO_SIMPLES',
                y='Percentual',
                hue='STATUS_EVASAO',
                data=status_por_tipo,
                palette='YlOrRd'
            )

            # Adicionar porcentagens no topo das barras
            for p in ax.patches:
                height = p.get_height()
                if height > 0:
                    ax.text(
                        p.get_x() + p.get_width() / 2.,
                        height,
                        f'{height:.1f}%',
                        ha='center',
                        va='bottom',
                        fontsize=10
                    )

            # Criar legenda manualmente com cores correspondentes ao hue
            handles, labels = ax.get_legend_handles_labels()
            legend_patches = [
                mpatches.Patch(color=h.get_facecolor(), label=l) for h, l in zip(handles, labels)
            ]
            plt.legend(handles=legend_patches, title='Status do Curso', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

            # Ajustar estilos e salvar gráfico
            ajustar_estilos_grafico(
                ax,
                title='Status dos Alunos por Tipo de Ingresso',
                xlabel='Tipo de Ingresso',
                ylabel='Percentual de Alunos (%)'
            )
            salvar_grafico('status_por_tipo_ingresso_corrigido', self.pasta_graficos)
            plt.close()

        except Exception as e:
            print(Fore.RED + f"Erro ao gerar gráfico de status por tipo de ingresso: {e}" + Style.RESET_ALL)
