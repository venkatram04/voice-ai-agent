const micBtn = document.getElementById("micBtn");
const liveTranscript = document.getElementById("liveTranscript");
const chatBox = document.getElementById("chatBox");
const appointmentCard = document.getElementById("appointmentCard");

const socket = new WebSocket("ws://127.0.0.1:8000/ws");

let recognition;
let isListening = false;
let finalTranscript = "";

// ==========================
// Speech Recognition Setup
// ==========================
if ("webkitSpeechRecognition" in window) {

    recognition = new webkitSpeechRecognition();

} else {

    alert("Speech Recognition not supported in this browser.");
}

recognition.continuous = true;
recognition.interimResults = true;
recognition.lang = "en-IN";

// ==========================
// Mic Button
// ==========================
micBtn.onclick = () => {

    if (!isListening) {

        finalTranscript = "";

        recognition.start();

        isListening = true;

        micBtn.innerText = "🎙 Listening...";

    } else {

        recognition.stop();

        isListening = false;

        micBtn.innerText = "🎤 Start Speaking";
    }
};

// ==========================
// Live Listening
// ==========================
recognition.onresult = (event) => {

    let interimTranscript = "";

    for (
        let i = event.resultIndex;
        i < event.results.length;
        ++i
    ) {

        const transcript =
            event.results[i][0].transcript;

        if (event.results[i].isFinal) {

            finalTranscript += transcript + " ";

        } else {

            interimTranscript += transcript;
        }
    }

    liveTranscript.innerHTML = `
        <div class="live-box">
            <b>Listening:</b><br>
            ${finalTranscript}
            <span class="interim">
                ${interimTranscript}
            </span>
        </div>
    `;
};

// ==========================
// When Speech Ends
// ==========================
recognition.onend = () => {

    isListening = false;

    micBtn.innerText = "🎤 Start Speaking";

    const cleanedTranscript =
        finalTranscript.trim();

    if (cleanedTranscript.length > 0) {

        // Show user message
        addMessage(
            "You",
            cleanedTranscript,
            "user-message"
        );

        // Send to backend
        socket.send(cleanedTranscript);
    }

    finalTranscript = "";
};

// ==========================
// Receive AI Response
// ==========================
socket.onmessage = (event) => {

    const data = JSON.parse(event.data);

    // Add AI response
    addMessage(
        "AI",
        data.response,
        "ai-message"
    );

    // Speak AI response
    speakText(data.response);

    // Show appointment details
    if (data.appointment) {

        showAppointment(data.appointment);
    }
};

// ==========================
// Add Message to Chat
// ==========================
function addMessage(sender, text, className) {

    const messageDiv =
        document.createElement("div");

    messageDiv.className =
        `message ${className}`;

    messageDiv.innerHTML = `
        <div class="sender">
            ${sender}
        </div>

        <div class="text">
            ${text}
        </div>
    `;

    chatBox.appendChild(messageDiv);

    // Auto scroll
    chatBox.scrollTop =
        chatBox.scrollHeight;
}

// ==========================
// AI Voice
// ==========================
function speakText(text) {

    window.speechSynthesis.cancel();

    const speech =
        new SpeechSynthesisUtterance(text);

    speech.lang = "en-IN";

    speech.rate = 1;

    speech.pitch = 1;

    window.speechSynthesis.speak(speech);
}

// ==========================
// Appointment Card
// ==========================
function showAppointment(data) {

    appointmentCard.innerHTML = `
        <div class="appointment-item">
            <b>Name:</b>
            ${data.patient_name}
        </div>

        <div class="appointment-item">
            <b>Age:</b>
            ${data.age}
        </div>

        <div class="appointment-item">
            <b>Doctor:</b>
            ${data.doctor}
        </div>

        <div class="appointment-item">
            <b>Date:</b>
            ${data.date}
        </div>

        <div class="appointment-item">
            <b>Slot:</b>
            ${data.slot}
        </div>

        <div class="appointment-item">
            <b>Reason:</b>
            ${data.reason}
        </div>

        <div class="appointment-status">
            ✅ Appointment Booked
        </div>
    `;
}