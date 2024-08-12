import pandas as pd
import numpy as np
from geopy import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

from src.utils.utils import carregar_dados, salvar_dados


def inicializar_geolocator():
    """
    Inicializa o objeto geolocator.
    :return: Objeto geolocator
    """
    return Nominatim(user_agent="geolocalizacao_urca")


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
            print("Calculando distância entre Urca e {}...".format(bairro))
            return round(geodesic((local_urca.latitude, local_urca.longitude),
                                  (local_bairro.latitude, local_bairro.longitude)).km, 2)
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Erro ao geolocalizar {bairro}: {e}")
    return np.NaN


def adicionar_distancia_ate_urca(dataframe, dataframe_distancias, geolocator):
    """
    Adiciona a distância entre um bairro e a Urca ao DataFrame.
    Retorna o DataFrame atualizado e um novo DataFrame de distâncias.
    :param dataframe: DataFrame com os dados
    :param dataframe_distancias: DataFrame com as distâncias já calculadas
    :param geolocator: Objeto geolocator
    :return: DataFrame, DataFrame
    """
    cache_distancias = dataframe_distancias.set_index('BAIRRO')[
        'DISTANCIA_URCA'].to_dict() if not dataframe_distancias.empty else {}

    if 'DISTANCIA_URCA' not in dataframe.columns:
        dataframe['DISTANCIA_URCA'] = np.NaN

    for index, row in dataframe.iterrows():
        bairro = row['BAIRRO']
        if bairro.lower() == 'urca':
            dataframe.at[index, 'DISTANCIA_URCA'] = 0.0
            continue
        if bairro not in cache_distancias or pd.isna(cache_distancias[bairro]) or cache_distancias[bairro] <= 0:
            cache_distancias[bairro] = calcular_distancia_ate_urca(bairro, row['CIDADE'], row['ESTADO'], geolocator)
        dataframe.at[index, 'DISTANCIA_URCA'] = cache_distancias[bairro]

    # Atualiza o DataFrame de distâncias apenas se houver mudanças
    new_df_distancias = pd.DataFrame(list(cache_distancias.items()), columns=['BAIRRO', 'DISTANCIA_URCA'])
    return dataframe, new_df_distancias


# Uso do código
if __name__ == "__main__":
    df = carregar_dados()
    df_distancias = carregar_dados('dados/processado/dfDistancias.csv')
    df, updated_df_distancias = adicionar_distancia_ate_urca(df, df_distancias, inicializar_geolocator())
    print(df[['BAIRRO', 'CIDADE', 'ESTADO', 'DISTANCIA_URCA']].head())
    salvar_dados(updated_df_distancias, 'dados/processado/dfDistancias.csv')
