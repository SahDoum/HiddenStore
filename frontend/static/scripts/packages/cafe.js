// cafe.js

import $ from 'jquery';
import './redraw';


const Cafe = {
	canPay: false,
	modeOrder: 0,
	totalPrice: 0,
	isLoading: false,
	isClosed: false,

	init(options) {
		Telegram.WebApp.ready();
		this.apiUrl = options.apiUrl;
		this.userId = options.userId;
		this.initDataHash = options.initDataHash;

		$("body").show();
		this.setupEventListeners();
		this.setupMainButton();
	},

	setupEventListeners() {
		$(".js-item-incr-btn").on("click", this.eIncrClicked.bind(this));
		$(".js-item-decr-btn").on("click", this.eDecrClicked.bind(this));
		$(".js-order-edit").on("click", this.eEditClicked.bind(this));
		$(".js-payment-edit").on("click", this.ePaymentClicked.bind(this));
		$(".js-status").on("click", this.eStatusClicked.bind(this));
		$(".js-item-cash-btn").on("click", this.ePayCash.bind(this));
		$(".js-item-card-btn").on("click", this.ePayCard.bind(this));

		// $(".js-order-comment-field").each((_, el) => {
		// 	autosize(el);
		// });

		document.addEventListener("keydown", (e) => {
			if (e.keyCode === 13) this.mainBtnClicked();
		});
	},

	setupMainButton() {
		Telegram.WebApp.MainButton.setParams({
			text_color: "#fff",
		}).onClick(this.mainBtnClicked.bind(this));
	},

	eIncrClicked(e) {
		e.preventDefault();
		const itemEl = $(e.currentTarget).closest(".js-item");
		this.incrClicked(itemEl, 1);
	},

	eDecrClicked(e) {
		e.preventDefault();
		const itemEl = $(e.currentTarget).closest(".js-item");
		this.incrClicked(itemEl, -1);
	},

	eEditClicked(e) {
		e.preventDefault();
		this.toggleMode(0);
	},

	ePaymentClicked(e) {
		e.preventDefault();
		this.toggleMode(1);
	},

	eStatusClicked() {
		this.hideStatus();
	},

	getOrderItem(itemEl) {
		const id = itemEl.data("item-id");
		return $(".js-order-item").filter(function () {
			return $(this).data("item-id") === id;
		});
	},

	updateItem(itemEl, delta) {
		const price = +itemEl.data("item-price");
		let count = +itemEl.data("item-count") || 0;
		const counterEl = $(".js-item-counter", itemEl);
		counterEl.text(count ? count : 1);

		const isSelected = itemEl.hasClass("item--selected");
		let animName = isSelected
			? delta > 0
				? "badge-incr"
				: count > 0
					? "badge-decr"
					: "badge-hide"
			: "badge-show";
		const curAnimName = counterEl.css("animation-name");
		if ((animName === "badge-incr" || animName === "badge-decr") && animName === curAnimName) {
			animName += "2";
		}
		counterEl.css("animation-name", animName);
		itemEl.toggleClass("item--selected", count > 0);

		const orderItemEl = this.getOrderItem(itemEl);
		const orderCounterEl = $(".js-order-item-counter", orderItemEl);
		orderCounterEl.text(count ? count : 1);
		orderItemEl.toggleClass("order__item--selected", count > 0);
		const orderPriceEl = $(".js-order-item-price", orderItemEl);
		const itemPrice = count * price;
		orderPriceEl.text(this.formatPrice(itemPrice));

		this.updateTotalPrice();
	},

	incrClicked(itemEl, delta) {
		if (this.isLoading || this.isClosed) {
			return;
		}
		let count = +itemEl.data("item-count") || 0;
		count += delta;
		if (count < 0) {
			count = 0;
		}
		itemEl.data("item-count", count);
		this.updateItem(itemEl, delta);
	},

	formatPrice(price) {
		return `₾${this.formatNumber(price / 100, 2, ".", ",")}`;
	},

	formatNumber(number, decimals, decPoint, thousandsSep) {
		const n = !isFinite(+number) ? 0 : +number;
		const prec = !isFinite(+decimals) ? 0 : Math.abs(decimals);
		const sep = thousandsSep || ",";
		const dec = decPoint || ".";
		let s = "";
		const toFixedFix = (n, prec) => {
			if (String(n).indexOf("e") === -1) {
				return +(Math.round(n + "e+" + prec) + "e-" + prec);
			} else {
				const arr = String(n).split("e");
				const sig = +arr[1] + prec > 0 ? "+" : "";
				return (+(
					Math.round(+arr[0] + "e" + sig + (+arr[1] + prec)) +
					"e-" +
					prec
				)).toFixed(prec);
			}
		};
		s = (prec ? toFixedFix(n, prec).toString() : String(Math.round(n))).split(".");
		if (s[0].length > 3) {
			s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
		}
		if ((s[1] || "").length < prec) {
			s[1] = s[1] || "";
			s[1] += new Array(prec - s[1].length + 1).join("0");
		}
		return s.join(dec);
	},

	updateMainButton() {
		const mainButton = Telegram.WebApp.MainButton;
		if (this.modeOrder) {
			if (this.isLoading) {
				mainButton.setParams({
					is_visible: true,
					color: "#65c36d",
				}).showProgress();
			} else {
				mainButton.setParams({
					is_visible: !!this.canPay,
					text: `PAY ${this.formatPrice(this.totalPrice)}`,
					color: "#31b545",
				}).hideProgress();
			}
		} else {
			mainButton.setParams({
				is_visible: !!this.canPay,
				text: "ЗАКАЗ",
				color: "#31b545",
			}).hideProgress();
		}
	},

	updateTotalPrice() {
		let totalPrice = 0;
		$(".js-item").each(function () {
			const itemEl = $(this);
			const price = +itemEl.data("item-price");
			const count = +itemEl.data("item-count") || 0;
			totalPrice += price * count;
		});
		this.canPay = totalPrice > 0;
		this.totalPrice = totalPrice;
		this.updateMainButton();
	},

	getOrderData() {
		const orderData = {};
		$(".js-item").each(function () {
			const itemEl = $(this);
			const id = itemEl.data("item-id");
			const count = +itemEl.data("item-count") || 0;
			if (count > 0) {
				orderData[id] = count;
			}
		});
		return JSON.stringify(orderData);
	},

	toggleMode(modeOrder) {
		this.modeOrder = modeOrder;

		if (modeOrder === 2) {
			const height = $(".page--order-overview").height();
			$("body").addClass("payment-mode");
			$(".page--order-overview").css("maxHeight", height).redraw();
			$(".page--payment").show();
		} else if (modeOrder === 1) {
			const height = $(".page--items").height();
			$("body").removeClass("payment-mode");
			$(".page--order-overview").show();
			if (height) $(".page--items").css("maxHeight", height).redraw();
			$("body").addClass("order-mode");
			// $(".js-order-comment-field").each(function () {
			// 	autosize.update(this);
			// });
			Telegram.WebApp.expand();
		} else if (modeOrder === 0) {
			$("body").removeClass("order-mode");
		}
		this.updateMainButton();
	},

	toggleLoading(loading) {
		this.isLoading = loading;
		this.updateMainButton();
		$("body").toggleClass("loading", !!this.isLoading);
		this.updateTotalPrice();
	},

	ePayCash(e) {
		const comment = $(".js-order-comment-field").val();
		const params = {
			order_data: this.getOrderData(),
			comment,
			price: this.totalPrice
		};
		this.toggleLoading(true);
		this.apiRequest("makeOrderCash", params, (result) => {
			console.log(result);
			this.toggleLoading(false);
			if (result.ok) {
				Telegram.WebApp.close();
			}
			if (result.error) {
				this.showStatus(result.error);
			}
		});
	},

	ePayCard(e) {
		const comment = $(".js-order-comment-field").val();
		const params = {
			order_data: this.getOrderData(),
			comment,
			price: this.totalPrice
		};
		this.toggleLoading(true);
		this.apiRequest("makeOrderInvoice", params, (result) => {
			console.log(result);
			this.toggleLoading(false);
			if (result.invoice) {
				window.Telegram.WebApp.openInvoice(result.invoice);
			}
			if (result.error) {
				this.showStatus(result.error);
			}
		});
	},

	mainBtnClicked() {
		if (!this.canPay || this.isLoading || this.isClosed) {
			return;
		}
		if (this.modeOrder === 1) {
			this.toggleMode(2);
		} else if (this.modeOrder === 2) {
			const comment = $(".js-order-comment-field").val();
			const params = {
				order_data: this.getOrderData(),
				comment,
				price: this.totalPrice,
			};
			if ($("#is_cash_payment_true").is(':checked')) {
				this.toggleLoading(true);
				this.apiRequest("makeOrderCash", params, (result) => {
					console.log(result);
					this.toggleLoading(false);
					if (result.ok) {
						Telegram.WebApp.close();
					}
					if (result.error) {
						this.showStatus(result.error);
					}
				});
			} else if ($("#is_cash_payment_false").is(':checked')) {
				this.toggleLoading(true);
				this.apiRequest("makeOrderInvoice", params, (result) => {
					console.log(result);
					this.toggleLoading(false);
					if (result.invoice) {
						window.Telegram.WebApp.openInvoice(result.invoice);
					}
					if (result.error) {
						this.showStatus(result.error);
					}
				});
			}
		} else if (this.modeOrder === 0) {
			this.toggleMode(1);
		}
	},

	showStatus(text) {
		clearTimeout(this.statusTo);
		$(".js-status").text(text).addClass("status--shown");
		if (!this.isClosed) {
			this.statusTo = setTimeout(() => {
				this.hideStatus();
			}, 2500);
		}
	},

	hideStatus() {
		clearTimeout(this.statusTo);
		$(".js-status").removeClass("status--shown");
	},

	apiRequest(method, data, onCallback) {
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
	},
};

export default Cafe;
