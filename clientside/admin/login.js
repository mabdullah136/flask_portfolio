// login.js
const baseUrl = 'http://127.0.0.1:5000'
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    event.preventDefault();
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    // Perform login through API
    var url = "http://127.0.0.1:5000/login";
    var data = {
        email: email,
        password: password
    };
    console.log(data);
    // Make a POST request to the API
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        console.log(response);
        if (response.status === 200) {
            alert("Login successful!");
            localStorage.setItem('isLoggedIn', true);
            window.location.href = "/clientside/admin/users.html";

        } else {
            alert("Invalid username or password");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
