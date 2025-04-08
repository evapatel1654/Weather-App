from flask import Flask, render_template, request, jsonify
from database import Database
from weather_api import WeatherAPI
from location_validator import LocationValidator
from export_handler import ExportHandler

app = Flask(__name__)
db = Database()
weather_api = WeatherAPI()
location_validator = LocationValidator()
export_handler = ExportHandler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    location = request.form.get('location')
    
    # Validate location
    validated_location = location_validator.validate(location)
    if not validated_location:
        return jsonify({'error': 'Invalid location'}), 400
    
    # Get weather data
    weather_data = weather_api.get_weather(validated_location)
    
    # Store in database
    db.create_weather_record(location, weather_data)
    
    return jsonify(weather_data)

@app.route('/history')
def get_history():
    records = db.get_all_records()
    return render_template('history.html', records=records)

@app.route('/export/<format>')
def export_data(format):
    data = db.get_all_records()
    return export_handler.export(data, format)

if __name__ == '__main__':
    app.run(debug=True)
