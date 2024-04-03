# Calcula distância entre dois bairros 
#  A geopy utiliza o serviço de localização Nominatim
# https://nominatim.openstreetmap.org/ui/search.html

from geopy.geocoders import Nominatim
from geopy import distance

geolocator = Nominatim(user_agent="geolocalização")
lugar = "Urca, Rio de Janeiro, Rio de Janeiro"
localizacao = geolocator.geocode(lugar)
#print(location)
print(lugar, ":", (localizacao.latitude, localizacao.longitude))

print()
lugar2 = "Flamengo, Rio de Janeiro, Rio de Janeiro"
localizacao2 = geolocator.geocode(lugar2)
#print(location2)
print(lugar2, ":", (localizacao2.latitude, localizacao2.longitude))

print()
distancia = distance.distance((localizacao.latitude, localizacao.longitude), (localizacao2.latitude, localizacao2.longitude)).km

print("Distância = ", round(distancia,2), "Km")