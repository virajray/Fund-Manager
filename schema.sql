DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS Admins;

CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    index_number TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE Payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    month TEXT NOT NULL,
    amount_paid REAL NOT NULL,
    payment_date TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

CREATE TABLE Admins(
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Add a default admin user (IMPORTANT: Change the password!)
INSERT INTO Admins (username, password) VALUES ('codex', 'f6b3mns33dw');
INSERT INTO Students (index_number, name, password) VALUES ('1001', 'Dinithi', 'dinithi123');
INSERT INTO Students (index_number, name, password) VALUES ('1002', 'Waruni', 'warunimodai');