CREATE DATABASE codedock;

\c codedock;

CREATE TABLE IF NOT EXISTS programs (
    id BIGSERIAL PRIMARY KEY,
    language VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    code TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS execution_history (
    id BIGSERIAL PRIMARY KEY,
    program_id BIGINT REFERENCES programs(id) ON DELETE SET NULL,
    input TEXT,
    output TEXT,
    error TEXT,
    execution_time BIGINT,
    memory BIGINT,
    exit_code INTEGER,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);