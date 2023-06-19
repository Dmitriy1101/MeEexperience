import psycopg2
import sqlalchemy

DSN = 'postgresql://postgres:NotGoodNotBad@localhost:5432/music_service'
engine = sqlalchemy.create_engine(DSN)