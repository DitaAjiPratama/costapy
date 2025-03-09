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

function responseAlert(response) {
  flushResponse();
  const obj = JSON.parse(response);
  if (obj.status == "success" ) {
    document.getElementById("form").style.display = 'none';
    document.getElementById("alert-response").classList.add('alert-success' );
  }
  if (obj.status == "failed"  ) document.getElementById("alert-response").classList.add('alert-danger'  );
  document.getElementById("alert-status"  ).innerHTML     = obj.status;
  document.getElementById("alert-desc"    ).innerHTML     = obj.desc;
  document.getElementById("alert-response").style.display = 'block';
}

function onSubmit() {
  loadingResponse();
  const queryString = window.location.search;
  const urlParams   = new URLSearchParams(queryString);
  const token       = urlParams.get('token')
  var password     = document.getElementById("form-password").value;
  var url     = "/api/auth/reset";
  var payload = {
    "token" : token,
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
