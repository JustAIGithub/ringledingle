$(document).ready(function() {


  // **********************************************
  // DEFAULTS
  // **********************************************

  ask_question_running = false;
  console.log("RINGLE DINGLE");
  var singer = "alan-rickman";
  var singer_name = "Alan Rickman";
  var input_file = "magic.mp3";
  var progressBar = $('.progress-bar');
  var totalSteps = $('.carousel-inner .carousel-item').length - 2; // -2 to exclude the "Generating" and "100%" steps
  var currentStep = $('.carousel-inner .carousel-item.active').index();

  async function generateLyrics() {
    console.log("Generating Lyrics...");

    
// **********************************************
// GENERATE LYRICS
// **********************************************


  if(ask_question_running){
    console.log("Ringle Dingle is already running");
    showMessageModal("Ringle Dingle is already running");
    return Promise.reject(new Error("Ringle Dingle is already running"));
  }
  ask_question_running = true;

  // get the text from the about box and escape it
  var about = document.getElementById("about").value;
 

  console.log("ABOUT", about, "EMAIL", email);
  var ai_request = "Generate a 4 stanza poem that will be narrated by ".concat(singer_name).concat(". Your poem MUST be in between the deliminiters STARTPOEM and ENDPOEM (respond with poem text ONLY, no 'Verse 1:' labels either).\n Also, the poem title will be between delimiters STARTTITLE and ENDTITLE.\nMake this poem from the following\n").concat(about);
  // ringlelyrics.textContent = 'Words are gathering, it may take a couple minutes...';

  console.log(ai_request);
  try {
    const response = await fetch('/generate-lyrics', {
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
  
  
    // document.getElementById('lyric-spinner').style.display = 'none';
    console.log(data);
    var lyrics = data.lyrics;
    var title = data.title;
    document.getElementById("title").innerHTML = title;

    var lyrics_box = document.getElementById("edit-lyrics");
    lyrics_box.innerHTML = lyrics;

  // Hide the spinner
  $('.spinner').hide();

    
  console.log(lyrics);
  $('.carousel').carousel('next');


  // display #results
  ask_question_running = false;
  return { lyrics: data.lyrics, title: data.title, img_url: data.img_url };

  } catch (error) {

    console.error(error);
    // Hide the spinner
    $('#lyric-spinner').hide();
    // THROW THE ERROR MODAL
    // submitText.textContent = 'Error in the request. Please try again or refresh the page.';
    ask_question_running = false;
    throw error;
  }


  }

  async function generateDingle() {
    var email = document.getElementById("email").innerText;
    console.log("Generating Dingle...");

      
  // **********************************************
  // GENERATE AUDIO
  // **********************************************
  

  // document.getElementById('spinner').style.display = 'inline-block';
  // submitText.textContent = 'Audio is generating, it may take a couple minutes...';
  if(ask_question_running){
    console.log("Ringle Dingle is already running");
    return Promise.reject(new Error("Ringle Dingle is already running"));
  }
  
  if (audio && !audio.paused) {
    audio.pause();
  }
  ask_question_running = true;


  // GET THE INPUTS
  var lyrics = encodeURIComponent(document.getElementById("edit-lyrics").value);
  var email = encodeURIComponent(document.getElementById("email").value);  
  var title = document.getElementById("title").innerHTML;
  console.log("Sending Narration request for a reading to voice: ".concat(singer_name));

  // HANDLE THE REQUEST
  try {
    const response = await fetch('/generate-dingle', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        words: lyrics,
        title: title,
        voice: singer,
        input_file: input_file,
        email: email,
        singer_name:singer_name      })
    });
   
    const data = await response.json();
    const airesponse = data.airesponse;
    var title = data.title;
    var img_url = data.img_url;
    var lrc_lyrics = data.lrc_lyrics;

    ask_question_running = false;

    
    // CHANGE THE ON PAGE ELEMENTS - TITLE, IMAGE, AUDIO
    document.getElementById("final-title").innerHTML = "Title: ".concat(title);
    document.getElementById("final-lyrics").innerHTML = "Title: ".concat(title);
    document.getElementById("final-image").src = img_url;
    // document.getElementById("myAudio").innerHTML = document.getElementById("myAudio").innerHTML;

    // CHANGE THE PLAY BUTTON
    const playButton = document.getElementById("play");
    playButton.innerHTML = "Play Audio";
    playButton.style.backgroundColor = "rgba(0, 128, 0, 0.3)"; // Set the background color to a light green


    // SUCCESS!
    // document.getElementById('.spinner').style.display = 'none';
    console.log(airesponse);
    // submitText.textContent = 'Click to Regenerate Audio';
    // next carousel
    $('.carousel').carousel('next');
    showMessageModal(`Success! Your audio has been emailed to ${decodeURIComponent(email)}. Press 'Play' on the audio below to hear your track.`, false);

} catch (error) {
    console.error(error);
    ask_question_running = false;
    // Hide the spinner
    // document.getElementById('spinner').style.display = 'none';
    // submitText.textContent = 'Error in the request. Please try again or refresh the page.'; 
    showMessageModal('An error occurred: ' + error.message);
    throw error;
  }

  }



  
  $('input').keypress(function(e) {
      if (e.which == 13) { // Enter key pressed
          e.preventDefault();
          $('.carousel').carousel('next');
      }
  });
  $('textarea').keypress(function(e) {
      if (e.which == 13) { // Enter key pressed
          e.preventDefault();
          $('.carousel').carousel('next');
      }
  });

 
  $('.carousel').off('slid.bs.carousel').on('slid.bs.carousel', function() {
    progressBar = $('.progress-bar');
    totalSteps = $('.carousel-inner .carousel-item').length - 2; // -2 to exclude the "Generating" and "100%" steps
    currentStep = $('.carousel-inner .carousel-item.active').index();  
    console.log("ASSIGNED CURRENT STEP", currentStep);
    

    if (currentStep <= totalSteps) {
        var progressValue = (currentStep / totalSteps) * 100;
        progressBar.css('width', progressValue + '%');
        progressBar.attr('aria-valuenow', progressValue);
        progressBar.html(Math.round(progressValue) + '%');
    } else {
        progressBar.css('width', '100%');
        progressBar.attr('aria-valuenow', 100);
        progressBar.html('100%');
    }

    // Log "fourth element" when the fourth carousel item is passed
    if (currentStep == 4) {
      generateLyrics();
    }
    
    if (currentStep == 6) {
      generateDingle();
    }

    $('.carousel-item.active').find('.entry-item').focus();


});

$(document).keydown(function(e) {
  // When you click the right arrow on the keyboard, it will go to the next step:

  // console.log("currentStep", currentStep, "totalSteps", totalSteps);
  switch(true) {
    case e.which == 39 && currentStep < totalSteps: // right
      $('.carousel').carousel('next');
      break;
    case e.which == 37 && currentStep > 0 && currentStep != totalSteps-1 && currentStep != totalSteps-4: // left
      $('.carousel').carousel('prev');
      break;
    default: 
      return; // exit this handler for other keys
  }
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
    input_file = item.getAttribute('value');
    $('.carousel').carousel('next');
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
    console.log(item.getAttribute('value').concat(" ").concat(item.innerText));
    singer = item.getAttribute('value');
    singer_name = item.innerText;
    $('.carousel').carousel('next');
  });
});




// On clicking "Enter" in #share-email input, call on the /email-share endpoint:
$('#share-email').on('keyup', function (e) {
  e.preventDefault();

  // Add to conditions if #btn is clicked, do the same thing as below

  if (e.key === 'Enter' || e.keyCode === 13) {
    document.getElementById('#email-spinner').style = 'inline-block';
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

        showMessageModal(`Success! Your audio has been emailed to ${decodeURIComponent(email)}. Press 'Start Over' to try to Ringle another Dingle.`, false);
      },
      error: function (error) {
        console.log('error');
        console.log(error);
        showMessageModal('An error occurred: ' + error.message + '. Please make sure you\'ve filled out the form - if not, please refresh the page.');
        $('#share-email').slideToggle();
      },
    });
    
    $('#email-spinner').hide();
    $('#share-email').slideToggle();
    $('#share-email').val('');
    ask_question_running = false;
    return false;

  };
});






  });
