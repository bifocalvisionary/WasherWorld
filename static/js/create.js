const upload = document.getElementById('upload');
const errorMsgElement = document.querySelector('span#errorMsg');

var imgURL;

function changePic(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $('#show-img')
          .attr('src', e.target.result);
      imgURL = e.srcElement.result;
    };
    reader.readAsDataURL(input.files[0]);
    console.log(imgURL)
  }

  upload.addEventListener("click", function () {
    $.ajax({
      type: "POST",
      url: "/imgUP",
      data: {
        url: imgURL,
      },
      success: function (e) {
        console.log(e);
      },
    });
  });
}

