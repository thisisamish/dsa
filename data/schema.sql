CREATE TABLE IF NOT EXISTS resources (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL CHECK(type IN ('problem', 'tutorial')),
    platform TEXT NOT NULL CHECK(platform IN ('LC', 'NC', 'GFG', 'C360', 'IB', 'CC', 'CF', 'AC', 'TC', 'CSES', 'LINT', 'HE', 'HR', 'SPOJ', 'SCALER', 'PROGRAMIZ')),
    title TEXT NOT NULL UNIQUE,
    description TEXT,
    difficulty TEXT CHECK(difficulty in ('Trivial', 'Easy', 'Medium', 'Hard', 'Extra Hard')),
    href TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    deleted_at DATETIME
);

CREATE TABLE IF NOT EXISTS sheets (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    href TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    deleted_at DATETIME
);

CREATE TABLE IF NOT EXISTS sheet_resources (
    sheet_id INTEGER,
    resource_id TEXT,
    PRIMARY KEY (sheet_id, resource_id),
    FOREIGN KEY (sheet_id) REFERENCES sheets(id),
    FOREIGN KEY (resource_id) REFERENCES resources(id)
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    deleted_at DATETIME
);

CREATE TABLE IF NOT EXISTS resource_tags (
    resource_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (resource_id, tag_id),
    FOREIGN KEY (resource_id) REFERENCES resources(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);

CREATE TABLE IF NOT EXISTS prerequisites (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    deleted_at DATETIME
);

CREATE TABLE IF NOT EXISTS problem_prerequisites (
    resource_id INTEGER,
    prerequisite_id INTEGER,
    PRIMARY KEY (resource_id, prerequisite_id),
    FOREIGN KEY (resource_id) REFERENCES resources(id),
    FOREIGN KEY (prerequisite_id) REFERENCES prerequisites(id)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL unique,
    email TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    deleted_at DATETIME
)

-- problem_sheets.name ENUM
-- lc150 -> leetcode_150_sheet
-- lc75 -> leetcode_75_sheet
-- lb450 -> luv_babbars_450_sheet
-- nc250 -> neetcode_250_sheet
-- nc150 -> neetcode_150_sheet
-- nc75 -> neetcode_75_sheet
-- st75 -> strivers_blind_75_sheet
-- st79 -> strivers_79_sheet
-- sta2z -> strivers_a2z_sheet
-- stsde -> strivers_sde_sheet

-- all_problems.title ENUM
-- LC -> LeetCode
-- NC -> NeetCode
-- GFG -> Geeks For Geeks
-- C360 -> Code360
-- IB -> InterviewBit
-- CC -> CodeChef
-- CF -> Codeforces
-- AC -> AtCoder
-- TC -> TopCoder
-- CSES -> CSES
-- LINK -> LintCode
-- SPOJ -> Sphere Online Judge
-- HE -> HackerEarth
-- HR -> HackerRank
-- SCALER -> Scaler
-- PROGRAMIZ -> Programiz