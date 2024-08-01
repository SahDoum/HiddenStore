// telegramWebAppEvents.js

export const setupTelegramWebAppEvents = () => {
	window.Telegram.WebApp.onEvent('invoiceClosed', (object) => {
		if (object.status === 'pending' || object.status === 'paid') {
			window.Telegram.WebApp.close();
		}
	});
};

