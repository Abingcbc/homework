# Image Search Engine

#### 1753837 陈柄畅

## Requirements

* Flask
* PyQt5
* Numpy
* Tensorflow
* Flask-HTTPAuth
* MDL ([Material Design Lite](https://github.com/google/material-design-lite))   ***I have uploaded it in folder `mdl`***

## Run

1. Run the rest-server.py
2. Open your browser (`Chrome` recommend) and go to `127.0.0.1:5000`

## Formulation

* Users can drag a picture into the block or simply click the block to upload a picture.

  <img src="./img/input_box.png" height=300px>

  `static/html/main.html line 159`

  ```html
  <form id="img_form" class="subscribe_form" method="post" enctype="multipart/form-data">
  	<div id="drag_area">
  		<div id="query_info">
  			<input id="click_choose" type="file" name="file" 			onchange="clickUpload(event)">
  			<br>
  			<p style="font-size: 20px">Drag picture here <br><br> or click to upload</p>
  		</div>
  		<img id="query_img">
  	</div>
  	<input class="subscribe center" value="Search" type="submit" onclick="fun()">
  </form>
  ```

* After users upload a picture, they can preview the query image in the block.

  <img src="./img/preview.png" height=300px>

  `static/js/main.js line 13`

  ```javascript
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
  ```

## Initiation

* Users can search pictures similar with the uploaded query image by clicking the search button.

  <img src="./img/search_button.png" height=200px>

  ***Detailed code is in `static/html/main.html line 200 fun()`***

* After users upload a picture, they can click the clear button and reupload a new one.

  <img src="./img/clear_button.png" height=300px>

  `static/js/mian.js line 30`

  ```javascript
  function clear_image() {
      //clear query image
      var query_img = document.getElementById("query_img");
      var query_info = document.getElementById("query_info");
      query_img.src = ""
      query_img.style.display = "none"
      query_info.style.display = "inline-block"
      var clear_button = document.getElementById("clear_button");
      clear_button.style.display = "none";
      //clear the result list
      var main = document.getElementById("main");
      var result = document.getElementById("result");
      main.removeChild(result);
      result = document.createElement("div");
      result.setAttribute("id","result");
      result.setAttribute("class","row");
      main.appendChild(result);
      document.getElementById("overview").innerHTML = "";
      //clear form
      document.getElementById("img_form").reset();
  }
  ```

## Review

* Users can overview the total number of results and results' tags.

  <img src="./img/overview.png" height=200px>

  `static/html/main.html line 188`

  ```html
  <div id="main" class="container text-center">
  	<h3 id="overview"></h3>
  	<div id="result" class="mdl-grid portfolio-max-width">
  	</div>
  </div>
  ```

  `static/html/main.html line 281`

  ```javascript
  overview = document.getElementById("overview");
  overview.innerHTML = "Find " + number.toString() + " results<br>";
  for (var i = 0; i < tag.length; i++) {
  	var span = document.createElement("span");
  	span.setAttribute("class", "mdl-chip");
  	var text = document.createElement("span");
  	text.setAttribute("class", "mdl-chip__text");
  	text.innerHTML = tag[i];
  	span.appendChild(text);
  	overview.appendChild(span);
  }
  ```

* Users can view the results in seperate cards. If user hover their cursors on the card, the image will be amplified so that users can see more details.

  <img src="./img/result_show.png" height=300px>

  `static/html/main.html line 246`

  ```javascript
  // add results dynamically
  var result = document.getElementById("result");
  for (var i = 0; i < number; i++) {
  	var div1 = document.createElement("div");
  	div1.setAttribute("class", "mdl-cell mdl-card mdl-shadow--4dp portfolio-card hover_amplify");
  	var div_picture = document.createElement("div");
  	div_picture.setAttribute("class", "mdl-card__media");
  	var image = document.createElement("img");
  	image.src = response['image' + i.toString()];
  	image.setAttribute("class", "article_img");
  	image.setAttribute("border", "0");
  	div_picture.appendChild(image);
      
  	var div_title = document.createElement("div");
  	div_title.setAttribute("class", "mdl-card__title");
  	var title = document.createElement("h2");
  	title.setAttribute("class", "mdl-card__title-text");
  	temp = response['image' + i.toString()].split("\\")
  	title.innerHTML = temp[temp.length - 1]
  	div_title.appendChild(title)
      
  	var div_button = document.createElement("div");
  	div_button.setAttribute("class", "mdl-card__actions mdl-card--border");
  	var button = document.createElement("button")
  	button.setAttribute("class", "favour_bt hover_amplify mdl-button mdl-	button--colored mdl-js-button mdl-js-ripple-effect mdl-button--accent");
  	button.setAttribute("img_name", temp[temp.length - 1]);
  	button.innerHTML = "ADD TO FAVOURITE LIST";
  	div_button.appendChild(button);
      div1.appendChild(div_picture);
  	div1.appendChild(div_title);
  	div1.appendChild(div_button);
  	result.appendChild(div1);
  }
  ```

  

  

  <img src="./img/result_hover.png" height=300px>

  `static/css/styles.css line 91`

  ```css
  img.article-image {
    width: 100%;
    height: auto;
  }
  ```

## Refinement

* Users can restrict the range of images they would like to search by just click the tags they wants. One thing should be mentioned is that if users set no tag, the image search engine will alert users and search with the default tag `all`. 

* When a tag is selected, its icon will turn black and when users' cursors are on the icon, the icon will amplify, which will give users a better experience.

  The layout of  the tags is too long, so you can see the detailed code in `static/html/main.html line 32`

  <img src="./img/tags.png" height=200px>

  The logic behind is in `static/js/main.js line 52`.

  ```javascript
  choose_tag = (id) => {
      var chosed_tag = document.getElementById(id);
      if (chosed_tag.src.indexOf("_") != -1) {
          tag.splice(tag.indexOf(id.substring(5,id.length)),1);
          chosed_tag.src = chosed_tag.src.substring(0,chosed_tag.src.length-6)+".png";
      } else {
          tag.push(id.substring(5,id.length));
          chosed_tag.src = chosed_tag.src.substring(0,chosed_tag.src.length-4)+"_c.png";
      }
      if (id != "icon_all") {
          var tag_all = document.getElementById("icon_all");
          if (tag_all.src.indexOf("_") != -1) {
              tag_all.src = tag_all.src.substring(0,tag_all.src.length-6)+".png";
              tag.splice(tag.indexOf("all"),1);
          }
      } else {
          for (var i = 1; i < tag_list.length; i++) {
              var cur_tag = document.getElementById("icon_"+tag_list[i]);
              if (cur_tag.src.indexOf("_") != -1) {
                  tag.splice(tag.indexOf(tag_list[i]),1);
                  cur_tag.src = cur_tag.src.substring(0,cur_tag.src.length-6)+".png";
              }
          }
      }
      console.log(tag);
  }
  ```

* User can choose the total number of results. The default number is 9.

  `static/html/main.html line 171`

  ```html
  <select id="max_count" class="custom-select" style="margin-top: 20px">
  	<option value="0">Choose max count of results</option>
  	<option value="1">1</option>
  	<option value="2">2</option>
  	<option value="3">3</option>
  	<option value="4">4</option>
  	<option value="5">5</option>
  	<option value="6">6</option>
  	<option value="7">7</option>
  	<option value="8">8</option>
  	<option value="9" selected="selected">9</option>
  	<option value="10">10</option>
  	<option value="11">11</option>
  	<option value="12">12</option>
  </select>
  ```

As shown above, the original route cannot support such function. So I modified the request route. I add two new segments in the route `<tag>` and `<int:number>`, which represent the tags and number of results. Correspondingly, I add screening part in `get_top_k_similar`.

`rest-server.py line 54`

```python
@app.route('/imgUpload/<tag>/<int:number>', methods=['GET', 'POST'])
def upload_img(tag, number):
    print(tag)
    print(number)
    print("image upload")
    tag_list = tag.split("_")
    result = 'static/result'
    if not gfile.Exists(result):
          os.mkdir(result)
    shutil.rmtree(result)
 
    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
           
            print('No selected file')
            return redirect(request.url)
        if file:# and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features,tag_list)
            os.remove(inputloc)
            image_path = "/result"
            image_list =[os.path.join(image_path, file) for file in os.listdir(result)
                              if not file.startswith('.')]
            images = {}
            for i in range(len(image_list)):
                images['image'+str(i)] = image_list[i]
            return jsonify(images)
```

`search.py  line 44`

```python
        sorted_list =  np.argsort([cosine(image_data, pred_row) \
                            for ith_row, pred_row in enumerate(pred)])
        top_k_ind = []
        print(tag_list)
        if "all" in tag_list:
            top_k_ind = sorted_list[:k]
        else:
            suit_img = []
            for tag in tag_list:
                with open("./database/tags/"+tag+".txt") as file:
                    for line in file:
                        suit_img.append(eval(line))
            suit_img = set(suit_img)
            for ind in sorted_list:
                img_name = pred_final[ind]
                num = eval(img_name[img_name.find("m")+1:-4])
                if num in suit_img:
                    top_k_ind.append(ind)
                    if len(top_k_ind) == k:
                        break
        print(top_k_ind)
        
        for i, neighbor in enumerate(top_k_ind):
            image = ndimage.imread(pred_final[neighbor])
            #timestr = datetime.now().strftime("%Y%m%d%H%M%S")
            #name= timestr+"."+str(i)
            name = pred_final[neighbor]
            tokens = name.split("\\")
            img_name = tokens[-1]
            print(img_name)
            name = 'static/result/'+img_name
            imsave(name, image)
```

## Use

* Users can add selected image into a favourite list by clicking the button under the image. Users can view pictures added in `static/favourite` folder. If it is successful, there will be a snackbar at the bottom to tell users. And if it fails, another snackbar at the bottom will alert users.

  <img src="./img/favour_button.png" height=400px>

  `static/html/main.html line 291`	*frontend code*

  ```javascript
  var add_favour = document.querySelectorAll(".favour_bt");
  var snack_bar = document.querySelector("#add_favour_snack");
  var imgs = document.querySelectorAll(".article_img");
  for (var i = 0; i < add_favour.length; i++) {
  	add_favour[i].addEventListener('click', function () {
  		var post_url = "favour/" + this.getAttribute("img_name");
  		$.ajax({
  			url: post_url,
  			type: 'POST',
  			success: function (response) {
  				window['counter'] = 0
  				if (response['success']) {
  					var data = { message: "Successful to add favouraite list! You can view it in 'favourite' folder." };
  					snack_bar.MaterialSnackbar.showSnackbar(data);
  				} else {
  					var data = { message: "Oops! It failed. Please try again."};
  					snack_bar.MaterialSnackbar.showSnackbar(data);
  				}
  			}
  		})
  	})
  };
  ```

  `rest-server.py line 38`	*backend code*

  ```python
  @app.route("/favour/<file_name>", methods=['POST'])
  def add_favour(file_name):
      if os.path.exists("./static/result/"+file_name):
          print("./static/result/"+file_name)				                             shutil.copy("./static/result/"+file_name,                                                "./static/favourite/"+file_name)
          res = {'success': True}
          return jsonify(res)
      else:
          res = {'success': False}
          return jsonify(res)
  ```

## The Requirements of an Image Search Task

I think that an image search task should let users find what they want. This is the most important requirement. The task should also guide user to use the search service without any complex operations. After user get the result, the task should also let users make use of the result, such as sharing to social medias, which may be what users really want to do.

## ATTENTION

I use `_` to decide whether a tag is chosen and original codes use `\\` in the path. If there is `_` in the path or you don't run it on `Windows` platform without any modification, it may not work well.



