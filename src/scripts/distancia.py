import pandas as pd
import numpy as np
from geopy import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

from src.utils import carregar_dados, salvar_dados


def inicializar_geolocator():
    """Inicializa e retorna um objeto geolocator."""
    return Nominatim(user_agent="geolocalizacao_urca")


def calcular_distancia_ate_urca(bairro, cidade, estado, geolocator):
    """
    Calcula a distância entre um bairro e a Urca, no Rio de Janeiro.
    Retorna a distância calculada ou np.NaN se não for possível calcular.
    """
    try:
        time.sleep(1)  # Evita sobrecarga na API
        endereco_bairro = f"{bairro}, {cidade}, {estado}"
        local_urca = geolocator.geocode("Urca, Rio de Janeiro, Rio de Janeiro")
        local_bairro = geolocator.geocode(endereco_bairro)
        if local_urca and local_bairro:
            return round(geodesic((local_urca.latitude, local_urca.longitude),
                                  (local_bairro.latitude, local_bairro.longitude)).km, 2)
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Erro ao geolocalizar {bairro}: {e}")
    return np.NaN


def adicionar_distancia_ate_urca(df, df_distancias, geolocator):
    """
    Atualiza ou adiciona distâncias do DataFrame principal baseando-se nas distâncias já calculadas.
    Calcula novas distâncias apenas para bairros sem dados válidos.
    """
    cache_distancias = df_distancias.set_index('BAIRRO')['DISTANCIA_URCA'].to_dict() if not df_distancias.empty else {}

    if 'DISTANCIA_URCA' not in df.columns:
        df['DISTANCIA_URCA'] = np.NaN

    for index, row in df.iterrows():
        bairro = row['BAIRRO']
        if bairro not in cache_distancias or pd.isna(cache_distancias[bairro]) or cache_distancias[bairro] <= 0:
            cache_distancias[bairro] = calcular_distancia_ate_urca(bairro, row['CIDADE'], row['ESTADO'], geolocator)
        df.at[index, 'DISTANCIA_URCA'] = cache_distancias[bairro]

    # Atualiza o DataFrame de distâncias apenas se houver mudanças
    new_df_distancias = pd.DataFrame(list(cache_distancias.items()), columns=['BAIRRO', 'DISTANCIA_URCA'])
    return df, new_df_distancias


# Uso do código
if __name__ == "__main__":
    df = carregar_dados()
    df_distancias = carregar_dados('dados/processado/dfDistancias.csv')
    df, updated_df_distancias = adicionar_distancia_ate_urca(df, df_distancias)
    print(df[['BAIRRO', 'CIDADE', 'ESTADO', 'DISTANCIA_URCA']].head())
    salvar_dados(updated_df_distancias, 'dados/processado/dfDistancias.csv')
