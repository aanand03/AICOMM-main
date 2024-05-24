document.querySelector('.red-home').addEventListener('click', () => {
    const name = document.querySelector('.name input').value;
    const password = document.querySelector('.password input').value;
  
    firebase.auth().signInWithEmailAndPassword(name, password)
      .then((userCredential) => {
        // User signed in successfully
        const user = userCredential.user;
        console.log(user);
      })
      .catch((error) => {
        // Handle errors
        const errorCode = error.code;
        const errorMessage = error.message;
        console.error(errorMessage);
      });
  });
  