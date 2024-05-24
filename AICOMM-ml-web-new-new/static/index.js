
function displayMessage(message, isError = false) {
    const messageElement = document.getElementById('message');
    messageElement.textContent = message;
    messageElement.style.color = isError ? 'red' : 'green';
}


let users = JSON.parse(localStorage.getItem('users')) || [];

function saveUsersToStorage() {
    localStorage.setItem('users', JSON.stringify(users));
}

function registerUser() {
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;

    if (users.some(user => user.username === username)) {
        displayMessage('Username already taken. Please choose another username.', true);
        return;
    }

    users.push({ username, password });
    saveUsersToStorage();
    displayMessage('Registration successful. You can now log in.', false);
}


function loginUser() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    const user = users.find(user => user.username === username && user.password === password);

    if (user) {
        displayMessage('Login successful!', false);
        
        setTimeout(function() {
            window.location.href = 'index.html'; 
        }, 2000); 
    } else {
        displayMessage('Invalid username or password. Please try again.', true);
    }
}
