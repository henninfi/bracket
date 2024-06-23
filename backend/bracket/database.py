from typing import Any

import sqlalchemy
from databases import Database
from heliclockter import datetime_utc

from bracket.config import config


def datetime_decoder(value: str) -> datetime_utc:
    value = value.split(".")[0].replace("+00", "+00:00")
    return datetime_utc.fromisoformat(value)


async def asyncpg_init(connection: Any) -> None:
    for timestamp_type in ("timestamp", "timestamptz"):
        await connection.set_type_codec(
            timestamp_type,
            encoder=datetime_utc.isoformat,
            decoder=datetime_decoder,
            schema="pg_catalog",
        )

# # Define the event listener function
# def set_schema(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("SET search_path TO test;")
#     cursor.close()


database = Database(str(config.pg_dsn), init=asyncpg_init, min_size=1, max_size=5)

engine = sqlalchemy.create_engine(str(config.pg_dsn))

# # Establish a connection
# connection = engine.connect()

# # Attach the event listener
# sqlalchemy.event.listen(engine, 'connect', set_schema)