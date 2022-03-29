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