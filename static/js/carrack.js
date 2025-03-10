function sendHttpRequest(url, method, data, callback, contentType = "multipart/form-data", authorization = "") {
  var xhr = new XMLHttpRequest();
  xhr.open(method, url, true);
  xhr.setRequestHeader("Content-Type", contentType);
  xhr.setRequestHeader("Authorization", authorization);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        var response = xhr.responseText;
        callback(null, response);
      }
      else callback(xhr.status, null);
    }
  };
  var requestData;
  if (contentType === "application/json") requestData = JSON.stringify(data);
  else requestData = data;
  xhr.send(requestData);
}
