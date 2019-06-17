function handleError(error) {
  console.error('navigator.getUserMedia error: ', error);
}
const constraints = {video: true};

(function() {
  const video = document.querySelector('#basic video');
  const captureVideoButton = document.querySelector('#basic .capture-button');
  let localMediaStream;

  const canvas = document.createElement('canvas');

  var images = [];



  function handleSuccess(stream) {
    localMediaStream = stream;
    video.srcObject = stream;
  }

  captureVideoButton.onclick = function() {
      navigator.mediaDevices.getUserMedia(constraints).then(handleSuccess).catch(handleError);

  };

  document.querySelector('#record-button').onclick = function() {
      images=[];
      do {
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          //returns drawImage
          canvas.getContext('2d').drawImage(video, 0, 0);
          // Other browsers will fall back to image/png

          images.push(canvas.toDataURL('image/png', 1.0));

          // sleep(1000);
      } while (images.length<200)
      console.log("done");
  };

  document.querySelector('#stop-button').onclick = function() {
    video.pause();
    localMediaStream.stop();

    var json = JSON.stringify(images);

    $.ajax({
      type: 'POST',
      contentType: 'application/json',
      url: '/register',
      data : json ,

      success : function(result) {
        jQuery("#clash").html(result);
      },error : function(result){
         console.log(result);
      }
    });
  };

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

})();
