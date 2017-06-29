var audio_context;
var recorder;

function startUserMedia(stream) {
  var input = audio_context.createMediaStreamSource(stream);
  recorder = new Recorder(input);
}

function initAudio(){
  try {
    window.AudioContext = window.AudioContext || window.webkitAudioContext;
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
    window.URL = window.URL || window.webkitURL;

    audio_context = new AudioContext;
  } catch (e) {
    alert('No web audio support in this browser!');
  }

  navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
    console.log('No live audio input: ' + e);
  });
}

function uploadAudio(){
  recorder && recorder.exportWAV(function(blob) {
    var formData = new FormData();
    formData.append("voice", blob);

    var request = new XMLHttpRequest();

    request.onreadystatechange = function() {
        console.log('state:', this.readyState);
        if (this.readyState == 4 && this.status == 200) {
            console.log(request.responseText);
            $('#container').append(request.responseText);
        }
    };

    request.open("post", "/audio");
    request.send(formData);



  });
}

initAudio();

$('#start').click(function(){
    console.log('start');
    recorder && recorder.record();
});

$('#stop').click(function(){
    console.log('stop');
    recorder && recorder.stop();
    uploadAudio();
    recorder.clear();
});
