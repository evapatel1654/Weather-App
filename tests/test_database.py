import pytest
from app.database import Database, WeatherRecord
from datetime import datetime

@pytest.fixture
def db():
    # Use an in-memory SQLite database for testing
    db = Database('sqlite:///:memory:')
    return db

def test_create_weather_record(db):
    weather_data = {
        'temperature': 20,
        'conditions': 'sunny'
    }
    
    db.create_weather_record('London', weather_data)
    
    record = db.session.query(WeatherRecord).first()
    assert record.location == 'London'
    assert record.temperature == 20
    assert record.conditions == 'sunny'

def test_get_all_records(db):
    # Create some test records
    weather_data = {'temperature': 20, 'conditions': 'sunny'}
    db.create_weather_record('London', weather_data)
    db.create_weather_record('Paris', weather_data)
    
    records = db.get_all_records()
    assert len(records) == 2
    assert records[0].location == 'London'
    assert records[1].location == 'Paris'

def test_update_record(db):
    weather_data = {'temperature': 20, 'conditions': 'sunny'}
    db.create_weather_record('London', weather_data)
    
    record = db.session.query(WeatherRecord).first()
    db.update_record(record.id, {'temperature': 25})
    
    updated_record = db.session.query(WeatherRecord).first()
    assert updated_record.temperature == 25

def test_delete_record(db):
    weather_data = {'temperature': 20, 'conditions': 'sunny'}
    db.create_weather_record('London', weather_data)
    
    record = db.session.query(WeatherRecord).first()
    db.delete_record(record.id)
    
    assert db.session.query(WeatherRecord).count() == 0
