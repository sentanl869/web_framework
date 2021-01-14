let ajax = function (method, path, data, token, responseCallback) {
    let request = new XMLHttpRequest();
    request.open(method, path, true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('X-CSRF-TOKEN', token);
    request.onreadystatechange = function () {
        if (request.readyState === 4) {
            let json = JSON.parse(request.response);
            responseCallback(json);
        }
    };
    data = JSON.stringify(data);
    request.send(data);
};