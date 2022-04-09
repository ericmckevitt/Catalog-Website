
class Course:
    def __init__(self, name, hours=0.0, prerequisites=None, corequisites=None):
        self.name = name
        self.prerequisites = prerequisites
        self.corequisites = corequisites
        self.hours = hours

    def set_prerequisites(self, prerequisites):
        self.prerequisites = prerequisites

    def set_corequisites(self, corequisites):
        self.corequisites = corequisites

    def add_prerequisite(self, prerequisite):
        if self.prerequisites is not None:
            self.prerequisites.append(prerequisite)

    def add_corequisite(self, corequisite):
        if self.corequisites is not None:
            self.corequisites.append(corequisite)

    def __repr__(self):
        return f'Course({self.name}, {self.prerequisites}, {self.corequisites})'

    def get_name(self):
        return self.name

    def get_hours(self):
        return self.hours

    def get_prerequisites(self):
        return self.prerequisites

    def get_corequisites(self):
        return self.corequisites


class Semester:
    def __init__(self, name, courses=None):
        self.name = name
        self.courses = courses

    def __repr__(self):
        return f"Semester({self.name}, {self.courses})"

    def add_course(self, course):
        self.courses.append(course)

    def get_courses(self):
        return self.courses

    def get_name(self):
        return self.name

    def get_total_hours(self):
        total_hours = 0
        for course in self.courses:
            total_hours += course.get_hours()
        return total_hours


class Schedule:
    def __init__(self, semesters=None):
        self.semesters = semesters

    def __repr__(self):
        output = f""
        for semester in self.semesters:
            semester_name = semester.get_name()
            output += f"{semester_name}\n"
            for course in semester.get_courses():
                output += f"\t{course.get_name()}\n"
            output += "\n"
        return output

    def add_semester(self, semester):
        self.semesters.append(semester)

    def validate_schedule(self):
        is_valid = True
        # Look at each semester
        for semester_number, semester in enumerate(self.semesters):
            # Make sure that each semester has no more than 19.5 hours total
            if semester.get_total_hours() > 19.5:
                print(
                    f"Semester {semester_number + 1} has {semester.get_total_hours()} hours. The maximum is 19.5 hours.")
                is_valid = False
                return is_valid

            # For each course in the semester
            for course in semester.get_courses():
                # If the course has prerequisites
                if course.get_prerequisites() is not None:
                    # for each prerequisite in the course
                    for prerequisite in course.get_prerequisites():
                        # Check if the prerequisite is one course or has options
                        if type(prerequisite) == list:
                            # If the course has options
                            previous_taken_courses = []
                            for previous_semester in self.semesters[:semester_number]:
                                # add courses from previous semesters to list
                                previous_taken_courses += previous_semester.get_courses()
                            # If none of the items in the prerequisite list are in the previous taken courses
                            if not any(item in previous_taken_courses for item in prerequisite):
                                is_valid = False
                                print(
                                    f"{course.get_name()} is not valid. You have not taken any of the following prerequisites:")
                                for item in prerequisite:
                                    if type(item) == str:
                                        print(f"\t{item}")
                                    else:
                                        print(f"\t{item.get_name()}")
                                return is_valid
                        else:
                            # check all previous semesters to find this course
                            previous_taken_courses = []
                            for previous_semester in self.semesters[:semester_number]:
                                # add courses from previous semesters to list
                                previous_taken_courses += previous_semester.get_courses()
                            # if the prerequisite is not in the list of previous taken courses
                            if prerequisite not in previous_taken_courses:
                                is_valid = False
                                if type(prerequisite) == str:
                                    print(f'\t{prerequisite}')
                                else:
                                    print(
                                        f"{prerequisite.get_name()} is a prerequisite of {course.get_name()}")
                                return is_valid
                # If the course has corequisites
                if course.get_corequisites() is not None:
                    # for each corequisite in the course
                    for corequisite in course.get_corequisites():
                        # Check if the corequisite is one course or has options
                        if type(corequisite) == list:
                            # If the course has options
                            previous_taken_courses = []
                            for previous_semester in self.semesters[:semester_number+1]:
                                # add courses from previous semesters to list
                                previous_taken_courses += previous_semester.get_courses()
                            # If none of the items in the corequisite list are in the previous taken courses
                            if not any(item in previous_taken_courses for item in corequisite):
                                is_valid = False
                                print(
                                    f"{course.get_name()} is not valid. You have not taken any of the following corequisites:")
                                for item in corequisite:
                                    print(f"\t{item.get_name()}")
                                return is_valid

                        else:
                            # check all semesters up to the current semester to find this course
                            courses = []
                            for semester in self.semesters[:semester_number+1]:
                                # add courses from previous semesters to list
                                courses += semester.get_courses()
                            # if the corequisite is not in the list of previous taken courses
                            if corequisite not in courses:
                                is_valid = False
                                print(
                                    f"{corequisite.get_name()} is a corequisite of {course.get_name()}")
                                return is_valid
        return True


