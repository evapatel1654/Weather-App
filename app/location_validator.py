from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import re

class LocationValidator:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="weather_app")

    def validate(self, location):
        """Validate and normalize location input"""
        if self._is_zip_code(location):
            return self._validate_zip_code(location)
        elif self._is_coordinates(location):
            return self._validate_coordinates(location)
        else:
            return self._validate_city_name(location)

    def _is_zip_code(self, location):
        """Check if input is a ZIP code"""
        zip_pattern = r'^\d{5}(-\d{4})?$'  # US ZIP code pattern
        return bool(re.match(zip_pattern, location))

    def _is_coordinates(self, location):
        """Check if input is coordinates"""
        coord_pattern = r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'
        return bool(re.match(coord_pattern, location))

    def _validate_zip_code(self, zip_code):
        try:
            location = self.geolocator.geocode(zip_code)
            if location:
                return f"{location.address}"
            return None
        except GeocoderTimedOut:
            return None

    def _validate_coordinates(self, coords):
        try:
            lat, lon = map(float, coords.split(','))
            location = self.geolocator.reverse((lat, lon))
            if location:
                return f"{location.address}"
            return None
        except (ValueError, GeocoderTimedOut):
            return None

    def _validate_city_name(self, city):
        try:
            location = self.geolocator.geocode(city)
            if location:
                return f"{location.address}"
            return None
        except GeocoderTimedOut:
            return None
