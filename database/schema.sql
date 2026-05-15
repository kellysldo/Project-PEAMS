-- ============================================
-- Events Attendance Management System
-- Course: Information Management 1 - CCCS105
-- Database: CCCS105
-- ============================================

CREATE DATABASE IF NOT EXISTS CCCS105;
USE CCCS105;

-- -----------------------------------------------
-- Table: users
-- Organizers/admins who manage events
-- -----------------------------------------------
CREATE TABLE users (
    user_id     INT AUTO_INCREMENT PRIMARY KEY,
    full_name   VARCHAR(100),
    username    VARCHAR(50)  NOT NULL UNIQUE,
    email       VARCHAR(100) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        ENUM('admin', 'staff') DEFAULT 'staff',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------
-- Table: events
-- Events created and managed by users
-- -----------------------------------------------
CREATE TABLE events (
    event_id    INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    event_name  VARCHAR(100) NOT NULL,
    event_date  DATE         NOT NULL,
    location    VARCHAR(100),
    description TEXT,
    INDEX (user_id),  
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- -----------------------------------------------
-- Table: attendees
-- Participants who register for events
-- -----------------------------------------------
CREATE TABLE attendees (
    attendee_id  INT AUTO_INCREMENT PRIMARY KEY,
    fullname     VARCHAR(100) NOT NULL,
    email        VARCHAR(100) NOT NULL UNIQUE,
    contact_no   VARCHAR(20),
    address      VARCHAR(100)
);

-- -----------------------------------------------
-- Table: registrations
-- Links attendees to events; tracks attendance status
-- -----------------------------------------------
CREATE TABLE registrations (
    registration_id   INT AUTO_INCREMENT PRIMARY KEY,
    attendee_id       INT      NOT NULL,
    event_id          INT      NOT NULL,
    attendance_status ENUM('registered', 'present', 'absent') DEFAULT 'registered',
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (attendee_id) REFERENCES attendees(attendee_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id)    REFERENCES events(event_id)       ON DELETE CASCADE,
    UNIQUE KEY unique_registration (event_id, attendee_id)
);
