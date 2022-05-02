
CREATE TABLE IF NOT EXISTS courses (
    department TEXT NOT NULL,
    course_number INTEGER NOT NULL,
    course_title TEXT NOT NULL,
    course_description TEXT NOT NULL,
    semester_hours NUMERIC(5,2),
    fall INTEGER,
    spring INTEGER,
    summer INTEGER,
    winter INTEGER,
    equivalent_with TEXT DEFAULT 'None',
    prerequisites TEXT DEFAULT 'None',
    corequisites TEXT DEFAULT 'None',
    PRIMARY KEY (department, course_number)
);





