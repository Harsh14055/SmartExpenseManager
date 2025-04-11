// document.addEventListener("DOMContentLoaded", function () {
//     const chatbotBtn = document.getElementById("chatbot-btn");
//     const chatbotContainer = document.getElementById("chatbot-container");
//     const closeChatbot = document.getElementById("close-chatbot");
//     const sendChatbot = document.getElementById("send-chatbot");
//     const chatbotInput = document.getElementById("chatbot-input");
//     const chatbotMessages = document.getElementById("chatbot-messages");

//     // Show chatbot UI
//     chatbotBtn.addEventListener("click", function () {
//         chatbotContainer.style.display = "flex";
//     });

//     // Hide chatbot UI
//     closeChatbot.addEventListener("click", function () {
//         chatbotContainer.style.display = "none";
//     });

//     // Send message to chatbot
//     sendChatbot.addEventListener("click", function () {
//         sendMessage();
//     });

//     chatbotInput.addEventListener("keypress", function (e) {
//         if (e.key === "Enter") {
//             sendMessage();
//         }
//     });

//     function sendMessage() {
//         const userMessage = chatbotInput.value.trim();
//         if (userMessage === "") return;

//         appendMessage("You: " + userMessage, "user-message");

//         fetch("/api/chatbot", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({ message: userMessage }),
//         })
//         .then(response => response.json())
//         .then(data => {
//             appendMessage("Bot: " + data.response, "bot-message");
//         })
//         .catch(error => console.error("Error:", error));

//         chatbotInput.value = "";
//     }

//     function appendMessage(text, className) {
//         const messageDiv = document.createElement("div");
//         messageDiv.classList.add(className);
//         messageDiv.textContent = text;
//         chatbotMessages.appendChild(messageDiv);
//         chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
//     }
// });


document.addEventListener("DOMContentLoaded", function () {
    console.log("Chatbot script loaded."); // Check if script is running

    const chatbotBtn = document.getElementById("chatbot-btn");
    const chatbotContainer = document.getElementById("chatbot-container");
    const closeChatbot = document.getElementById("close-chatbot");
    const sendButton = document.getElementById("send-chatbot");
    const inputField = document.getElementById("chatbot-input");
    const messageBox = document.getElementById("chatbot-messages");

    if (!chatbotBtn || !chatbotContainer || !closeChatbot || !sendButton || !inputField || !messageBox) {
        console.error("One or more chatbot elements not found!");
        return;
    }

    console.log("Chatbot elements loaded successfully.");

    chatbotBtn.addEventListener("click", function () {
        chatbotContainer.style.display = chatbotContainer.style.display === "block" ? "none" : "block";
        console.log("Chatbot toggled:", chatbotContainer.style.display);
    });

    closeChatbot.addEventListener("click", function () {
        chatbotContainer.style.display = "none";
        console.log("Chatbot closed.");
    });

    sendButton.addEventListener("click", function () {
        const userMessage = inputField.value.trim();
        if (userMessage === "") {
            console.warn("Empty message, ignoring.");
            return;
        }

        console.log("Sending message:", userMessage);
        messageBox.innerHTML += `<div class="chatbot-message user-message">${userMessage}</div>`;

        fetch('/chatbot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Received response:", data);
            messageBox.innerHTML += `<div class="chatbot-message bot-message">${data.response}</div>`;
        })
        .catch(error => console.error("Error sending message:", error));

        inputField.value = "";
    });
});
