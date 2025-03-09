function flushResponse() {
  document.getElementById("alert-response"  ).style.display = 'none';
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

function responseSession(response) {
  flushResponse();
  const obj = JSON.parse(response);
  document.getElementById("alert-status").innerHTML = obj.status;
  if (obj.status == "success") {
    document.getElementById("alert-desc"    ).innerHTML = "Welcome!";
    document.getElementById("alert-response").classList.add('alert-success');
    document.getElementById("alert-response").style.display = 'block';
    window.location.replace("/?msg=Welcome");
  }
  else {
    document.getElementById("alert-desc"    ).innerHTML = "Internal error";
    document.getElementById("alert-response").classList.add('alert-danger');
    document.getElementById("alert-response").style.display = 'block';
  }
}

function setSession(jwt) {
  var url     = "/api/auth/session/set";
  var payload = {
    "jwt" : jwt
  };
  sendHttpRequest(url, "POST", payload, function (error, response) {
    if (error) console.error("Error:", error);
    else {
      console.log("JSON Response:", response);
      responseSession(response);
    }
  }, "application/json");
}

function responseAlert(response) {
  flushResponse();
  const obj = JSON.parse(response);
  if (obj.status == "success") {
    loadingResponse();
    document.getElementById("alert-desc"    ).innerHTML = "Set the session";
    setSession(obj.data.jwt);
  }
  if (obj.status == "failed") {
    document.getElementById("alert-response").classList.add('alert-danger');
    document.getElementById("alert-status"  ).innerHTML = obj.status;
    document.getElementById("alert-desc"    ).innerHTML = obj.desc;
    document.getElementById("alert-response").style.display = 'block';
  }
}

function onSubmit() {
  loadingResponse();
  var username    = document.getElementById("form-username").value;
  var password    = document.getElementById("form-password").value;

  var url     = "/api/auth/login";
  var payload = {
    "username" : username,
    "password" : password
  };
  sendHttpRequest(url, "POST", payload, function (error, response) {
    if (error) console.error("Error:", error);
    else {
      console.log("JSON Response:", response);
      responseAlert(response);
    }
  }, "application/json");

}

flushResponse();
