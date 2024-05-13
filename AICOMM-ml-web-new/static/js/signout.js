firebase.auth().signOut().then(() => {
    // User signed out successfully
  }).catch((error) => {
    // Handle errors
    console.error(error.message);
  });
  