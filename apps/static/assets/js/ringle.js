
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
var ringlelyrics = document.getElementById("generate-lyrics");
var ringlesubmit = document.getElementById("ringlesubmit");
var dalle_request_box = document.getElementById("dalle-request");

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



// **********************************************
// GENERATE LYRICS
// **********************************************
ringlelyrics.addEventListener("click", async function(event) {
  // GENERATE LYRICS BUTTON
  event.preventDefault(); // Prevent the link from navigating

  if(ask_question_running){
    console.log("Ringle Dingle is already running");
    return Promise.reject(new Error("Ringle Dingle is already running"));
  }
  ask_question_running = true;

  $('#lyric-spinner').show();
  var raplyrics = encodeURIComponent(document.getElementById("raplyrics").value);

  var ai_request = "Generate a 4 stanza poem that will be narrated by ".concat(singer_name).concat(" with the following in between deliminiters STARTPOEM and ENDPOEM (respond with lyrics ONLY, no 'Verse 1:' Labeling either). Also put the poem title between delimiters STARTTITLE and ENDTITLE, and Describe in one sentence what a cover photo would be for the poem (i.e. the string will get processed in DALLE for AI image rendering), and put that prompt string in between the delimiters STARTDALLE and ENDDALLE:\n").concat(raplyrics);
  // ringlelyrics.textContent = 'Words are gathering, it may take a couple minutes...';

  console.log(ai_request);
  try {
    const response = await fetch('/make-poem', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        words: ai_request,
        singer_name: singer_name
      })
    });

    const data = await response.json();
    ask_question_running = false;
    // Hide the spinner
    $('#lyric-spinner').hide();

    // document.getElementById('lyric-spinner').style.display = 'none';
    console.log(data);
    ringlelyrics.textContent = 'Done! Click to regenerate lyrics';
    var lyrics = data.lyrics;
    var title = data.title;
    var dalle_request = data.dalle_request;
    dalle_request_box.innerHTML = dalle_request;
    airesponseTextArea.value = lyrics;
    document.getElementById("title").innerHTML = title;
    
  console.log(lyrics);

  // display #results
  $('#results').show();
  $('#title').focus();
  ask_question_running = false;
  return { lyrics: data.lyrics, title: data.title, img_url: data.img_url };

  } catch (error) {

    console.error(error);
    ask_question_running = false;
    // Hide the spinner
    $('#lyric-spinner').hide();
    submitText.textContent = 'Error in the request. Please try again or refresh the page.';
    ask_question_running = false;
    throw error;
  }

});



// **********************************************
// GENERATE AUDIO
// **********************************************
ringlesubmit.addEventListener("click", async function(event) {
  
  // SET UP THE RUNNING CONDITIONS
  event.preventDefault(); 
  $('.final-results').hide(); 
  document.getElementById('spinner').style.display = 'block';
  submitText.textContent = 'Audio is generating, it may take a couple minutes...';
  if(ask_question_running){
    console.log("Ringle Dingle is already running");
    return Promise.reject(new Error("Ringle Dingle is already running"));
  }
  
  if (audio && !audio.paused) {
    audio.pause();
  }
  ask_question_running = true;


  // GET THE INPUTS
  var dalle_request = dalle_request_box.innerHTML;
  var raplyrics = encodeURIComponent(document.getElementById("response").value);
  var response = document.getElementById("response");
  email = encodeURIComponent(document.getElementById("submit-email").value);  
  title = document.getElementById("title").innerHTML;
  console.log("Sending Narration request for a reading to voice: ".concat(singer_name));

  // HANDLE THE REQUEST
  try {
    const response = await fetch('/make-rap', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        words: raplyrics,
        title: title,
        voice: singer,
        input_file: input_file,
        email: email,
        singer_name:singer_name,
        dalle_request: dalle_request
      })
    });
   
    const data = await response.json();
    const airesponse = data.airesponse;
    var title = data.title;
    var img_url = data.img_url;

    ask_question_running = false;

    
    // CHANGE THE ON PAGE ELEMENTS - TITLE, IMAGE, AUDIO
    document.getElementById("title").innerHTML = "Title".concat(title);
    document.getElementById("result-image").src = img_url;
    document.getElementById("myAudio").innerHTML = document.getElementById("myAudio").innerHTML;

    // CHANGE THE PLAY BUTTON
    const playButton = document.getElementById("play");
    playButton.innerHTML = "Play Audio";
    playButton.style.backgroundColor = "rgba(0, 128, 0, 0.3)"; // Set the background color to a light green


    // SUCCESS!
    document.getElementById('spinner').style.display = 'none';
    $('.final-results').slideToggle();
    $('#title').focus();
    console.log(airesponse);
    submitText.textContent = 'Click to Regenerate Audio';
    showMessageModal(`Success! Your audio has been emailed to ${decodeURIComponent(email)}. Press 'Play' on the audio below to hear your track.`, false);

} catch (error) {
    console.error(error);
    ask_question_running = false;
    // Hide the spinner
    document.getElementById('spinner').style.display = 'none';
    submitText.textContent = 'Error in the request. Please try again or refresh the page.'; 
    showMessageModal('An error occurred: ' + error.message);
    throw error;
  }

  
});

  
  // END SUBMIT RAP BUTTON


// **********************************************
// ************** MISC FUNCTIONS **************

// Error handling
// Error handling

// On clicking "Enter" in #share-email input, call on the /email-share endpoint:
$('#share-email').on('keyup', function (e) {
  e.preventDefault();
  if (e.key === 'Enter' || e.keyCode === 13) {
    $('#email-spinner').show();
    $('#share-email').hide();
    if(ask_question_running){
      console.log("Ringle Dingle is already running");
      return Promise.reject(new Error("Ringle Dingle is already running"));
    }
    
    ask_question_running = true;
  
    // Encode the values
    const email = encodeURIComponent($('#share-email').val());
    const title = $('#title').text();
    const lyrics = encodeURIComponent($('#response').val());
    const img_url = $('#result-image').attr('src');

    console.log("SENDING UP", email, title, lyrics, img_url, singer_name);
    
    
    const data = {
      email: email,
      title: title,
      lyrics: lyrics,
      img_url: img_url,
      singer_name: singer_name,
    };
    $.ajax({
      type: 'POST',
      url: '/email-share',
      data: JSON.stringify(data),
      contentType: 'application/json',
      success: function (data) {
        console.log('success');
        console.log(data);
        $('#share-email-div').hide();

        showMessageModal(`Success! Your audio has been emailed to ${decodeURIComponent(email)}. Press 'Play' on the audio below to hear your track.`, false);
      },
      error: function (error) {
        console.log('error');
        console.log(error);
        showMessageModal('An error occurred: ' + error.message + '. Please make sure you\'ve filled out the form - if not, please refresh the page.');
      },
    });
    
    $('#email-spinner').hide();
    ask_question_running = false;
    return false;

  };
});



    



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

