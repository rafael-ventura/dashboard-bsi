from geopy.geocoders import Nominatim
from haversine import haversine, Unit
import pandas as pd


def calculate_distance(lat1, lon1, lat2, lon2):
    return haversine((lat1, lon1), (lat2, lon2), unit=Unit.KILOMETERS)


geolocator = Nominatim(user_agent="myGeocoder")
location_unirio = geolocator.geocode("UNIRIO")

df = pd.read_csv('../../dados/dfPrincipal.csv')

# Você precisará preencher a lista de bairros únicos
bairros = df['BAIRRO'].unique()

distancias = []

for bairro in bairros:
    location_bairro = geolocator.geocode(f"{bairro}, Rio de Janeiro")
    if location_bairro is not None:
        dist = calculate_distance(location_unirio.latitude, location_unirio.longitude, location_bairro.latitude,
                                  location_bairro.longitude)
        distancias.append((bairro, dist))

df_distancias = pd.DataFrame(distancias, columns=['BAIRRO', 'DISTANCIA'])

# Agora você pode fazer o merge com o dataframe original
df = df.merge(df_distancias, on='BAIRRO')