# Make courses
math111 = Course('Calculus I', 4.0)
math112 = Course('Calculus II', 4.0, [math111])
math213 = Course('Calculus III', 4.0, [math112])
csm101 = Course('Freshman Success Seminar', 0.5)
chgn121 = Course('Chemistry I', 4.0)
csci101 = Course('Introduction to Computer Science', 3.0)
hass100 = Course('Nature and Human Values', 4.0)
pagn_elective = Course('Physical Activity Course', 0.5)
phgn100 = Course('Physics I', 4.5, [math111], [math112])
edns151 = Course('Design 1', 3.0)
csci261 = Course('Programming Concepts', 3.0)
csci303 = Course('Data Science', 3.0, [[csci101, csci261]])
ebgn498 = Course('InnovateX', 3.0)
csci262 = Course('Data Structures', 3.0, [csci261])
ebgn201 = Course('Principles of Economics', 3.0)
csci274 = Course('Introduction to the Linux Operating System', 1.0, [csci261])
hass200 = Course('Global Studies', 3.0, [hass100])
phgn200 = Course('Physics II', 4.5, [phgn100], [math213])
csci250 = Course('Building a Sensor System', 3.0,
                 prerequisites=None, corequisites=[math213, phgn200])
csci306 = Course('Software Engineering', 3.0, [csci262])
csci403 = Course('Database Management', 3.0, [csci262])
math201 = Course('Probability & Statistics', 3.0, [math112])
math225 = Course('Differential Equations', 3.0, [math112], [math213])
csci341 = Course('Computer Organization', 3.0, [csci261], [csci262])
csci358 = Course('Discrete Mathematics', 3.0, [math213])
eeng281 = Course('Intro to Circuits', 3.0, [phgn200])
math307 = Course('Intro to Scientifc Computing', 3.0, [math213], [math225])
math332 = Course('Linear Algebra', 3.0, [math213])
csci404 = Course('Artificial Intelligence', 3.0, [csci262])
csci473 = Course('Human-Centered Robotics', 3.0, [csci262, math201])
eeng282 = Course('Electric Circuits', 4.0, [phgn200])
phgn215 = Course('Analog Electronics', 4.0, [phgn200])
megn441 = Course('Introduction to Robotics', 3.0, [
                 csci261, [eeng281, eeng282, phgn215]])
eeng307 = Course('Introduction to Feedback Control Systems', 3.0, [eeng281])
csci406 = Course('Algorithms', 3.0, [csci262, csci358, math213])
csci370 = Course('Advanced Software Engineering', 4.5, [csci306])
eeng310 = Course('Information Systems Science I', 4.0, [
                 [eeng281, eeng282, phgn200], math225])
eeng311 = Course('Information Systems Science II', 3.0, [eeng310])
csci437 = Course('Introduction to Computer Vision', 3.0, [
                 [math201, eeng311], math332, csci261])
csci470 = Course('Machine Learning', 3.0, [math332, math201])
csci400 = Course('Principles of Programming Languages', 3.0, [csci306])
csci442 = Course('Operating Systems', 3.0, [csci262, csci274, csci341])


# make semesters
semester1 = Semester(
    'Fall 2020', [math111, csm101, edns151, hass100, pagn_elective, csci101])
semester2 = Semester(
    'Spring 2021', [math112, phgn100, csci261, csci303, ebgn498])
semester3 = Semester(
    'Summer 2021', [csci262, ebgn201])
semester4 = Semester(
    'Fall 2021', [chgn121, csci274, hass200, math213, phgn200])
semester5 = Semester(
    'Spring 2022', [csci250, csci306, csci403, math201, math225, pagn_elective])
semester6 = Semester(
    'Fall 2022', [csci341, csci358, eeng281, math307, math332, pagn_elective])
semester7 = Semester(
    'Spring 2023', [csci404, csci473, eeng307, megn441, csci406, pagn_elective])
semester8 = Semester(
    'Summer 2023', [csci370])
semester9 = Semester(
    'Fall 2023', [csci437, csci470, csci400])
semester10 = Semester(
    'Spring 2024', [csci442])

schedule = Schedule([semester1, semester2, semester3, semester4,
                    semester5, semester6, semester7, semester8, semester9, semester10])

print(schedule)

# Test Schedule
if schedule.validate_schedule():
    print("Schedule is valid")
else:
    print("Schedule is invalid")
