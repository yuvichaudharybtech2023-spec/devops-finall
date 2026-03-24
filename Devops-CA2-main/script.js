// script.js - Client-Side Form Validation

function validateForm() {
    let isValid = true;
    
    // Clear all previous errors
    clearErrors();

    // 1. Validate Student Name (not empty)
    const name = document.getElementById('studentName').value.trim();
    if (name === "") {
        showError('nameError', 'Student Name is required.');
        isValid = false;
    }

    // 2. Validate Email (proper format)
    const email = document.getElementById('email').value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email === "") {
        showError('emailError', 'Email ID is required.');
        isValid = false;
    } else if (!emailRegex.test(email)) {
        showError('emailError', 'Please enter a valid email format.');
        isValid = false;
    }

    // 3. Validate Mobile Number (valid digits only, assumption: 10 digits as standard)
    const mobile = document.getElementById('mobile').value.trim();
    const mobileRegex = /^[0-9]{10}$/; // exactly 10 digits
    if (mobile === "") {
        showError('mobileError', 'Mobile Number is required.');
        isValid = false;
    } else if (!mobileRegex.test(mobile)) {
        showError('mobileError', 'Mobile should contain exactly 10 valid digits.');
        isValid = false;
    }

    // 4. Validate Department (should be selected)
    const department = document.getElementById('department').value;
    if (department === "") {
        showError('departmentError', 'Please select a department.');
        isValid = false;
    }

    // 5. Validate Gender (at least one option selected)
    const genderMale = document.getElementById('genderMale').checked;
    const genderFemale = document.getElementById('genderFemale').checked;
    const genderOther = document.getElementById('genderOther').checked;
    if (!genderMale && !genderFemale && !genderOther) {
        showError('genderError', 'Please select your gender.');
        isValid = false;
    }

    // 6. Validate Feedback Comments (not blank and min 10 words)
    const comments = document.getElementById('comments').value.trim();
    if (comments === "") {
        showError('commentsError', 'Feedback comments cannot be blank.');
        isValid = false;
    } else {
        // Count words separated by spaces or newlines
        const wordCount = comments.split(/\s+/).filter(word => word.length > 0).length;
        if (wordCount < 10) {
            showError('commentsError', `Feedback must be at least 10 words. (Currently ${wordCount})`);
            isValid = false;
        }
    }

    // If valid, show success message and optionally prevent actual submission for testing
    if (isValid) {
        document.getElementById('successMessage').style.display = 'block';
        return false; // Prevent traditional form submission to see the success message in tests
    }

    return false; // Always prevent submission if invalid
}

function showError(elementId, message) {
    document.getElementById(elementId).innerText = message;
}

function clearErrors() {
    const errorElements = document.getElementsByClassName('error');
    for (let i = 0; i < errorElements.length; i++) {
        errorElements[i].innerText = '';
    }
    document.getElementById('successMessage').style.display = 'none';
}
