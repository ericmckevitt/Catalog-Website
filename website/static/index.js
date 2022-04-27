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

// implement deleteSemester function
function deleteSemester(semester_id) {
    fetch('/delete-semester', {
        method: 'POST',
        body: JSON.stringify({ semester_id: semester_id })
    }).then((_res) => {
        // Refresh page by redirecting to same page
        window.location.href = "/";
    })
}

// implement addSemester function
function addSemester(semester) {
    fetch('/add-semester', {
        method: 'POST',
        body: JSON.stringify({})
    }).then((_res) => {
        // Refresh page by redirecting to same page
        window.location.href = "/";
    })
}