-- ============================================
-- CodeVerity Database Schema
-- ============================================

-- USERS (students, instructors, admins)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('STUDENT', 'INSTRUCTOR', 'ADMIN')),
    created_at TIMESTAMP DEFAULT NOW()
);

-- COURSES
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    instructor_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ASSIGNMENTS
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    language VARCHAR(20) NOT NULL,
    due_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- SUBMISSIONS
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES users(id),
    assignment_id INTEGER NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    code TEXT NOT NULL,
    language VARCHAR(20) NOT NULL,
    version INTEGER DEFAULT 1,
    submitted_at TIMESTAMP DEFAULT NOW()
);

-- FEATURES (extracted per submission)
CREATE TABLE features (
    id SERIAL PRIMARY KEY,
    submission_id INTEGER NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
    lexical JSONB,
    stylometric JSONB,
    structural JSONB,
    complexity JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- STUDENT_PROFILES (historical baseline per student)
CREATE TABLE student_profiles (
    id SERIAL PRIMARY KEY,
    student_id INTEGER UNIQUE NOT NULL REFERENCES users(id),
    submission_count INTEGER DEFAULT 0,
    avg_features JSONB,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- MODEL_VERSIONS (track which ML model produced which result)
CREATE TABLE model_versions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    trained_at TIMESTAMP,
    metrics JSONB
);

-- ANALYSIS_RESULTS
CREATE TABLE analysis_results (
    id SERIAL PRIMARY KEY,
    submission_id INTEGER UNIQUE NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
    status VARCHAR(30) NOT NULL CHECK (status IN ('LOW_RISK', 'REVIEW_RECOMMENDED', 'HIGH_RISK', 'INSUFFICIENT_EVIDENCE')),
    confidence FLOAT,
    model_version_id INTEGER REFERENCES model_versions(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- EVIDENCE (list of reasons per analysis result)
CREATE TABLE evidence (
    id SERIAL PRIMARY KEY,
    analysis_result_id INTEGER NOT NULL REFERENCES analysis_results(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    strength VARCHAR(20) CHECK (strength IN ('WEAK', 'MODERATE', 'STRONG'))
);

-- AUDIT_LOGS
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(255) NOT NULL,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);







-- ============================================
-- Indexes
-- ============================================


CREATE INDEX idx_submissions_student ON submissions(student_id);
CREATE INDEX idx_submissions_assignment ON submissions(assignment_id);
CREATE INDEX idx_analysis_status ON analysis_results(status);