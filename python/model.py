from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Define the base class for models
Base = declarative_base()

# SynopData table schema
class SynopData(Base):
    __tablename__ = 'synop_data'
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    file_content = Column(LargeBinary, nullable=False)
    timestamp = Column(String, nullable=False)  # Store extracted timestamp as string

# DecodedCSVData table schema
class DecodedCSVData(Base):
    __tablename__ = 'decoded_csv_data'
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    file_content = Column(LargeBinary, nullable=False)  # Storing CSV content
    timestamp = Column(String,nullable=False)

# class ContoursData(Base):
#     __tablename__ = 'contours_data'
#     id = Column(Integer, primary_key=True)
#     filename = Column(String, nullable=False)
#     file_path = Column(String, nullable=False)  # Path to the file on disk
#     timestamp = Column(String, nullable=False)  # Extracted from filename

# Set up the database connection
DATABASE_URL = 'sqlite:///weather_data.db'  # SQLite database for simplicity
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
