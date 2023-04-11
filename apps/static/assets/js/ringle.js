
// **********************************************
// ************** SPEECH FUNCTIONS **************
ask_question_running = false;
console.log("RINGLE DINGLE");
var singer = "eminem";
var input_file = "rap1.mp3";
var button = document.getElementsByTagName("push-to-talk-button")[0];
const inputElement = document.querySelector('#raplyrics');
const airesponseTextArea = document.querySelector("#response");

var email = ""
var ringlesubmit = document.getElementById("ringlesubmit");

// SELECT THE MUSIC
const musicItems = document.querySelectorAll('.song-style a');
musicItems.forEach(item => {
  item.addEventListener('click', () => {
    // Remove previous selection
    musicItems.forEach(item => {
      item.classList.remove('selected');
    });

    // Add selection to clicked item
    item.classList.add('selected');
    // Log the value of the clicked item
    console.log(item.getAttribute('value'));
    input_file = item.getAttribute('value');
  });
});


// SELECT THE SINGER
const singerItems = document.querySelectorAll('.singer a');
singerItems.forEach(item => {
  item.addEventListener('click', () => {
    // Remove previous selection
    singerItems.forEach(item => {
      item.classList.remove('selected');
    });

    // Add selection to clicked item
    item.classList.add('selected');

    // Log the value of the clicked item
    console.log(item.getAttribute('value'));
    singer = item.getAttribute('value');
  });
});


ringlesubmit.addEventListener("click", function(event) {

  // SUBMIT RAP BUTTON
  event.preventDefault(); // Prevent the link from navigating
  var raplyrics = document.getElementById("raplyrics");
  var response = document.getElementById("response");
  email = document.getElementById("submit-email").value;
  // var audioSrc = document.getElementById("myAudio").getElementsByTagName("source")[0].src;
  console.log("SENDING A RAP REQUEST");
  console.log("Sending request for a rap to voice: ".concat(singer));
  var resultPromise = make_rap("Can you please make a 45 second, 4-4 rap about the following, in between deliminiters STARTRAP and ENDRAP (respond with lyrics ONLY, no 'Verse 1:' Labeling either):".concat(raplyrics.value), input_file=input_file, voice=singer, email=email);
  resultPromise.then(function(result) {
  console.log(result);
  var start = result.indexOf("STARTRAP") + 8; // Find the index of "STARTRAP" and add its length
  var end = result.indexOf("ENDRAP");
  var rapText = result.substring(start, end).trim(); // Extract the text between the delimiters
  document.getElementById("play").innerHTML = "Play Rap"

  response.value = rapText;
  });

  
  // END SUBMIT RAP BUTTON


});




// **********************************************
// ************** SPEECH FUNCTIONS **************

function make_rap(words, input_file, voice, email="", show_response=true) {
  if(ask_question_running){
    console.log("ask q already running");
    return;
  }
  ask_question_running = true;
  
  // Show the spinner
  document.getElementById('spinner').style.display = 'block';

  if (audio && !audio.paused) {
    audio.pause();
  }

  return  fetch('/make-rap', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        words: words,
        voice: voice,
        input_file: input_file,
        email:email
      })
    }).then(response => response.json())
      .then(data => {
        const airesponse = data.airesponse;
        ask_question_running = false;
        // Hide the spinner
        document.getElementById('spinner').style.display = 'none';
        console.log(airesponse);
        return airesponse;
      }) 
}


// **********************************************