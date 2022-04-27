/**
 * 
 * @param {*} couresId 
 * 
 * Description: 
 * 
 * This function takes in the ID of a course
 * to be deleted, sends a POST request to an
 * endpoint called /delete-course, and reloads
 * the page. 
 */
function deleteCourse(courseId) {
    fetch('/delete-course', {
        method: 'POST',
        body: JSON.stringify({ courseId: courseId })
    }).then((_res) => {
        // Refresh page by redirecting to same page
        window.location.href = "/account";
    })
}

function deleteCourseFromSemester(course_id, semester_id) {
    console.log(course_id, semester_id);
    fetch('/delete-course-from-semester', {
        method: 'POST',
        body: JSON.stringify({ course_id: course_id, semester_id: semester_id })
    }).then((_res) => {
        // Refresh page by redirecting to same page
        window.location.href = "/";
    })
}

/**
 * 
 * @param {*} major 
 * 
 * Description: 
 * 
 * This function takes in a major to be 
 * deleted, sends a POST request to an
 * endpoint called /delete-major, and 
 * reloads the page. 
 */
function deleteMajor(major) {
    fetch('/delete-major', {
        method: 'POST',
        body: JSON.stringify({})
    }).then((_res) => {
        // Refresh page by redirecting to same page
        window.location.href = "/account";
    })
}

// deletes a specific semester from the home page
function deleteSemester(semester_id) {
    fetch('/delete-semester', {
        method: 'POST',
        body: JSON.stringify({ semester_id: semester_id })
    }).then((_res) => {
        // Refresh page by redirecting to same page
        window.location.href = "/";
    })
}

// adds a blank semester to the home page
function addSemester(semester) {
    fetch('/add-semester', {
        method: 'POST',
        body: JSON.stringify({})
    }).then((_res) => {
        // Refresh page by redirecting to same page
        window.location.href = "/";
    })
}

// validates the schedule on the home page
function validateSchedule(userID) {
    console.log("LOG: " + userID);
    fetch('/validate-schedule', {
        method: 'POST',
        body: JSON.stringify({ userID: userID })
    }).then((_res) => {
        // Refresh page by redirecting to same page
        window.location.href = "/";
    })
}