
// **********************************************
// ************** SPEECH FUNCTIONS **************
ask_question_running = false;
console.log("RINGLE DINGLE");
var singer = "alan-rickman";
var singer_name = "Alan Rickman";
var input_file = "magic.mp3";
var button = document.getElementsByTagName("push-to-talk-button")[0];
const airesponseTextArea = document.querySelector("#response");

var email = ""
var ringlesubmit = document.getElementById("ringlesubmit");
// Get the submit-box element
const submitBox = document.getElementById('submit-box');
// Get the <p> element inside the submit-box element
const submitText = submitBox.querySelector('p');

  $('#demo-opener').click(function() {
    $('#demo').slideToggle();
    // Make demo opener text to "Hide Demo":
    $('#demo-opener').text() == "Hide Demo"

  });


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
const singerItems = document.querySelectorAll('.singer-select a');
singerItems.forEach(item => {
  item.addEventListener('click', () => {
    // Remove previous selection
    singerItems.forEach(item => {
      item.classList.remove('selected');
    });

    // Add selection to clicked item
    item.classList.add('selected');

    // Log the value of the clicked item
    console.log(item.getAttribute('value').concat(item.innerText));
    singer = item.getAttribute('value');
    singer_name = item.innerText;
  });
});


ringlesubmit.addEventListener("click", function(event) {
  // SUBMIT RAP BUTTON

  // close the results div (NOT TOGGLE)
  $('#results').hide(); 
  event.preventDefault(); // Prevent the link from navigating
  var raplyrics = encodeURIComponent(document.getElementById("raplyrics").value);
  email = encodeURIComponent(document.getElementById("submit-email").value);  
  var response = document.getElementById("response");
  // var audioSrc = document.getElementById("myAudio").getElementsByTagName("source")[0].src;
  console.log("SENDING A Narration REQUEST");
  console.log("Sending request for a reading to voice: ".concat(singer_name));
  var resultPromise = make_rap("Generate a poem that will be narrated by ".concat(singer_name).concat(" about the following, in between deliminiters STARTPOEM and ENDPOEM (respond with lyrics ONLY, no 'Verse 1:' Labeling either). Also put the poem title between delimiters STARTTITLE and ENDTITLE: ").concat(raplyrics), input_file=input_file, voice=singer, email=email, singer_name=singer_name);
  

  
  resultPromise.then(function(result) {

    console.log(result);
    console.log(result.airesponse);
    console.log(result.title);
    console.log(result.img_url);


    // get the title, and img_url from the result:

    var title = result.title;
    // Add title to the text of <h4 id="title">:
    document.getElementById("title").innerHTML = title;
    
    var img_url = result.img_url;
    // Add img_url to src of <img src="" id="result-image" alt="result image">:
    document.getElementById("result-image").src = img_url;

    // Set ai_repsponse to the value of result.airesponse:
    var airesponse = result.airesponse;
    
    // var start = airesponse.indexOf("STARTPOEM") + 9;
    // var end = airesponse.indexOf("ENDPOEM");
    document.getElementById("myAudio").innerHTML = document.getElementById("myAudio").innerHTML;
    // var rapText = airesponse.substring(start, end).trim();
    const playButton = document.getElementById("play");
    playButton.innerHTML = "Play Audio";
    playButton.style.backgroundColor = "rgba(0, 128, 0, 0.3)"; // Set the background color to a light green
    response.innerHTML = airesponse;
  

    showMessageModal(`Success! Your audio has been emailed to ${decodeURIComponent(email)}. Press 'Play' on the audio below to hear your track.`, false);
    $('#results').slideToggle();

  }).catch(function(error) {
    showMessageModal('An error occurred: ' + error.message);
  });

});

  
  // END SUBMIT RAP BUTTON


// **********************************************
// ************** SPEECH FUNCTIONS **************

async function make_rap(words, input_file, voice, email="", singer_name="", show_response=true) {
  if(ask_question_running){
    console.log("Ringle Dingle is already running");
    return Promise.reject(new Error("Ringle Dingle is already running"));
  }
  ask_question_running = true;
  
  // Show the spinner
  document.getElementById('spinner').style.display = 'block';
  // Change the text of the <p> element
  submitText.textContent = 'Audio is generating, it may take a couple minutes...';

  if (audio && !audio.paused) {
    audio.pause();
  }

  try {
    const response = await fetch('/make-rap', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        words: words,
        voice: voice,
        input_file: input_file,
        email: email,
        singer_name:singer_name
      })
    });

    const data = await response.json();
    const airesponse = data.airesponse;
    ask_question_running = false;
    // Hide the spinner
    document.getElementById('spinner').style.display = 'none';
    console.log(airesponse);
    submitText.textContent = 'Step 5: Submit';

  
  return { airesponse: airesponse, title: data.title, img_url: data.img_url };

} catch (error) {
    console.error(error);
    ask_question_running = false;
    // Hide the spinner
    document.getElementById('spinner').style.display = 'none';
    submitText.textContent = 'Error in the request. Please try again or refresh the page.';
    throw error;
  }
}


// **********************************************

// Error handling
// Error handling
function showMessageModal(message, isError = true) {
  // Create a modal overlay
  const modalOverlay = document.createElement('div');
  modalOverlay.style.position = 'fixed';
  modalOverlay.style.top = 0;
  modalOverlay.style.left = 0;
  modalOverlay.style.width = '100%';
  modalOverlay.style.height = '100%';
  modalOverlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
  modalOverlay.style.display = 'flex';
  modalOverlay.style.justifyContent = 'center';
  modalOverlay.style.alignItems = 'center';
  modalOverlay.style.zIndex = 1000;

  // Create a modal to display the error message
  const modal = document.createElement('div');
  modal.style.backgroundColor = 'white';
  modal.style.padding = '20px';
  modal.style.borderRadius = '10px';
  modal.style.textAlign = 'center';
  modal.style.color = 'black';
  modal.style.width = '80%';
  modal.style.maxWidth = '400px';

  // Add error message
  const messageElement = document.createElement('p');
  messageElement.textContent = message;
  modal.appendChild(messageElement);
  document.getElementById('spinner').style.display = 'none';


  // Add an 'OK' button to close the modal
  const okButton = document.createElement('button');
  okButton.textContent = 'OK';
  okButton.style.backgroundColor = isError ? '#504caf' : '#4caf50'; // Change the button color for success messages
  okButton.style.color = 'white';
  okButton.style.border = 'none';
  okButton.style.padding = '10px 20px';
  okButton.style.fontSize = '16px';
  okButton.style.cursor = 'pointer';
  okButton.style.borderRadius = '5px';
  okButton.style.marginTop = '10px';
  okButton.addEventListener('click', () => {
    document.body.removeChild(modalOverlay);
  });

  modal.appendChild(okButton);
  modalOverlay.appendChild(modal);
  document.body.appendChild(modalOverlay);
}


// Display sample lyrics on hover
// airesponseTextArea.addEventListener('mouseover', () => {
//   if (!airesponseTextArea.value) {
//     airesponseTextArea.value = 'Sample lyrics:\nToday is Jim\'s birthday,\nBut I have news that will dismay.\nI regret to inform him,\nThat he has aids, such a grim.\nYour mother also died,\nMy heart with you will abide.';
//   }
// });

// airesponseTextArea.addEventListener('mouseout', () => {
//   if (airesponseTextArea.value.startsWith('Sample lyrics:')) {
//     airesponseTextArea.value = '';
//   }
// });

