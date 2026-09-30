// script.js
// TACHYON - Core Router (FINAL CLEAN VERSION)

// ------------------------------
// INIT SYSTEM
// ------------------------------

function initTachyon() {

    if (!window.TachyonUI) {
        console.error("Tachyon: UI not loaded");
        return;
    }

    // Bind input from UI
    window.TachyonUI.bindInput(handleInput);

    window.TachyonUI.systemMessage("Tachyon booted.");
    window.TachyonUI.systemMessage("Systems online.");
}

// ------------------------------
// INPUT PIPELINE
// ------------------------------

async function handleInput(text) {

    // 1. Always show user message
    window.TachyonUI.addMessage("User", text);

    // 2. Store in memory
    window.addMemoryMessage?.("user", text);

    // ------------------------------
    // COMMAND ROUTE
    // ------------------------------

    if (text.startsWith("/")) {

        const result = window.handleCommand?.(text);

        if (result !== undefined) {
            window.TachyonUI.systemMessage(result);
        }

        return;
    }

    // ------------------------------
    // AI ROUTE
    // ------------------------------

    try {

        const reply = await window.askOllama?.(text);

        // show AI response
        window.TachyonUI.addMessage("Tachyon", reply);

        // store in memory
        window.addMemoryMessage?.("assistant", reply);

    } catch (err) {

        console.error(err);

        window.TachyonUI.systemMessage(
            "AI error: unable to reach Ollama."
        );
    }
}

// ------------------------------
// BOOT
// ------------------------------

window.addEventListener("DOMContentLoaded", initTachyon);