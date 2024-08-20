import pandas as pd
import numpy as np
from geopy import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
import os

from src.utils.utils import carregar_dados, salvar_dados


def inicializar_geolocator():
    """
    Inicializa o objeto geolocator.
    :return: Objeto geolocator
    """
    return Nominatim(user_agent="geolocalizacao_urca")


def carregar_bairros_falha(filepath='dados/processado/bairros_falha.csv'):
    """
    Carrega a lista de bairros que falharam em calcular a distância anteriormente.
    :param filepath: Caminho do arquivo CSV de bairros falhos.
    :return: Set com os bairros que falharam anteriormente.
    """
    if os.path.exists(filepath):
        return set(pd.read_csv(filepath)['BAIRRO'].values)
    return set()


def salvar_bairros_falha(bairros_falha, filepath='dados/processado/bairros_falha.csv'):
    """
    Salva a lista de bairros que falharam em calcular a distância.
    :param bairros_falha: Conjunto de bairros que falharam.
    :param filepath: Caminho onde salvar o arquivo.
    """
    # Verifica e cria o diretório, se necessário
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Salva o arquivo CSV
    pd.DataFrame({'BAIRRO': list(bairros_falha)}).to_csv(filepath, index=False)


def calcular_distancia_ate_urca(bairro, cidade, estado, geolocator):
    """
    Calcula a distância entre um bairro e a Urca, no Rio de Janeiro.
    Retorna a distância em quilômetros.
    :param bairro: Nome do bairro
    :param cidade: Nome da cidade
    :param estado: Nome do estado
    :param geolocator: Objeto geolocator
    :return: float
    """
    try:
        time.sleep(1)  # Evita sobrecarga na API
        endereco_bairro = f"{bairro}, {cidade}, {estado}"
        local_urca = geolocator.geocode("Urca, Rio de Janeiro, Rio de Janeiro")
        local_bairro = geolocator.geocode(endereco_bairro)
        if local_urca and local_bairro:
            print(f"Calculando distância entre Urca e {bairro}...")
            return round(geodesic((local_urca.latitude, local_urca.longitude),
                                  (local_bairro.latitude, local_bairro.longitude)).km, 2)
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Erro ao geolocalizar {bairro}: {e}")
    return np.NaN


def adicionar_distancia_ate_urca(dataframe, dataframe_distancias, geolocator, bairros_falha_existentes):
    """
    Adiciona a distância entre um bairro e a Urca ao DataFrame.
    Filtra cidades e bairros fora do estado do Rio de Janeiro.
    Retorna o DataFrame atualizado, um novo DataFrame de distâncias e bairros com erro.
    :param dataframe: DataFrame com os dados
    :param dataframe_distancias: DataFrame com as distâncias já calculadas
    :param geolocator: Objeto geolocator
    :param bairros_falha_existentes: Conjunto de bairros que falharam anteriormente
    :return: DataFrame, DataFrame, Conjunto de bairros falhos atualizado
    """
    # Filtrar somente cidades e bairros dentro do estado do RJ
    dataframe = dataframe[dataframe['ESTADO'] == 'Rio de Janeiro']

    cache_distancias = dataframe_distancias.set_index('BAIRRO')[
        'DISTANCIA_URCA'].to_dict() if not dataframe_distancias.empty else {}

    if 'DISTANCIA_URCA' not in dataframe.columns:
        dataframe['DISTANCIA_URCA'] = np.NaN

    # Inicializa listas para armazenar bairros bem-sucedidos e com erro
    bairros_sucesso = []
    bairros_falha = bairros_falha_existentes.copy()  # Copiamos os bairros falhos existentes

    for index, row in dataframe.iterrows():
        bairro = row['BAIRRO']
        if bairro.lower() == 'urca':
            dataframe.at[index, 'DISTANCIA_URCA'] = 0.0
            bairros_sucesso.append(bairro)
            continue

        # Verifica se o bairro já falhou anteriormente
        if bairro in bairros_falha:
            print(f"Pulado {bairro}, falhou anteriormente.")
            dataframe.at[index, 'DISTANCIA_URCA'] = np.NaN
            continue

        if bairro not in cache_distancias or pd.isna(cache_distancias[bairro]) or cache_distancias[bairro] <= 0:
            distancia = calcular_distancia_ate_urca(bairro, row['CIDADE'], row['ESTADO'], geolocator)
            cache_distancias[bairro] = distancia

        dataframe.at[index, 'DISTANCIA_URCA'] = cache_distancias[bairro]

        # Verifica se a distância foi calculada corretamente
        if pd.notna(cache_distancias[bairro]):
            bairros_sucesso.append(bairro)
        else:
            bairros_falha.add(bairro)  # Adiciona o bairro na lista de falhas

    # Atualiza o DataFrame de distâncias apenas se houver mudanças
    new_df_distancias = pd.DataFrame(list(cache_distancias.items()), columns=['BAIRRO', 'DISTANCIA_URCA'])

    # Printar o número de bairros processados e os bairros que falharam
    print(f"\nTotal de bairros processados com sucesso: {len(bairros_sucesso)}")
    print(f"Bairros processados: {', '.join(bairros_sucesso)}")

    print(f"\nTotal de bairros que falharam ao calcular a distância: {len(bairros_falha - bairros_falha_existentes)}")
    print(f"Bairros com falha nesta execução: {', '.join(bairros_falha - bairros_falha_existentes)}")

    return dataframe, new_df_distancias, bairros_falha


# Uso do código
if __name__ == "__main__":
    df = carregar_dados()
    df_distancias = carregar_dados('dados/processado/dfDistancias.csv')

    # Carrega bairros que falharam anteriormente
    bairros_falha_existentes = carregar_bairros_falha()

    df, updated_df_distancias, bairros_falha_atualizado = adicionar_distancia_ate_urca(
        df, df_distancias, inicializar_geolocator(), bairros_falha_existentes
    )

    # Printar dataframe com resultados e salvar
    print(df[['BAIRRO', 'CIDADE', 'ESTADO', 'DISTANCIA_URCA']].head())

    salvar_dados(updated_df_distancias, 'dados/processado/dfDistancias.csv')
    salvar_bairros_falha(bairros_falha_atualizado)
