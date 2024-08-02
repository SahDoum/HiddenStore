// main.js

import Cafe from './packages/cafe.js';
import { setupTelegramWebAppEvents } from './packages/telegramWebAppEvents.js';
import { initRipple } from './packages/rippleEffect.js';

setupTelegramWebAppEvents();
initRipple();

// Initialize Cafe with options
const cafe = new Cafe();
cafe.init({
	apiUrl: `${window.location.origin}/api`,
	userId: 0, // Replace with actual user ID if available
	initDataHash: '',
	dataCheckString: ''
});
