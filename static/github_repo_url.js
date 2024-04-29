document.addEventListener("DOMContentLoaded", function() {
    // Get the form and input field
    var form = document.querySelector('form');
    var input = document.querySelector('#github_url');
    
    // Add an event listener to the form submit event
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        
        // Get the value of the GitHub repository URL from user input
        var githubUrl = prompt('Please enter your GitHub repository URL:');
        
        // Set the value of the hidden input field to the GitHub repository URL
        input.value = githubUrl;
        
        // Submit the form
        form.submit();
    });
});

