from sqlalchemy import create_engine, Column, Integer, String, JSON, Table, MetaData
import databases

DATABASE_URL = "postgresql+asyncpg://tug_user:tug_pass@db:5432/tug_db"

database = databases.Database(DATABASE_URL)
metadata = MetaData()

resultados = Table(
    "resultados",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre_archivo", String),  
    Column("muestra_id", Integer),
    Column("timestamp", String),       
    Column("resultado", JSON)          
)

engine = create_engine(DATABASE_URL.replace("+asyncpg", ""))
metadata.create_all(engine)
