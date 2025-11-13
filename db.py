from sqlalchemy import create_engine, Column, Integer, String, JSON, Table, MetaData, Float, DateTime, Text, Boolean, ForeignKey, Date
import databases
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
import os

# Neon Tech Database Connection - Con valores por defecto
DB_USER = os.getenv('DB_USER', 'neondb_owner')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'npg_1z5eRvbokuXr')
DB_HOST = os.getenv('DB_HOST', 'ep-ancient-forest-ahbu5yy8-pooler.us-east-1.aws.neon.tech')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'neondb')
DB_SSLMODE = os.getenv('DB_SSLMODE', 'require')

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSLMODE}"
SYNC_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSLMODE}"

database = databases.Database(DATABASE_URL)
metadata = MetaData()

patient = Table(
    "patient",
    metadata,
    Column("id", String, primary_key=True, default=uuid.uuid4),
    Column("national_id", String)  
)

test = Table(
    "test",
    metadata,
    Column("id", String, primary_key=True, default=uuid.uuid4),
    Column("file_name", String),
    Column("patient_id", String, ForeignKey("patient.id"))
)

sample = Table(
    "sample",
    metadata,
    Column("id", String, primary_key=True, default=uuid.uuid4),
    Column("number", String),  
    Column("date", Date),      
    Column("test_id", String, ForeignKey("test.id"))
)

sample_graphics = Table(
    "sample_graphics",
    metadata,
    Column("graphic_id", String,ForeignKey("graphics.id")),
    Column("sample_id", String, ForeignKey("sample.id"))
)

graphics = Table(
    "graphics",
    metadata,
    Column("id", String, primary_key=True, default=uuid.uuid4),
    Column("name", String)
)

metricvalue = Table(
    "metricvalue",
    metadata,
    Column("id", String, primary_key=True, default=uuid.uuid4), 
    Column("value", String),
    Column("metric_id", String, ForeignKey("metric.id")),
    Column("sample_id", String, ForeignKey("sample.id"))
)

metric = Table(
    "metric",
    metadata,
    Column("id", String, primary_key=True, default=uuid.uuid4),
    Column("name", String),
    Column("is_active", Boolean, default=True),
    Column("phase_id", String, ForeignKey("phase.id")),
    Column("measurement_units_id", String, ForeignKey("measurement_units.id"))
)

phase = Table(
    "phase",
    metadata,
    Column("id", String, primary_key=True, default=uuid.uuid4),
    Column("name", String)
)

measurement_units = Table(
    "measurement_units",
    metadata,
    Column("id", String, primary_key=True, default=uuid.uuid4),
    Column("name", String)
)

def init_db():
    engine = create_engine(SYNC_DATABASE_URL)
    try:
        metadata.create_all(engine, checkfirst=True)
        print("Tablas creadas o verificadas!")
    except Exception as e:
        print(f"Error al crear tablas: {e}")
        # Continuar si las tablas ya existen

init_db()