export class ApiManager {
	constructor(apiUrl, userId, initDataHash, dataCheckString) {
		this.apiUrl = apiUrl;
		this.userId = `${userId}`;
		this.initDataHash = initDataHash;
		this.dataCheckString = dataCheckString;
	}

	async request(method, data, onCallback) {
		const authData = Telegram.WebApp.initData || "";
		const apiUrl = `${this.apiUrl}/${method}`;

		console.log(apiUrl);
		console.log(data);

		try {
			const response = await fetch(apiUrl, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-Requested-With": "XMLHttpRequest"
				},
				credentials: "include",
				body: JSON.stringify({
					...data,
					_auth: authData,
					user_id: this.userId,
					initDataHash: this.initDataHash,
					dataCheckString: this.dataCheckString,
				})
			});

			const result = await response.json();

			if (response.ok) {
				onCallback && onCallback(result);
			} else {
				onCallback && onCallback({ error: "An error occurred while placing the order. Please try again later." });
			}
		} catch (error) {
			onCallback && onCallback({ error: "An error occurred while placing the order. Please try again later." });
		}
	}
}
