// ui.js
// TACHYON - UI Layer
// Handles rendering + basic interaction only

// ------------------------------
// DOM REFERENCES
// ------------------------------

const chatBox = document.getElementById("chatBox");
const input = document.getElementById("chatInput");
const form = document.getElementById("chatForm");

// ------------------------------
// MESSAGE RENDERING
// ------------------------------

function addMessage(role, text) {
    if (!chatBox) return;

    const message = document.createElement("div");

    message.className = `msg ${role.toLowerCase()}`;

    message.innerHTML = `
        <span class="role">${role}:</span>
        <span class="text">${text}</span>
    `;

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;

    return message;
}

// ------------------------------
// INPUT HANDLING HOOK
// (NO LOGIC YET - JUST EVENT HOOK)
// ------------------------------

function bindInput(onSubmit) {
    if (!form || !input) {
        console.error("Tachyon UI: Missing chatForm or chatInput");
        return;
    }

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const text = input.value.trim();
        if (!text) return;

        input.value = "";

        if (onSubmit) {
            onSubmit(text);
        }
    });
}

// ------------------------------
// SYSTEM MESSAGE HELPERS
// ------------------------------

function systemMessage(text) {
    return addMessage("System", text);
}

// ------------------------------
// EXPORT TO GLOBAL (NO MODULES)
// ------------------------------

window.TachyonUI = {
    addMessage,
    bindInput,
    systemMessage
};