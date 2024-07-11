from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
weather_api_key = '3c195f88f2b5332c421ae8dd55ae467e'
autocomplete_api_url = 'http://api.openweathermap.org/data/2.5/find'
geolocation_api_url = 'http://ip-api.com/json/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    units = request.form.get('units', 'metric')  # Default to metric units (Celsius)
    
    if not city:  # If city is not provided, attempt to get user's location
        try:
            response = requests.get(geolocation_api_url)
            location_data = response.json()
            city = location_data['city']
        except Exception as e:
            return render_template('error.html', error=str(e))
    
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units={units}'
    
    try:
        response = requests.get(api_url)
        data = response.json()
        
        if response.status_code == 200:
            weather_data = {
                'city': city,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'temperature_unit': units
            }
            return render_template('weather.html', weather=weather_data)
        else:
            error_message = data['message']
            return render_template('error.html', error=error_message)
    
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('query')
    params = {
        'q': query,
        'type': 'like',
        'sort': 'population',
        'cnt': 10,
        'appid': weather_api_key
    }
    response = requests.get(autocomplete_api_url, params=params)
    cities = [city['name'] for city in response.json()['list']]
    return jsonify(cities)

if __name__ == '__main__':
    app.run(debug=True)

