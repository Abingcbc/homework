var domain = "http://abingcbc.cn:10010";

window.onload = () => {
    displayNav();
    var xhr = new XMLHttpRequest();
    var username = localStorage.getItem("username");
    if (username == null) {
        window.location.href = "/login";
        return;
    }
    xhr.open("GET", domain + "/order?username=" + username, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4) {
            var orderItemList = JSON.parse(xhr.responseText);
            var orderItemContainer = document.getElementById("orderItemContainer");
            orderItemContainer.innerHTML = "";
            for (var i = 0; i < orderItemList.length; i++) {
                orderItemContainer.innerHTML += '\
                <div class="orderItem">\
                    <div class="orderItemImg" onclick="gotoDetail(this)">\
                        <p class="productId">' + orderItemList[i].productId + '</p>\
                        <img src="' + orderItemList[i].imageUrl + '">\
                    </div>\
                    <div class="orderItemInfo">\
                        <p>' + orderItemList[i].name + '</p>\
                        <p><span class="orderItemPrice">' + orderItemList[i].newPrice + ' * ' + orderItemList[i].number + '</span></p>\
                    </div>\
                    <div class="orderItemControl">\
                        <p class="orderItemTime">' + orderItemList[i].createTime + '</p>\
                    </div>\
                </div>';
            }
            if (orderItemList.length == 0) {
                orderItemContainer.innerHTML = '暂无商品，快去选购吧~';
            }
        }
    }
    xhr.send();
}

var gotoDetail = (product) => {
    var productId = product.getElementsByClassName("productId")[0].innerHTML;
    window.location.href = "/detail?productId="+productId;
}

checkLogin = () => {
    if (localStorage.getItem("username") != null) {
        return true;
    } else {
        return false;
    }
}

displayNav = () => {
    if (checkLogin()) {
        document.getElementsByClassName("login")[0].setAttribute("style", "display: none");
        document.getElementsByClassName("logined")[0].innerHTML = 
            "您好，" + localStorage.getItem("username") + 
            document.getElementsByClassName("logined")[0].innerHTML;
    } else {
        document.getElementsByClassName("logined")[0].setAttribute("style", "display: none");
    }
}

logout = () => {
    localStorage.removeItem("username");
    window.location.href = "/";
}