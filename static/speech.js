var synth = window.speechSynthesis;

// remove and replace when you're done, these are here to make the button work
var inputForm = document.querySelector('form');
var voiceSelect = document.querySelector('select');

// keep
var voices = [];

// needed, but ignore this in implementation.
function populateVoiceList() {
  voices = synth.getVoices().sort(function (a, b) {
      const aname = a.name.toUpperCase(), bname = b.name.toUpperCase();
      if ( aname < bname ) return -1;
      else if ( aname == bname ) return 0;
      else return +1;
  });
}

// ditto above
populateVoiceList();
//if (speechSynthesis.onvoiceschanged !== undefined) {
//  speechSynthesis.onvoiceschanged = populateVoiceList;
//}

// pass your text through here
function speakText2(wordsToSpeak) {
    if (synth.speaking) {
        console.error('speechSynthesis.speaking');
        return;
    }
    if (wordsToSpeak !== '') {
    var utterThis = new SpeechSynthesisUtterance(wordsToSpeak);
    utterThis.onend = function (event) {
        console.log('SpeechSynthesisUtterance.onend');
    }
    utterThis.onerror = function (event) {
        console.error('SpeechSynthesisUtterance.onerror');
    }
    //var selectedOption = voiceSelect.selectedOptions[0].getAttribute('data-name');
    var selectedOption = 'Google UK English Male (en-GB)';
    for(i = 0; i < voices.length ; i++) {
      if(voices[i].name === selectedOption) {
        utterThis.voice = voices[i];
        break;
      }
    }
    synth.speak(utterThis);
  }
}

/*// example function which calls speak with "Look Mom, I'm on TV!". Remove on final version.
inputForm.onsubmit = function(event) {
  event.preventDefault();

  //speakText();

  speakText2('Look Mom, I\'m on TV!');
}*/