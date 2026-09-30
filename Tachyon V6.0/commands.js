// commands.js
// TACHYON - Simple Command Layer
// No plugins, no registry system, just direct commands

// ------------------------------
// COMMAND HANDLER
// ------------------------------

function handleCommand(text) {

    const parts = text.trim().split(" ");
    const cmd = parts[0].toLowerCase();
    const args = parts.slice(1);

    switch (cmd) {

        // ----------------------
        // HELP
        // ----------------------
        case "/help":
            window.TachyonUI.systemMessage(
                "Commands: /help /clear /mode /about"
            );
            break;

        // ----------------------
        // CLEAR CHAT
        // ----------------------
        case "/clear":
            clearChat();
            break;

        // ----------------------
        // MODE SWITCH (stub for now)
        // ----------------------
        case "/mode":
            setMode(args[0]);
            break;

        // ----------------------
        // ABOUT
        // ----------------------
        case "/about":
            window.TachyonUI.systemMessage(
                "Tachyon - personal AI system running locally."
            );
            break;

        // ----------------------
        // UNKNOWN COMMAND
        // ----------------------
        default:
            window.TachyonUI.systemMessage(
                "Unknown command: " + cmd
            );
            break;
    }
}

// ------------------------------
// CLEAR FUNCTION
// ------------------------------

function clearChat() {

    const box = document.getElementById("chatBox");

    if (box) {
        box.innerHTML = "";
    }

    window.TachyonUI.systemMessage(
        "Chat cleared."
    );
}

// ------------------------------
// MODE SYSTEM (stub)
// ------------------------------

function setMode(mode) {

    if (!mode) {
        window.TachyonUI.systemMessage(
            "Usage: /mode <name>"
        );
        return;
    }

    window.TachyonUI.systemMessage(
        "Mode switched to: " + mode
    );
}

// ------------------------------
// EXPORT TO GLOBAL
// ------------------------------

window.handleCommand = handleCommand;