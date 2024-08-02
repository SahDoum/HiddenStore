export class ApiManager {
	constructor(apiUrl, userId, initDataHash, dataCheckString) {
		this.apiUrl = apiUrl;
		this.userId = userId;
		this.initDataHash = initDataHash;
		this.dataCheckString = dataCheckString;
	}

	request(method, data, onCallback) {
		const authData = Telegram.WebApp.initData || "";
		const apiUrl = `${this.apiUrl}/${method}`;
		let userId = 155493213;
		if (this.userId) userId = this.userId;
		console.log(apiUrl);
		$.ajax(apiUrl, {
			type: "POST",
			data: {
				...data,
				_auth: authData,
				method,
				user_id: userId,
				initDataHash: this.initDataHash,
				dataCheckString: this.dataCheckString,
			},
			dataType: "json",
			xhrFields: {
				withCredentials: true,
			},
			success: (result) => {
				onCallback && onCallback(result);
			},
			error: (xhr) => {
				onCallback && onCallback({ error: "При заказе случилась ошибка. Попробуйте еще раз чуть позже." });
			},
		});
	}
}
