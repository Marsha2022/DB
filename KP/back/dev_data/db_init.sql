-- PostgreSQL Script to Initialize Tournament Monitoring Database
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    user_type VARCHAR(50) NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    captain_id INT REFERENCES users(user_id) ON DELETE SET NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE team_members (
    member_id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(team_id) ON DELETE CASCADE,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tournaments (
    tournament_id SERIAL PRIMARY KEY,
    tournament_name VARCHAR(150) NOT NULL,
    organizer_id INT REFERENCES users(user_id) ON DELETE SET NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    tournament_id INT REFERENCES tournaments(tournament_id) ON DELETE CASCADE,
    team1_id INT REFERENCES teams(team_id) ON DELETE SET NULL,
    team2_id INT REFERENCES teams(team_id) ON DELETE SET NULL,
    match_date TIMESTAMP NOT NULL,
    winner_team_id INT REFERENCES teams(team_id) ON DELETE SET NULL,
    score VARCHAR(20)
);

CREATE TABLE schedule (
    schedule_id SERIAL PRIMARY KEY,
    tournament_id INT REFERENCES tournaments(tournament_id) ON DELETE CASCADE,
    match_id INT REFERENCES matches(match_id) ON DELETE CASCADE,
    location VARCHAR(255) NOT NULL
);

CREATE TABLE tournament_bracket (
    bracket_id SERIAL PRIMARY KEY,
    tournament_id INT REFERENCES tournaments(tournament_id) ON DELETE CASCADE,
    match_id INT REFERENCES matches(match_id) ON DELETE CASCADE,
    stage VARCHAR(50) NOT NULL
);
