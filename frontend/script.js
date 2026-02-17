const inputBox = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const micBtn = document.getElementById("mic-btn");
const chatBox = document.getElementById("chat-box");
const stopBtn = document.getElementById("stop-btn");
let selectedVoice = null;

// load voices
window.speechSynthesis.onvoiceschanged = () => {
  const voices = window.speechSynthesis.getVoices();
  selectedVoice = voices.find(v =>
    /Daniel|Google UK English Male|Microsoft David/.test(v.name)
  );
};

sendBtn.addEventListener("click", () => {
  const msg = inputBox.value.trim();
  if (!msg) return;
  addMessage("user", msg);
  inputBox.value = "";
  sendToJarvis(msg);
});

inputBox.addEventListener("keydown", e => {
  if (e.key === "Enter") {
    e.preventDefault();
    sendBtn.click();
  }
});

stopBtn.addEventListener("click", () => {
  window.speechSynthesis.cancel();
});

micBtn.addEventListener("click", () => {
  const recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  micBtn.innerText = "🎙️ Listening...";
  recognition.start();
  recognition.onresult = e => {
    const voiceInput = e.results[0][0].transcript;
    micBtn.innerText = "🎤";
    addMessage("user", voiceInput);
    sendToJarvis(voiceInput);
  };
  recognition.onerror = () => {
    micBtn.innerText = "🎤";
    alert("Mic input failed. Try again.");
  };
});

function sendToJarvis(msg) {
  fetch("http://127.0.0.1:8000/api/ask/", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({message: msg}),
  })
    .then(res => res.json())
    .then(data => {
      addMessage("bot", data.reply);
      speak(data.reply);
    })
    .catch(() => {
      addMessage("bot", "⚠️ Jarvis failed to reply.");
    });
}

function addMessage(sender, text) {
  const div = document.createElement("div");
  div.className = sender === "user" ? "user-msg" : "bot-msg";
  div.innerText = `${sender==="user"?"🧑 You":"🤖 Jarvis"}: ${text}`;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function speak(text) {
  window.speechSynthesis.cancel();
  const utter = new SpeechSynthesisUtterance(text);
  utter.rate = 2.3; utter.pitch = 0.8; utter.lang = "en-GB";
  if (selectedVoice) utter.voice = selectedVoice;
  window.speechSynthesis.speak(utter);
}

// starfield
function createStars(count=100) {
  const field = document.getElementById("starfield");
  for (let i=0; i<count; i++) {
    const star = document.createElement("div");
    star.classList.add("star");
    const size = Math.random()*2+1;
    star.style.width  = `${size}px`;
    star.style.height = `${size}px`;
    star.style.left   = `${Math.random()*100}vw`;
    star.style.animationDuration = `${Math.random()*5+3}s`;
    field.appendChild(star);
  }
}
document.addEventListener("DOMContentLoaded", () => {
  createStars(150);
});
