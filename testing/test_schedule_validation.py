import pytest
import sys
from python import schedule_validation as sv

# Construct a schedule for testing
# Courses
def test_make_courses():
    math111 = sv.Course('Calculus I', 'MATH', '111', 4.0, pc.get_course_prereqs('MATH', 111))
    math112 = sv.Course('Calculus II', 'MATH', '112', 4.0, pc.get_course_prereqs('MATH', 112))
    hass100 = sv.Course('Nature and Human Values', 'HASS', '100', 3.0, pc.get_course_prereqs('HASS', 100))
    phgn100 = sv.Course('Physics I', 'PHGN', '100', 4.5, pc.get_course_prereqs('PHGN', 100))
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSM', 101)
    csm101 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CHGN', 121)
    chgn121 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSCI', 101)
    csci101 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('EDNS', 151)
    edns151 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSCI', 261)
    csci261 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('MATH', 213)
    math213 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('PHGN', 200)
    phgn200 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSCI', 274)
    csci274 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSCI', 262)
    csci262 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('EBGN', 201)
    ebgn201 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('MATH', 225)
    math225 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSCI', 358)
    csci358 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSCI', 341)
    csci341 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('HASS', 200)
    hass200 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('EENG', 281)
    eeng281 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('EENG', 307)
    eeng307 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('MATH', 332)
    math332 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSCI', 306)
    csci306 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('MEGN', 441)
    megn441 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('MATH', 201)
    math201 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSCI', 406)
    csci406 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSCI', 404)
    csci404 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSCI', 470)
    csci470 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSCI', 370)
    csci370 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSCI', 400)
    csci400 = sv.Course(name, dept, cn, hours, prereqs, coreqs)
    name, dept, cn, hours, prereqs, coreqs = pc.get_course_info('CSCI', 442)
    csci442 = sv.Course(name, dept, cn, hours, prereqs, coreqs)

    # Construct semesters
        # Add courses to semesters
    semester1 = sv.Semester('Fall 2020', [math111, hass100, chgn121, csci101, csm101])
    semester2 = sv.Semester('Spring 2021', [math112, phgn100, edns151, csci261])
    semester3 = sv.Semester('Fall 2021', [math213, phgn200, csci274, csci262, ebgn201])
    semester4 = sv.Semester('Spring 2022', [math225, csci358, csci341, hass200, eeng281])
    semester5 = sv.Semester('Fall 2022', [eeng307, math332, csci306, megn441, math201])
    semester6 = sv.Semester('Spring 2023', [csci406, csci404, csci470])
    semester7 = sv.Semester('Summer 2023', [csci370])
    semester8 = sv.Semester('Fall 2023', [csci400])
    semester9 = sv.Semester('Spring 2024', [csci442])

    # Construct a schedule
        # Add semesters to schedule
    schedule = sv.Schedule([semester1, semester2, semester3, semester4, semester5, semester6, semester7, semester8, semester9])

    assert(1 == 1)