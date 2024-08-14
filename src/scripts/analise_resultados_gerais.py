import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from colorama import Fore
from src.utils.plots import salvar_grafico, criar_pasta_graficos
from src.utils.utils import separar_por_periodo, carregar_dados


def analise_resultados_gerais(df, nome_pasta):
    criar_pasta_graficos(nome_pasta)

    # Separar os dados por período
    periodos = separar_por_periodo(df)
    periodos_dados = {}

    for periodo, df_periodo in periodos.items():
        if periodo == '1_antes_cotas':
            grupo_cotistas = pd.DataFrame()
            grupo_nao_cotistas = df_periodo
        else:
            grupo_cotistas = df_periodo[df_periodo['FORMA_INGRESSO_SIMPLES'] == 'Cotas']
            grupo_nao_cotistas = df_periodo[df_periodo['FORMA_INGRESSO_SIMPLES'] == 'Ampla Concorrencia']

        periodos_dados[periodo] = (grupo_cotistas, grupo_nao_cotistas)

    # Plotar gráficos consolidados
    plotar_media_cra_por_grupo_consolidado(periodos_dados, nome_pasta)
    plotar_taxa_evasao_conclusao_cursando_consolidado(periodos_dados, nome_pasta)

    print(Fore.GREEN + "\nAnálise por Período Concluída!")


def plotar_media_cra_por_grupo_consolidado(periodos_dados, nome_pasta):
    dados_consolidados = []

    for periodo, (grupo_cotistas, grupo_nao_cotistas) in periodos_dados.items():
        media_cotistas = grupo_cotistas['CRA'].mean() if not grupo_cotistas.empty else None
        media_nao_cotistas = grupo_nao_cotistas['CRA'].mean() if not grupo_nao_cotistas.empty else None

        dados_consolidados.append({'Periodo': periodo, 'Grupo': 'Cotistas', 'Média CRA': media_cotistas})
        dados_consolidados.append({'Periodo': periodo, 'Grupo': 'Não Cotistas', 'Média CRA': media_nao_cotistas})

    df_consolidado = pd.DataFrame(dados_consolidados)

    plt.figure(figsize=(14, 8))
    ax = sns.barplot(x='Periodo', y='Média CRA', hue='Grupo', data=df_consolidado, palette='pastel', ci=None)

    # Adicionando os valores exatos das médias em cima das barras
    for p in ax.patches:
        if p.get_height() > 0:  # Verifica se o valor é maior que 0 para evitar anotações erradas
            ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 8), textcoords='offset points')

    plt.title(f'Comparação de Média de CRA por Período e Grupo')
    plt.xlabel('Período')
    plt.ylabel('Média CRA')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    salvar_grafico('comparacao_media_cra_por_grupo_e_periodo', nome_pasta)


def plotar_taxa_evasao_conclusao_cursando_consolidado(periodos_dados, nome_pasta):
    dados_consolidados = []

    def calcular_taxas(grupo):
        total = len(grupo)
        if total == 0:
            return 0, 0, 0
        evasao = len(grupo[grupo['STATUS_EVASAO'] == 'Evasão']) / total * 100
        conclusao = len(grupo[grupo['STATUS_EVASAO'] == 'Concluído']) / total * 100
        cursando = len(grupo[grupo['STATUS_EVASAO'] == 'Cursando']) / total * 100
        return evasao, conclusao, cursando

    for periodo, (grupo_cotistas, grupo_nao_cotistas) in periodos_dados.items():
        taxas_cotistas = calcular_taxas(grupo_cotistas)
        taxas_nao_cotistas = calcular_taxas(grupo_nao_cotistas)

        dados_consolidados.append({'Periodo': periodo, 'Grupo': 'Cotistas', 'Status': 'Evasão', 'Porcentagem': taxas_cotistas[0]})
        dados_consolidados.append({'Periodo': periodo, 'Grupo': 'Cotistas', 'Status': 'Conclusão', 'Porcentagem': taxas_cotistas[1]})
        dados_consolidados.append({'Periodo': periodo, 'Grupo': 'Cotistas', 'Status': 'Cursando', 'Porcentagem': taxas_cotistas[2]})

        dados_consolidados.append({'Periodo': periodo, 'Grupo': 'Não Cotistas', 'Status': 'Evasão', 'Porcentagem': taxas_nao_cotistas[0]})
        dados_consolidados.append({'Periodo': periodo, 'Grupo': 'Não Cotistas', 'Status': 'Conclusão', 'Porcentagem': taxas_nao_cotistas[1]})
        dados_consolidados.append({'Periodo': periodo, 'Grupo': 'Não Cotistas', 'Status': 'Cursando', 'Porcentagem': taxas_nao_cotistas[2]})

    df_consolidado = pd.DataFrame(dados_consolidados)

    plt.figure(figsize=(14, 8))
    ax = sns.barplot(x='Periodo', y='Porcentagem', hue='Status', data=df_consolidado, palette='muted', ci=None)

    # Adicionando os valores exatos das porcentagens em cima das barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points')

    plt.title(f'Taxa de Evasão, Conclusão e Cursando por Período e Grupo')
    plt.xlabel('Período')
    plt.ylabel('Porcentagem (%)')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    salvar_grafico('comparacao_taxa_evasao_conclusao_cursando_por_periodo', nome_pasta)


if __name__ == "__main__":
    df = carregar_dados()
    analise_resultados_gerais(df, 'graficos/resultados_gerais')
