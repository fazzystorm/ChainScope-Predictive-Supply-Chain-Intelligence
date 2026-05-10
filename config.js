// config.js
// Extracting API keys and URLs to make export and migration easier.

window.CHAINSCOPE_CONFIG = {
    // MapTiler API Key for styling
    MAP_STYLE_URL: 'https://api.maptiler.com/maps/darkmatter/style.json?key=wzYbF8hXDKBEhoG9HnCW',

    // Cloudflare Worker URL for live ship tracking
    SHIP_WORKER_URL: 'https://delicate-recipe-b1b3.quantumfaizan.workers.dev/',

    // CORS proxy used for fetching the BBC RSS feedLoading..

    NEWS_PROXY_URL: 'https://api.allorigins.win/get?url='
};
