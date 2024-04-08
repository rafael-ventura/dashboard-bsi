from pandas import NA
import time
from geopy import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from src.utils import carregar_dados


def calcular_distancia_ate_urca(bairro, cache_distancias, bairros_nao_encontrados):
    """
    Calcula a distância entre a Urca e um bairro específico.
    """
    if bairro in cache_distancias:
        return cache_distancias[bairro]

    geolocator = Nominatim(user_agent="geolocalizacao_urca")

    # Defina o timeout como 5 segundos
    timeout = 5

    try:
        # Inclua o timeout na chamada geocode
        local_urca = geolocator.geocode("Urca, Rio de Janeiro, Rio de Janeiro", timeout=timeout)
        local_bairro = geolocator.geocode(f"{bairro}, Rio de Janeiro, Rio de Janeiro", timeout=timeout)

        if local_urca and local_bairro:
            distancia_km = geodesic((local_urca.latitude, local_urca.longitude),
                                    (local_bairro.latitude, local_bairro.longitude)).km
            cache_distancias[bairro] = round(distancia_km, 2)
            time.sleep(1)
            return cache_distancias[bairro]
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Erro ao geolocalizar {bairro}: {e}")

    bairros_nao_encontrados.append(bairro)
    return NA  # Retorna pd.NA em vez de None


def adicionar_distancia_ate_urca(dataframe):
    """
    Adiciona a coluna 'DISTANCIA_URCA' ao dataframe com a distância de cada bairro até a Urca.
    Calcula a distância apenas uma vez para cada bairro único e usa esse resultado para todos os alunos do mesmo bairro.
    """

    cache_distancias = {}
    bairros_nao_encontrados = []

    for bairro in dataframe['BAIRRO'].unique():
        distancia = calcular_distancia_ate_urca(bairro, cache_distancias, bairros_nao_encontrados)
        cache_distancias[bairro] = distancia

    dataframe['DISTANCIA_URCA'] = dataframe['BAIRRO'].map(cache_distancias)

    if bairros_nao_encontrados:
        print("Bairros não encontrados:", set(bairros_nao_encontrados))

    return dataframe


if __name__ == "__main__":
    df = carregar_dados()
    df = adicionar_distancia_ate_urca(df)
    print(df['DISTANCIA_URCA'])
