import json, requests
from geopy.geocoders import Nominatim
import SECRETS

# takes arguments of current city or zip code from the command line
# returns temperature, humidity, 

class weatherAPICall:
    
    def __init__(self, cityAndState, AlertContents = None, PointContents = None,
                Temp = None, Conditions = None, Lat = None, Lon = None) -> None:
        self.cityAndState = cityAndState
        self.AlertContents = AlertContents
        self.PointContents = PointContents
        self.Temp = None
        self.TempUnit = None
        self.WindSpeed = None
        self.WindDirection = None
        self.Conditions = Conditions
        self.Lat, self.Lon = self.getLatLon()  
        self.ForecastURL = self.pointsCall(self.Lat, self.Lon)
        
    def pointsCall(self, lat, lon):
        url = f"https://api.weather.gov/points/{self.Lat},{self.Lon}"
        response = requests.get(url)
        self.PointContents = json.loads(response.content)
        ForecastURL = self.PointContents['properties']['forecast']
        return ForecastURL
        
    def getLatLon(self):
        # Initialize Nominatim API
        geolocator = Nominatim(user_agent="MyApp")
        cityAndStateList  = self.cityAndState.replace(', ', ' ').split()
        cityAndStateDict = {'city':cityAndStateList[0], 'state':cityAndStateList[1]}
        location = geolocator.geocode(cityAndStateDict)
        return location.latitude, location.longitude
    
    def getForecast(self):
        forecastResponse = json.loads(requests.get(self.ForecastURL).content)
        self.Temp = forecastResponse['properties']['periods'][0]['temperature']
        self.TempUnit = forecastResponse['properties']['periods'][0]['temperatureUnit']
        self.WindSpeed = forecastResponse['properties']['periods'][0]['windSpeed']
        self.WindDirection = forecastResponse['properties']['periods'][0]['windDirection']
        self.Humidity = forecastResponse['properties']['periods'][0]['relativeHumidity']['value']
