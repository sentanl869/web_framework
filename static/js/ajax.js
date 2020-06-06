let ajax = function (method, path, data, token, responseCallback) {
    let r = new XMLHttpRequest();
    r.open(method, path, true);
    r.setRequestHeader('Content-Type', 'application/json');
    r.setRequestHeader('X-CSRF-TOKEN', token)
    r.onreadystatechange = function () {
        if (r.readyState === 4) {
            let json = JSON.parse(r.response);
            responseCallback(json);
        }
    };
    data = JSON.stringify(data);
    r.send(data);
};