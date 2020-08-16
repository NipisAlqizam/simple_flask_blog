function validatePassword() {
  let pass1 = document.forms["register"]["password"].value;
  let pass2 = document.forms["register"]["repeat_password"];
  if (pass1 != pass2.value) {
    document.forms["register"]["password"].className = "incorrect_password";
    document.forms["register"]["repeat_password"].className = "incorrect_password";
    return false;
  }
}
