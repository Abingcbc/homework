var domain = "http://abingcbc.cn:10010";

login = () => {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', domain+"/login", true);
    var jsonString = JSON.stringify({
        username: username,
        password: password
    });
    xhr.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.onreadystatechange = () => {
        // 请求已完成，且响应已就绪
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                localStorage.setItem("username", username);
                window.location.href = "/";
            } else {
                alert("用户名或密码错误！");
            }
        }
    }
    xhr.send(jsonString);
}


register = () => {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var passwordValid = document.getElementById("passwordValid").value;
    if (password !== passwordValid) {
        alert("两次输入密码不一致！");
        return;
    }
    var xhr = new XMLHttpRequest();
    xhr.open('POST', domain+"/register", true);
    var jsonString = JSON.stringify({
        username: username,
        password: password
    });
    xhr.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.onreadystatechange = () => {
        // 请求已完成，且响应已就绪
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                window.location.href = "/login";
            } else {
                alert("用户名已被使用！");
            }
        }
    }
    xhr.send(jsonString);
}