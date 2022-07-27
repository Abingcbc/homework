tag = ["all"];
number = 9;
tag_list = ["all","animals","baby","bird","car","cloud","female","flower","food","indoor","lake","male",
            "night","people","plant","portrait","river","sea","sky","structure","sunset","transport","tree","water"];

function myFunction(){
    document.getElementById("predictedResult").innerHTML= "";
    $('#clear').hide();
}

window.onload = () => {
    var drag_area = document.getElementById("drag_area");
    drag_area.ondragover = (ev) => {
        ev.preventDefault();
    }
    drag_area.ondrop = (ev) => {
        ev.preventDefault();
        var files = ev.dataTransfer.files;
        var reader = new FileReader();
        if(files[0].type.indexOf('image')!=-1){
            reader.readAsDataURL(files[0]);
            var query_img = document.getElementById("query_img");
            var query_info = document.getElementById("query_info");
            reader.onload = () => {
                query_img.src = reader.result;
                query_info.style.display = "none";
                query_img.style.display = "inline-block";
                var clear_button = document.getElementById("clear_button");
                clear_button.style.display = "inline-block"
            }
        } else {
            alert("Please upload a picture!");
        }
    }
}

function clickUpload(ev) {
    var files = ev.target.files;
    var reader = new FileReader();
    if (files && files.length > 0) {
        reader.readAsDataURL(files[0]);
        var query_img = document.getElementById("query_img");
        var query_info = document.getElementById("query_info");
        reader.onload = () => {
            query_img.src = reader.result;
            query_info.style.display = "none";
            query_img.style.display = "inline-block";
            var clear_button = document.getElementById("clear_button");
            clear_button.style.display = "inline-block"
        }
    }
}

function clear_image() {
    var query_img = document.getElementById("query_img");
    var query_info = document.getElementById("query_info");
    query_img.src = ""
    query_img.style.display = "none"
    query_info.style.display = "inline-block"
    var clear_button = document.getElementById("clear_button");
    clear_button.style.display = "none";
}

choose_tag = (id) => {
    var chosed_tag = document.getElementById(id);
    if (chosed_tag.src.indexOf("_") != -1) {
        tag.splice(tag.indexOf(id.substring(5,id.length)),1);
        chosed_tag.src = chosed_tag.src.substring(0,chosed_tag.src.indexOf("_"))+".png";
    } else {
        tag.push(id.substring(5,id.length));
        chosed_tag.src = chosed_tag.src.substring(0,chosed_tag.src.indexOf("."))+"_c.png";
    }
    if (id != "icon_all") {
        var tag_all = document.getElementById("icon_all");
        if (tag_all.src.indexOf("_") != -1) {
            tag_all.src = tag_all.src.substring(0,tag_all.src.indexOf("_"))+".png";
            tag.splice(0,1);
        }
    } else {
        for (var i = 1; i < tag_list.length; i++) {
            var cur_tag = document.getElementById("icon_"+tag_list[i]);
            if (cur_tag.src.indexOf("_") != -1) {
                tag.splice(tag.indexOf(tag_list[i]),1);
                cur_tag.src = cur_tag.src.substring(0,cur_tag.src.indexOf("_"))+".png";
            }
        }
    }
    console.log(tag);
}