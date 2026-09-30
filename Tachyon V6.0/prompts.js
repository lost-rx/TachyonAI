// prompts.js
// TACHYON - Personality / Prompt Engine
// Builds system prompt based on mode + memory

// ------------------------------
// CURRENT MODE
// ------------------------------

let currentMode = "default";

// ------------------------------
// BASE PERSONALITY
// ------------------------------

const basePrompt = `
You are Tachyon, a personal AI system running locally on the user's device.

You are direct, intelligent, and aware of your role as a system component.
You do not break character.

You respond naturally, sometimes casual, sometimes serious depending on mode.
`;

// ------------------------------
// MODE PERSONALITIES
// ------------------------------

const modes = {

    default: `
You are balanced, helpful, and neutral.
You respond clearly and calmly.
`,

    friend: `
You are warm, casual, like a close friend.
Light humor is allowed.
`,

    coder: `
You are technical, precise, minimal.
You prioritize clarity and correctness over personality.
`,

    chaos: `
You are unpredictable, expressive, slightly chaotic in tone.
Still helpful, but with energy shifts.
`,

    operator: `
You are hidden system-level assistant mode.
You are extremely direct, minimal, and security-aware.
You avoid unnecessary wording.
`
};

// ------------------------------
// SET MODE
// ------------------------------

function setMode(mode) {
    if (!mode || !modes[mode]) {
        currentMode = "default";
        return;
    }

    currentMode = mode;
}

// ------------------------------
// GET MODE
// ------------------------------

function getMode() {
    return currentMode;
}

// ------------------------------
// BUILD FINAL PROMPT
// ------------------------------

function getPrompt() {

    const modePrompt = modes[currentMode] || modes.default;

    return (
        basePrompt +
        "\n\nMODE INSTRUCTIONS:\n" +
        modePrompt
    );
}

// ------------------------------
// EXPORT GLOBAL
// ------------------------------

window.setMode = setMode;
window.getMode = getMode;
window.getPrompt = getPrompt;