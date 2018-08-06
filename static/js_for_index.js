//handle the data in discuss area
function senddata() {
  let data = document.querySelector("textarea").value;
  if (data !== "") {
    fetch("/handledata", {
      method: "POST",
      credentials: "include",
      body: data
    }).then(() => {
      window.location.href = "/home";
    });
  }
}

function clearinput() {
  document.querySelector("textarea").value = "";
}

document
  .querySelector("input[name='publish']")
  .addEventListener("click", senddata);
document
  .querySelector("input[name='cancel']")
  .addEventListener("click", clearinput);

//column change function
let main = document.querySelector(".home");
let discuss = document.querySelector(".discuss");
let drawing = document.querySelector(".drawing");
let talking = document.querySelector(".talking");
let myplace = document.querySelector(".myplace");
for (let i = 1; i < 6; i++) {
  let button = document.querySelector(".maincolumns li:nth-child(" + i + ")");
  button.addEventListener("click", function() {
    document.querySelector(".jsselected").classList.remove("jsselected");
    let shown = document.querySelector(".page:nth-child(" + i + ")");
    this.classList.add("jsselected");
    document.querySelector(".shown").classList.remove("shown");
    shown.classList.add("shown");
  });
}

//generate the content of home page

function request_discuss() {
  fetch("/discussdata/newest", {
    method: "GET",
    credentials: "include",
    headers: { Accept: "application/json", "Content-Type": "application/json" }
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      let num = 0;
      let container = document.querySelector(".discusspart .list");
      while (data[num]) {
        container.appendChild(generate_items_in_discuss(data[num]));
        num++;
      }
    });
}

function generate_items_in_discuss(data) {
  var el = document.createElement("div");
  var src = "/avatar/" + data[1] + "/80?height=80";
  //'{{ url_for("avatar",text = ' + data[1] + ", height=80, width=80)}}";
  el.innerHTML =
    '<div class="discuss_item"><img src="' +
    src +
    '"><div class="discuss_content"><p class="">' +
    data[0] +
    '</div><div class="discuss_item_detail"><span>已有' +
    data[3] +
    "人插嘴</span><br><span>" +
    data[2] +
    "</span></div></div>";
  console.log(el);
  return el;
}
