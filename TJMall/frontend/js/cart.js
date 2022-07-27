var domain = "http://abingcbc.cn:10010";

window.onload = () => {
    displayNav();
    var xhr = new XMLHttpRequest();
    var username = localStorage.getItem("username");
    if (username == null) {
        window.location.href = "/login";
        return;
    }
    xhr.open("GET", domain + "/cart?username=" + username, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4) {
            var cartItemList = JSON.parse(xhr.responseText);
            var cartItemContainer = document.getElementById("cartItemContainer");
            cartItemContainer.innerHTML = "";
            for (var i = 0; i < cartItemList.length; i++) {
                cartItemContainer.innerHTML += '\
                <div class="cartItem">\
                    <div class="cartItemImg" onclick="gotoDetail()">\
                        <p class="productId">' + cartItemList[i].productId + '</p>\
                        <img src="' + cartItemList[i].imageUrl + '">\
                    </div>\
                    <div class="cartItemInfo">\
                        <p>' + cartItemList[i].name + '</p>\
                        <p><span class="cartItemPrice">' + cartItemList[i].newPrice + '</span></p>\
                    </div>\
                    <div class="cartItemControl">\
                        <p class="cartItemNum">' + cartItemList[i].number + '</p>\
                        <div class="cartButton" onclick="remove(this)">\
                            —\
                            <p class="productId">' + cartItemList[i].productId + '</p>\
                        </div>\
                        <div class="cartButton" onclick="buy(this)">\
                            结算\
                            <p class="productId">' + cartItemList[i].productId + '</p>\
                        </div>\
                    </div>\
                </div>';
            }
            if (cartItemList.length == 0) {
                cartItemContainer.innerHTML = '购物车中暂无商品，快去选购吧~';
            }
        }
    }
    xhr.send();
}

remove = (element) => {
    var productId = parseInt(element.getElementsByClassName("productId")[0].innerHTML);
    var cartItem = JSON.stringify({
        username: localStorage.getItem("username"),
        productId: productId
    })
    var xhr = new XMLHttpRequest();
    xhr.open('POST', domain+"/remove", true);
    xhr.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.onreadystatechange = () => {
        // 请求已完成，且响应已就绪
        if (xhr.readyState === 4) {
            window.location.href = '/cart';
        }
    }
    xhr.send(cartItem);
}

buy = (element) => {
    var productId = parseInt(element.getElementsByClassName("productId")[0].innerHTML);
    var cartItemNum = parseInt(element.parentElement.getElementsByClassName("cartItemNum")[0].innerHTML);
    var cartItem = JSON.stringify({
        username: localStorage.getItem("username"),
        productId: productId,
        number: cartItemNum
    })
    var xhr = new XMLHttpRequest();
    // 添加order时会自动完成购买操作，并删除购物车中的商品
    xhr.open('POST', domain+"/order", true);
    xhr.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.onreadystatechange = () => {
        // 请求已完成，且响应已就绪
        if (xhr.readyState === 4) {
            alert("购买商品成功！")
            window.location.href = '/order';
        }
    }
    xhr.send(cartItem);
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