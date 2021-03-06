DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS students_tasks;
DROP TABLE IF EXISTS task_answers;
DROP TABLE IF EXISTS emails;

CREATE TABLE students
(
    id INTEGER primary key,
    var INTEGER not null, 
    name varchar(32),
    role varchar(8),
    nicknames varchar(128)
);

CREATE TABLE tasks
(
    id INTEGER primary key,
    text varchar(64),
    attachments varchar(256),
    visibility integer
);

CREATE TABLE task_answers
(
    task_id INTEGER,
    id INTEGER,
    val varchar(32),
    color varchar(16),
    primary key (task_id, id)
);

CREATE TABLE students_tasks
(
    task_id INTEGER,
    student_id INTEGER,
  	answer varchar(256),
    primary key (task_id, student_id)
);

create table emails
(
    name varchar(64),
    email varchar(64)
);

