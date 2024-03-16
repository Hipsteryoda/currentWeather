import json, requests
from geopy.geocoders import Nominatim

# takes arguments of current city or zip code from the command line
# returns temperature, humidity, 
# Weather API: https://www.weather.gov/documentation/services-web-api#/

class weatherAPICall:
    
    def __init__(self, cityAndState) -> None:
        self.cityAndState = cityAndState
        self.PointContents = None
        self.Conditions = None
        self.Lat, self.Lon = self.getLatLon()  
        self.ForecastURL = self.pointsCall(self.Lat, self.Lon)
        self.getForecast()
        
        # UNUSED
        # self.AlertContents = None
        # self.Temp = None
        # self.TempUnit = None
        # self.WindSpeed = None
        # self.WindDirection = None
        # self.Humidity = None
        
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

if __name__ == '__main__':
    import sys
    # Get the city and state as the last argument
    cityAndState = sys.argv[-1]
    # Instantiate the weather object
    weather = weatherAPICall(cityAndState)
    
    # Print out some details
    print(f"The current temperature in {cityAndState} is: {weather.Temp}{weather.TempUnit}")
    print(f"The current wind is: {weather.WindSpeed} from the {weather.WindDirection}")
    print(f"The current relative humidity is: {weather.Humidity}")
    
    
    
    
    