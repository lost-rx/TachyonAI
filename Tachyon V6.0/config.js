// config.js
// TACHYON - System Configuration
// Single source of truth for global settings

window.CONFIG = {

    // ------------------------------
    // OLLAMA CONNECTION
    // ------------------------------

    API_URL: "http://localhost:11434/api/chat",
    MODEL: "llama3.2:3b",

    // ------------------------------
    // MEMORY LIMITS
    // ------------------------------

    MAX_HISTORY: 20,

    // ------------------------------
    // UI SETTINGS (future expansion)
    // ------------------------------

    THEME: "dark",
    ACCENT_COLOR: "purple",

    // ------------------------------
    // SYSTEM FLAGS
    // ------------------------------

    STREAMING: false,
    DEBUG: true,

    // ------------------------------
    // TACHYON IDENTITY
    // ------------------------------

    SYSTEM_NAME: "Tachyon"
};