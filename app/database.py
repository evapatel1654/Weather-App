from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class WeatherRecord(Base):
    __tablename__ = 'weather_records'
    
    id = Column(Integer, primary_key=True)
    location = Column(String)
    temperature = Column(Float)
    conditions = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Database:
    def __init__(self):
        self.engine = create_engine('sqlite:///weather.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_weather_record(self, location, weather_data):
        record = WeatherRecord(
            location=location,
            temperature=weather_data['temperature'],
            conditions=weather_data['conditions']
        )
        self.session.add(record)
        self.session.commit()

    def get_all_records(self):
        return self.session.query(WeatherRecord).all()

    def update_record(self, record_id, data):
        record = self.session.query(WeatherRecord).get(record_id)
        if record:
            for key, value in data.items():
                setattr(record, key, value)
            self.session.commit()

    def delete_record(self, record_id):
        record = self.session.query(WeatherRecord).get(record_id)
        if record:
            self.session.delete(record)
            self.session.commit()
