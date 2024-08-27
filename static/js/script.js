// Smooth scrolling for internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Form validation (example)
document.querySelector('form').addEventListener('submit', function(event) {
    let inputs = document.querySelectorAll('input[required], textarea[required]');
    inputs.forEach(input => {
        if (!input.value.trim()) {
            event.preventDefault();
            alert('Please fill out all required fields.');
        }
    });
});
