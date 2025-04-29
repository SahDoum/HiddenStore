// main.js

import Cafe from './packages/cafe.js';
import { setupTelegramWebAppEvents } from './packages/telegramWebAppEvents.js';
import { initRipple } from './packages/rippleEffect.js';

import Calendar from './packages/calendar.js';

// setupTelegramWebAppEvents();
initRipple();

window.Cafe = Cafe;
window.Calendar = Calendar
window.initRipple = initRipple
