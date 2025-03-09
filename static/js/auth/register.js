function flushResponse() {
  document.getElementById("alert-response"  ).style.display = 'none';
  document.getElementById("resend-div"      ).style.display = 'none';
  document.getElementById("alert-response"  ).classList.remove('alert-success'  );
  document.getElementById("alert-response"  ).classList.remove('alert-danger'   );
  document.getElementById("alert-response"  ).classList.remove('alert-primary'  );
}

function loadingResponse() {
  flushResponse();
  document.getElementById("alert-status"  ).innerHTML = "Loading...";
  document.getElementById("alert-desc"    ).innerHTML = "Please wait...";
  document.getElementById("alert-response").classList.add('alert-primary');
  document.getElementById("alert-response").style.display = 'block';
}

function responseAlert(response) {
  flushResponse();
  const obj = JSON.parse(response);
  if (obj.status == "success" ) document.getElementById("alert-response").classList.add('alert-success' );
  if (obj.status == "failed"  ) document.getElementById("alert-response").classList.add('alert-danger'  );
  if (obj.desc == "check email for verification") {
    document.getElementById("resend-email"    ).value     = document.getElementById("form-email").value;
    document.getElementById("resend-message"  ).innerHTML = obj.data.message;
    document.getElementById("resend-link"     ).setAttribute('href', obj.data.resend);
    document.getElementById("resend-div"      ).style.display = 'block';
  }
  document.getElementById("alert-status"  ).innerHTML     = obj.status;
  document.getElementById("alert-desc"    ).innerHTML     = obj.desc;
  document.getElementById("alert-response").style.display = 'block';
}

function onSubmit(token) {
  loadingResponse();
  var email     = document.getElementById("form-email"    ).value;
  var username  = document.getElementById("form-username" ).value;
  var password  = document.getElementById("form-password" ).value;
  var roles     = document.getElementById("roles"         ).value;
  var url       = "/api/auth/register/"+roles;
  var payload   = {
    "email"     : email,
    "username"  : username,
    "password"  : password
  };
  payload.captcha = token; // Add response from reCAPTCHA
  sendHttpRequest(url, "POST", payload, function (error, response) {
    if (error) console.error("Error:", error);
    else {
      console.log("JSON Response:", response);
      responseAlert(response);
    }
  }, "application/json");
}

function resending() {
  loadingResponse();
  var email     = document.getElementById("resend-email").value;
  var url       = "/api/auth/resend?email="+email;
  sendHttpRequest(url, "GET", null, function (error, response) {
    if (error) console.error("Error:", error);
    else {
      console.log("JSON Response:", response);
      responseAlert(response);
    }
  }, "multipart/form-data");
}

flushResponse();
