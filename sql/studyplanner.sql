create database studyplanner;

use studyplanner;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE study_plans (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    topic VARCHAR(255) NOT NULL,
    exam_date DATE NOT NULL,
    study_date DATE NOT NULL,
    completed TINYINT(1) DEFAULT 0,
    PRIMARY KEY (id),
    KEY user_id (user_id)
);