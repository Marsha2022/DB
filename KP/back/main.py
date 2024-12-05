from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime

import database_connection as db_conn


app = FastAPI()


@app.get("/")
async def welcome():
    return {"message": "The server is running"}


class LoginRequest(BaseModel):
    username: str
    hashed_password: str


@app.post("/login")
async def login(data: LoginRequest):
    query = """
    SELECT username, hashed_password, user_type
      FROM users
     WHERE username = $1;
    """
    try:
        user_data = await db_conn.execute_query(query, data.username)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        user = user_data[0]
        if user["hashed_password"] != data.hashed_password:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        return {"message": "Login successful", "user_type": user["user_type"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@app.post("/users/")
async def get_all_users():
    query = """
    SELECT username, email, user_type, created_date
      FROM users;
    """
    try:
        result = await db_conn.execute_query(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


class AddUserRequest(BaseModel):
    username: str
    hashed_password: str
    email: str
    user_type: str
    created_date: str


@app.post("/users/add")
async def add_user(data: AddUserRequest):
    query = """
    INSERT INTO users (username, hashed_password, email, user_type, created_date)
    VALUES ($1, $2, $3, $4, $5);
    """
    try:
        created_date = datetime.datetime.fromisoformat(data.created_date)
        await db_conn.execute_query(query, data.username, data.hashed_password, data.email, data.user_type, created_date)
        return {"message": "User added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


class DeleteUserRequest(BaseModel):
    username: str


@app.post("/users/delete")
async def delete_user(data: DeleteUserRequest):
    query = """
    DELETE FROM users
     WHERE username = $1;
    """
    try:
        await db_conn.execute_query(query, data.username)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@app.post("/schedule")
async def get_schedule():
    query = """
    SELECT t.tournament_name,
           tm1.team_name AS team1_name,
           tm2.team_name AS team2_name,
           m.match_date
      FROM matches m
           JOIN tournaments t ON m.tournament_id = t.tournament_id
           JOIN teams tm1 ON m.team1_id = tm1.team_id
           JOIN teams tm2 ON m.team2_id = tm2.team_id;
    """
    try:
        schedule_data = await db_conn.execute_query(query)
        return schedule_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@app.post("/teams")
async def get_teams():
    try:
        query = """
            SELECT t.team_name,
                   c.username AS captain_name,
                   u.username AS member_name
            FROM teams t
            JOIN users c ON t.captain_id = c.user_id
            JOIN team_members tm ON t.team_id = tm.team_id
            JOIN users u ON tm.user_id = u.user_id
        """
        result = await db_conn.execute_query(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
