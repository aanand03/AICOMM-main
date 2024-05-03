document.querySelector('.btn-main').addEventListener('click', () => {
    const emailValue = document.querySelector('#em').value;
    const password = document.querySelector('#pas').value;

    firebase.auth().createUserWithEmailAndPassword(emailValue, password)
      .then((userCredential) => {
        // User signed up successfully
        const user = userCredential.user;
        console.log(user);

        // Update the DOM to show success message
        showMessage('Signup successful!');
      })
      .catch((error) => {
        // Handle errors
        const errorCode = error.code;
        const errorMessage = error.message;
        console.error(errorMessage);
        showMessage(`Signup failed: ${errorMessage}`);
      });
      function showMessage(message) {
        const messageElement = document.getElementById('message');
        messageElement.innerHTML = `<h1>${message}</h1>`;
      }
  });
  