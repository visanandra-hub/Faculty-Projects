-- Schema for Hospital Implant Tracker

-- Table: User
CREATE TABLE user (
    id INTEGER PRIMARY KEY,  -- ID unic pentru fiecare utilizator (doctor, admin etc.)
    username VARCHAR(64) UNIQUE NOT NULL,  -- Nume de utilizator, trebuie să fie unic
    email VARCHAR(120) UNIQUE NOT NULL,    -- Email-ul, unic și obligatoriu
    password_hash VARCHAR(256) NOT NULL,   -- Parola criptată
    role VARCHAR(20) NOT NULL DEFAULT 'doctor',  -- Rolul utilizatorului (default: doctor)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Data la care a fost creat contul
);

-- Table: ImplantType
CREATE TABLE implant_type (
    id INTEGER PRIMARY KEY,   -- ID unic pentru fiecare tip de implant
    name VARCHAR(100) UNIQUE NOT NULL  -- Numele tipului de implant (ex: Titanium), trebuie să fie unic
);

-- Table: Implant
CREATE TABLE implant (
    id INTEGER PRIMARY KEY,  -- ID intern al implantului
    implant_id VARCHAR(50) UNIQUE NOT NULL,  -- Cod unic extern pentru implant (ex: IMP-001)
    type_id INTEGER NOT NULL,  -- Tipul implantului (cheie străină către implant_type)
    patient_name VARCHAR(100) NOT NULL,  -- Numele pacientului care a primit implantul
    doctor_id INTEGER NOT NULL,  -- Doctorul care a făcut implantul (cheie străină către user)
    implant_date DATE NOT NULL,  -- Data efectuării implantului
    status VARCHAR(20) NOT NULL DEFAULT 'Active',  -- Starea implantului (Active, Inactive etc.)
    notes TEXT,  -- Observații medicale despre implant
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Data la care a fost înregistrat implantul
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Data ultimei actualizări
    FOREIGN KEY (type_id) REFERENCES implant_type(id),  -- Legătură cu tabela de tipuri
    FOREIGN KEY (doctor_id) REFERENCES user(id)         -- Legătură cu tabela de utilizatori
);

-- Queries

-- Query: Get total number of implants
SELECT COUNT(*) AS total_implants FROM implant;
-- Returnează numărul total de implanturi înregistrate în baza de date

-- Query: Get implants by type
SELECT it.name, COUNT(i.id) AS count
FROM implant_type it
JOIN implant i ON it.id = i.type_id
GROUP BY it.name;
-- Afișează câte implanturi sunt din fiecare tip (Titanium, Ceramic etc.)

-- Query: Get implants by status
SELECT status, COUNT(id) AS count
FROM implant
GROUP BY status;
-- Afișează câte implanturi sunt pe fiecare stare (Active, Inactive, etc.)

-- Query: Get implants added this month
SELECT COUNT(*) AS implants_this_month
FROM implant
WHERE created_at >= date('now', 'start of month');
-- Numără câte implanturi au fost adăugate de la începutul lunii curente până în prezent

-- Query: Get top doctors by number of implants managed
SELECT u.username, COUNT(i.id) AS count
FROM user u
JOIN implant i ON u.id = i.doctor_id
WHERE u.role = 'doctor'
GROUP BY u.id, u.username
ORDER BY count DESC
LIMIT 5;
-- Afișează cei mai activi 5 doctori în funcție de numărul de implanturi gestionate

-- Query: Get recent implants (last 5)
SELECT *
FROM implant
ORDER BY created_at DESC
LIMIT 5;
-- Afișează ultimele 5 implanturi adăugate, începând cu cel mai recent

-- Query: Get implants for a specific doctor
SELECT *
FROM implant
WHERE doctor_id = :doctor_id;
-- Afișează toate implanturile realizate de un anumit doctor (se înlocuiește `:doctor_id` cu ID-ul doctorului)

-- Query: Get implants filtered by type and status
SELECT *
FROM implant
WHERE type_id = :type_id AND status = :status;
-- Afișează implanturile care au un anumit tip și o anumită stare

-- Query: Get implants filtered by doctor, type, and status
SELECT *
FROM implant
WHERE doctor_id = :doctor_id AND type_id = :type_id AND status = :status;
-- Afișează implanturile după doctor, tip și stare, toate simultan

-- Query: Get monthly trend for the past 6 months
SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS count
FROM implant
WHERE created_at >= date('now', '-6 months')
GROUP BY month
ORDER BY month;
-- Afișează numărul de implanturi adăugate în fiecare lună, în ultimele 6 luni
