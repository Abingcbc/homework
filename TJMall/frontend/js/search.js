var domain = "http://abingcbc.cn:10010";

var gotoDetail = (product) => {
    var productId = product.getElementsByClassName("productId")[0].innerHTML;
    window.location.href = "/detail?productId="+productId;
}

window.onload = () => {
    displayNav();
    var xhr = new XMLHttpRequest();
    var reg = new RegExp('[?&]keyword=([^&#]+)');
    var keyword = window.location.href.match(reg);
    if (keyword) {
        keyword = keyword[1];
    } else {
        window.location.href = "/";
        return;
    }
    document.getElementById("keyword").value = decodeURIComponent(keyword);
    xhr.open("GET", domain + "/search?keyword="+keyword, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4) {
            var productContainer = document.getElementById("productContainer");
            var productList = JSON.parse(xhr.responseText);
            productContainer.innerHTML = "";
            for (var i = 0; i < productList.length; i++) {
                productContainer.innerHTML += '\
                    <div class="productOverviewItem" onclick="gotoDetail(this)">\
                        <div class="productOverviewImg">\
                            <p class="productId">' + productList[i].productId + '</p>\
                            <img src="' + productList[i].imageUrl + '">\
                        </div>\
                        <div class="productOverviewProductInfo">\
                            <p>' + productList[i].name + '</p>\
                            <p><span class="productOverviewPrice text-danger">' + productList[i].newPrice + '</span>\
                                <del>' + productList[i].originalPrice + '</del>\
                            </p>\
                        </div>\
                    </div>';
            }
            if (productList.length == 0) {
                productContainer.innerHTML = "暂无包含该关键词的商品";
            }
        }
    }
    xhr.send();
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

search = () => {
    window.location.href = "/search?keyword=" + document.getElementById("keyword").value;
}