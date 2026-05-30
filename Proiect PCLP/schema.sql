-- Schema for Hospital Implant Tracker

-- Table: User
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'doctor',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: ImplantType
CREATE TABLE implant_type (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Table: Implant
CREATE TABLE implant (
    id INTEGER PRIMARY KEY,
    implant_id VARCHAR(50) UNIQUE NOT NULL,
    type_id INTEGER NOT NULL,
    patient_name VARCHAR(100) NOT NULL,
    doctor_id INTEGER NOT NULL,
    implant_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (type_id) REFERENCES implant_type(id),
    FOREIGN KEY (doctor_id) REFERENCES user(id)
);


INSERT INTO user (id, username, email, password_hash, role) VALUES
(1, 'dr.popescu', 'popescu@example.com', 'hashed_pass_1', 'doctor'),
(2, 'dr.ionescu', 'ionescu@example.com', 'hashed_pass_2', 'doctor'),
(3, 'admin', 'admin@example.com', 'hashed_pass_3', 'admin'),
(4, 'dr.george', 'george@example.com', 'hashed_pass_4', 'doctor'),
(5, 'dr.matei', 'matei@example.com', 'hashed_pass_5', 'doctor');

INSERT INTO implant_type (id, name) VALUES
(1, 'Titanium'),
(2, 'Ceramic'),
(3, 'Zirconia'),
(4, 'Polyethylene'),
(5, 'Stainless Steel');

INSERT INTO implant (id, implant_id, type_id, patient_name, doctor_id, implant_date, status, notes) VALUES
(1, 'IMP-001', 1, 'Ion Vasile', 1, '2024-05-01', 'Active', 'No complications.'),
(2, 'IMP-002', 2, 'Maria Popa', 2, '2024-04-15', 'Active', 'Initial discomfort reported.'),
(3, 'IMP-003', 3, 'Gheorghe Ionescu', 1, '2024-03-20', 'Inactive', 'Implant removed due to infection.'),
(4, 'IMP-004', 4, 'Elena Radu', 4, '2024-06-10', 'Active', NULL),
(5, 'IMP-005', 5, 'Alexandru Dinu', 5, '2024-05-30', 'Active', 'Patient scheduled for follow-up.');


