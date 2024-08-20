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

    # Plotar gráficos separados para cada período
    for periodo, (grupo_cotistas, grupo_nao_cotistas) in periodos_dados.items():
        plotar_grafico_por_periodo(periodo, grupo_cotistas, grupo_nao_cotistas, nome_pasta, df)

    print(Fore.GREEN + "\nAnálise por Período Concluída!")


def plotar_grafico_por_periodo(periodo, grupo_cotistas, grupo_nao_cotistas, nome_pasta, df):
    dados_consolidados = []

    if 'ZONA' in df.columns:  # Verifica se a coluna 'ZONA' existe
        for zona in df['ZONA'].unique():
            total_cotistas_zona = grupo_cotistas[grupo_cotistas['ZONA'] == zona].shape[0] if not grupo_cotistas.empty else 0
            total_nao_cotistas_zona = grupo_nao_cotistas[grupo_nao_cotistas['ZONA'] == zona].shape[0] if not grupo_nao_cotistas.empty else 0

            total_cotistas_zona_perc = (total_cotistas_zona / len(grupo_cotistas)) * 100 if len(grupo_cotistas) > 0 else 0
            total_nao_cotistas_zona_perc = (total_nao_cotistas_zona / len(grupo_nao_cotistas)) * 100 if len(grupo_nao_cotistas) > 0 else 0

            dados_consolidados.append({'Zona': zona, 'Grupo': 'Cotistas', 'Porcentagem': total_cotistas_zona_perc})
            dados_consolidados.append({'Zona': zona, 'Grupo': 'Não Cotistas', 'Porcentagem': total_nao_cotistas_zona_perc})

        df_consolidado_zona = pd.DataFrame(dados_consolidados)

        # Criar um gráfico grande com labels e ticks maiores
        plt.figure(figsize=(16, 10))
        ax = sns.barplot(x='Zona', y='Porcentagem', hue='Grupo', data=df_consolidado_zona, palette='pastel', ci=None)

        # Adicionando os valores exatos em cima das barras
        for p in ax.patches:
            if p.get_height() > 0:  # Verifica se o valor é maior que 0 para evitar anotações erradas
                ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', xytext=(0, 8), textcoords='offset points')

        plt.title(f'Número de Alunos por Zona Geográfica - {periodo}', fontsize=18)
        plt.xlabel('Zona Geográfica', fontsize=14)
        plt.ylabel('Porcentagem (%)', fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
        plt.tight_layout()

        # Salvar o gráfico para cada período separadamente
        salvar_grafico(f'distribuicao_alunos_por_zona_{periodo}', nome_pasta)
    else:
        print(Fore.RED + "A coluna 'ZONA' não existe no DataFrame!")


if __name__ == "__main__":
    df = carregar_dados()
    analise_resultados_gerais(df, 'graficos/resultados_gerais')
