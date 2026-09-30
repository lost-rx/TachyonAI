// memory.js
// TACHYON - Memory Layer
// Stores facts + conversation state

// ------------------------------
// CORE MEMORY STORE
// ------------------------------

let memory = {
    facts: {},
    conversationSummary: "",
    lastMessages: []
};

// ------------------------------
// ADD FACT (long-term memory)
// ------------------------------

function remember(key, value) {
    memory.facts[key] = value;
}

// ------------------------------
// GET FACT
// ------------------------------

function recall(key) {
    return memory.facts[key] || null;
}

// ------------------------------
// STORE RECENT MESSAGE
// ------------------------------

function addMessage(role, text) {
    memory.lastMessages.push({ role, text });

    // limit memory size
    if (memory.lastMessages.length > 30) {
        memory.lastMessages.shift();
    }
}

// ------------------------------
// SIMPLE SUMMARY (placeholder system)
// ------------------------------
// later we can upgrade this into AI summarization

function updateSummary(text) {
    memory.conversationSummary = text;
}

// ------------------------------
// CLEAR MEMORY
// ------------------------------

function clearMemory() {
    memory.facts = {};
    memory.lastMessages = [];
    memory.conversationSummary = "";
}

// ------------------------------
// EXPORT
// ------------------------------

window.MEMORY = memory;

window.remember = remember;
window.recall = recall;
window.addMemoryMessage = addMessage;
window.updateMemorySummary = updateSummary;
window.clearMemory = clearMemory;