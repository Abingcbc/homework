var domain = "http://abingcbc.cn:10010";

window.onload = () => {
    displayNav();
    var xhr = new XMLHttpRequest();
    var reg = new RegExp('[?&]productId=([^&#]+)');
    var productId = window.location.href.match(reg);
    if (productId) {
        productId = parseInt(productId[1]);
    } else {
        window.location.href = "/";
        return;
    }
    xhr.open("GET", domain + "/detail?productId=" + productId, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4) {
            var productDetail = JSON.parse(xhr.responseText);
            var infoContainer = document.getElementById("infoContainer");
            if (productDetail != null) {
                infoContainer.innerHTML = "";
                infoContainer.innerHTML = '\
                    <p class="productId" id="productId">' + productDetail.productId + '</p>\
                    <div class="productDetailSide">\
                        <div class="productDetailImg">\
                            <img src="' + productDetail.imageUrl + '" alt="" />\
                        </div>\
                    </div>\
                    <div class="productDetailInfo">\
                        <div class="productDetailTitle">\
                            <p><span class="productDetailSlogan">百亿补贴</span>' + productDetail.name + '</p>\
                        </div>\
                        <div class="productDetailPriceContainer">\
                            <div class="productDetailPrice-row">\
                                <p><span class="productDetailPriceType">优惠价</span>\
                                    <span class="productDetailPrice">￥' + productDetail.newPrice + '</span>\
                                </p>\
                            </div>\
                            <div class="productDetailPrice-row">\
                                <p><span class="productDetailPriceType">原价</span>\
                                    <del>￥' + productDetail.originalPrice + '</del>\
                                </p>\
                            </div>\
                        </div>\
                        <div class="addCartButton">\
                            <button class="shoppingButton" onclick="addCart()">加入购物车</button>\
                            <button class="shoppingButton" onclick="buy()">直接购买</button>\
                        </div>\
                    </div>';
            }
            var detailImageContainer = document.getElementById("detailImageContainer");
            detailImageContainer.innerHTML = "";
            var urlList = productDetail.detailUrls.split("|");
            for (var i = 0; i < urlList.length; i++) {
                detailImageContainer.innerHTML += '<img src="' + urlList[i] + '" alt=""/>';
            }
        }
    }
    xhr.send();
}

addCart = () => {
    var username = localStorage.getItem("username");
    if (username == null) {
        window.location.href = "/login";
        return
    }
    var productId = parseInt(document.getElementsByClassName("productId")[0].innerHTML);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', domain+"/add", true);
    var jsonString = JSON.stringify({
        username: username,
        productId: productId,
        number: 1
    });
    xhr.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.onreadystatechange = () => {
        // 请求已完成，且响应已就绪
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                alert("添加购物车成功！");
            } else {
                alert("添加购物车失败！");
            }
        }
    }
    xhr.send(jsonString);
}

buy = () => {
    if (!checkLogin()) {
        window.location.href = "/login";
        return;
    }
    var productId = parseInt(document.getElementById("productId").innerHTML);
    var cartItem = JSON.stringify({
        username: localStorage.getItem("username"),
        productId: productId,
        // -1 代表直接购买
        number: -1
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