// main.js

import Cafe from './packages/cafe.js';
import { setupTelegramWebAppEvents } from './packages/telegramWebAppEvents.js';
import { initRipple } from './packages/rippleEffect.js';

setupTelegramWebAppEvents();
initRipple();

window.Cafe = Cafe;
