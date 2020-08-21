window.onload = function () {
  let repeat = document.forms["register"]["repeat_password"];
  console.log(repeat);
  repeat.addEventListener('input', validatePassword);
  let login = document.forms["register"]["login"];
  login.addEventListener('input', validateUsername);
}
function validatePassword() {
  let pass1 = document.forms["register"]["password"].value;
  let pass2 = document.forms["register"]["repeat_password"];
  if (pass1 != pass2.value) {
    document.forms["register"]["password"].className = "incorrect_password";
    document.forms["register"]["repeat_password"].className = "incorrect_password";
    return false;
  } else {
    document.forms["register"]["password"].className = "";
    document.forms["register"]["repeat_password"].className = "";
  }
}

function validateUsername() {
  let xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = () => {
    if (xmlhttp.status == 200 && xmlhttp.readyState == 4) {
      try {
        let data = JSON.parse(xmlhttp.responseText);
        if (data['exists']) {
          document.forms["register"]["login"].className = "incorrect_login";
        } else {
          document.forms["register"]["login"].className = "";
        }
      } catch(e) {
        console.log(e);
        return;
      }
    }
    
  };
  xmlhttp.open("GET", "/api/user_exists?username="+document.forms["register"]["login"].value, true);
  xmlhttp.send();
}