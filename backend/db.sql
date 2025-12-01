-- Admins table
CREATE TABLE Admins (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Calendar entries (Kalenderluker)
CREATE TABLE CalendarEntries (
    id SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    youtube_url VARCHAR(255),
    task_text TEXT,
    video_type VARCHAR(10) CHECK (video_type IN ('youtube', 'upload')),
    video_path VARCHAR(255),
    created_by INTEGER REFERENCES Admins(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_published BOOLEAN DEFAULT FALSE
);

-- Visitor tokens for guest recognition
CREATE TABLE Visitors (
    token_id UUID PRIMARY KEY,
    first_visit TIMESTAMP DEFAULT NOW()
);

-- Log of guest accesses to calendar entries
CREATE TABLE AccessLogs (
    id SERIAL PRIMARY KEY,
    visitor_token UUID REFERENCES Visitors(token_id),
    calendar_id INTEGER REFERENCES CalendarEntries(id),
    access_time TIMESTAMP DEFAULT NOW()
);
