var domain = "http://abingcbc.cn:10010";

var gotoDetail = (product) => {
    var productId = product.getElementsByClassName("productId")[0].innerHTML;
    window.location.href = "/detail?productId=" + productId;
}

window.onload = () => {
    displayNav();
    // 鼠标放置在图片上停止播放
    var container = document.getElementsByClassName("slideContainer")[0];
    container.onmouseenter = function () {
        clearInterval(timer);
    }
    container.onmouseleave = function () {
        autoPlay();
    }
    showCurrentDot();
    var xhr = new XMLHttpRequest();
    xhr.open("GET", domain + "/all", true);
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
        }
    }
    xhr.send();
}

search = () => {
    window.location.href = "/search?keyword=" + document.getElementById("keyword").value;
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

// 轮播图控制
var index = 0;
function nextPic() {
    var slide = document.getElementsByClassName("slide")[0];
    var newLeft;
    if (slide.style.left === "-1600px") {
        newLeft = 0;
    } else {
        newLeft = parseInt(slide.style.left) - 800;
    }
    slide.style.left = newLeft + "px";            
    index++;
    if(index > 2){
        index = 0;
    }
    showCurrentDot();
}
function prevPic() {
    var slide = document.getElementsByClassName("slide")[0];
    var newLeft;
    if (slide.style.left === "0px") {
        newLeft = -1600;
    } else {
        newLeft = parseInt(slide.style.left) + 800;
    }
    slide.style.left = newLeft + "px";            
    index--;
    if(index < 0){
        index = 2;
    }
    showCurrentDot();
}
var timer = null;
function autoPlay() {
    timer = setInterval(function () {
        nextPic();
    }, 2000);
}
autoPlay();

function showCurrentDot() {
    var dots = document.getElementsByClassName("buttons")[0].children;
    for (var i = 0, len = dots.length; i < len; i++) {
        dots[i].setAttribute("style", "");
    }
    dots[index].setAttribute("style", "background-color: red");
}