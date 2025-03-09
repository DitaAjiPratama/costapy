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
  if (obj.status == "success" ) document.getElementById("alert-response").classList.add('alert-success' );
  if (obj.status == "failed"  ) document.getElementById("alert-response").classList.add('alert-danger'  );
  document.getElementById("alert-status"  ).innerHTML     = obj.status;
  document.getElementById("alert-desc"    ).innerHTML     = obj.desc;
  document.getElementById("alert-response").style.display = 'block';
}

function onSubmit() {
  loadingResponse();
  var email     = document.getElementById("form-email"    ).value;
  var url       = "/api/auth/forgot";
  var payload   = {
    "email"     : email
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
