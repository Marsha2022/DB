import asyncpg
from fastapi import HTTPException


DB_PARAMS = {
    "database": "tournamentdb",
    "user": "tournamentdb_owner",
    "password": "n7OlDfCm1SLV",
    "host": "ep-soft-dawn-a5fverwq.us-east-2.aws.neon.tech",
    "port": "5432",
}


async def execute_query(query, *parameters):
    connection = await asyncpg.connect(**DB_PARAMS)
    try:
        results = await connection.fetch(query, *parameters)
        return [dict(row) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        await connection.close()
