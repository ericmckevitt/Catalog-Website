
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
                                print(
                                    f"{prerequisite.get_name()} is a prerequisite of {course.get_name()}")
                                return False
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
                                print(
                                    f"{corequisite.get_name()} is a corequisite of {course.get_name()}")
                                return False
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

# make two semesters
semester1 = Semester(
    'Fall 2020', [math111, csm101, edns151, hass100, pagn_elective])
semester2 = Semester(
    'Spring 2021', [math112, phgn100, csci261, csci303])

schedule = Schedule([semester1, semester2])

print(schedule.validate_schedule())
