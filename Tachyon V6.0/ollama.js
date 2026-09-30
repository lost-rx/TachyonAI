// ollama.js
// TACHYON - AI Brain Layer
// ONLY handles communication with Ollama

// ------------------------------
// CONVERSATION MEMORY (TEMPORARY)
// ------------------------------

let conversation = [];

// ------------------------------
// ADD TO CONTEXT
// ------------------------------

function addToConversation(role, content) {
    conversation.push({ role, content });

    // keep it bounded (prevents infinite memory growth)
    if (conversation.length > (window.CONFIG?.MAX_HISTORY || 20)) {
        conversation.shift();
    }
}

// ------------------------------
// BUILD PAYLOAD
// ------------------------------

function buildMessages() {
    const systemPrompt =
        window.getPrompt?.() ||
        "You are Tachyon, a helpful AI.";

    return [
        {
            role: "system",
            content: systemPrompt
        },
        ...conversation
    ];
}

// ------------------------------
// MAIN AI CALL
// ------------------------------

async function askOllama(userText) {

    addToConversation("user", userText);

    try {
        const res = await fetch(window.CONFIG.API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: window.CONFIG.MODEL,
                stream: false,
                messages: buildMessages()
            })
        });

        if (!res.ok) {
            throw new Error("HTTP " + res.status);
        }

        const data = await res.json();

        const reply =
            data.message?.content ||
            "No response.";

        addToConversation("assistant", reply);

        return reply;
    }

    catch (err) {
        console.error(err);

        return "Tachyon error: cannot reach Ollama.";
    }
}

// ------------------------------
// CLEAR MEMORY
// ------------------------------

function clearConversation() {
    conversation = [];
}

// ------------------------------
// OPTIONAL TEST FUNCTION
// ------------------------------

async function testOllama() {
    try {
        const res = await fetch(window.CONFIG.API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                model: window.CONFIG.MODEL,
                stream: false,
                messages: [
                    {
                        role: "user",
                        content: "Reply with ONLINE"
                    }
                ]
            })
        });

        return res.ok;
    } catch {
        return false;
    }
}

// ------------------------------
// EXPORT TO GLOBAL
// ------------------------------

window.askOllama = askOllama;
window.clearConversation = clearConversation;
window.testOllama = testOllama;