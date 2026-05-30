-- Queries for Hospital Implant Tracker

-- Query: Get total number of implants
SELECT COUNT(*) AS total_implants FROM implant;

-- Query: Get implants by type
SELECT it.name, COUNT(i.id) AS count
FROM implant_type it
JOIN implant i ON it.id = i.type_id
GROUP BY it.name;

-- Query: Get implants by status
SELECT status, COUNT(id) AS count
FROM implant
GROUP BY status;

-- Query: Get implants added this month
SELECT COUNT(*) AS implants_this_month
FROM implant
WHERE created_at >= date('now', 'start of month');

-- Query: Get top doctors by number of implants managed
SELECT u.username, COUNT(i.id) AS count
FROM user u
JOIN implant i ON u.id = i.doctor_id
WHERE u.role = 'doctor'
GROUP BY u.id, u.username
ORDER BY count DESC
LIMIT 5;

-- Query: Get recent implants (last 5)
SELECT *
FROM implant
ORDER BY created_at DESC
LIMIT 5;

-- Query: Get implants for a specific doctor
SELECT *
FROM implant
WHERE doctor_id = :doctor_id;

-- Query: Get implants filtered by type and status
SELECT *
FROM implant
WHERE type_id = :type_id AND status = :status;

-- Query: Get implants filtered by doctor, type, and status
SELECT *
FROM implant
WHERE doctor_id = :doctor_id AND type_id = :type_id AND status = :status;

-- Query: Get monthly trend for the past 6 months
SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS count
FROM implant
WHERE created_at >= date('now', '-6 months')
GROUP BY month
ORDER BY month; 