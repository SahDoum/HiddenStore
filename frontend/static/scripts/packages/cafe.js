// cafe.js

import $ from 'jquery';
import './redraw';
import { StatusManager, Modes } from './cafeStatusManager'
import { Item } from './cafeItem'
import { ApiManager } from './apiManager'


class Cafe {
	constructor() {
		this.canPay = false;
		this.totalPrice = 0;
		this.isLoading = false;
		this.isClosed = false;
		this.statusManager = new StatusManager();
	}

	// setup

	init(options) {
		Telegram.WebApp.ready();
		this.statusManager.init();

		this.setupEventListeners();
		this.setupMainButton();

		this.apiManager = new ApiManager(
			options.apiUrl,
			options.userId,
			options.initDataHash,
			options.dataCheckString
		);
	}

	setupEventListeners() {
		$(".js-item-incr-btn").on("click", this.eIncrClicked.bind(this));
		$(".js-item-decr-btn").on("click", this.eDecrClicked.bind(this));
		$(".js-order-edit").on("click", this.eEditClicked.bind(this));
		$(".js-payment-edit").on("click", this.ePaymentClicked.bind(this));
		$(".js-status").on("click", this.eStatusClicked.bind(this));
		// $(".js-item-cash-btn").on("click", this.ePayCash.bind(this));
		// $(".js-item-card-btn").on("click", this.ePayCard.bind(this));

		// $(".js-order-comment-field").each((_, el) => {
		// 	autosize(el);
		// });

		document.addEventListener("keydown", (e) => {
			if (e.keyCode === 13) this.mainBtnClicked();
		});
	}

	setupMainButton() {
		Telegram.WebApp.MainButton.setParams({
			text_color: "#fff",
		}).onClick(this.mainBtnClicked.bind(this));
	}

	// event callbacks

	eIncrClicked(e) {
		e.preventDefault();
		item = new Item(e);
		this.incrClicked(item, 1);
	}

	eDecrClicked(e) {
		e.preventDefault();
		item = new Item(e);
		this.incrClicked(item, -1);
	}

	eEditClicked(e) {
		e.preventDefault();
		this.statusManager.toggleMode(Modes.INITIAL);
	}

	ePaymentClicked(e) {
		e.preventDefault();
		this.statusManager.toggleMode(Modes.ITEMS);
	}

	eStatusClicked() {
		this.hideStatus();
	}

	ePay(e) {
		this.order();
	}

	// view

	incrClicked(item, delta) {
		if (this.isLoading || this.isClosed) {
			return;
		}
		item.updateCount(delta);
		item.updateItem(item);
		this.updateTotalPrice();
	}

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
		this.statusManager.setTotalPrice(this.totalPrice);
		this.statusManager.setCanPay(this.canPay);
		this.statusManager.updateMainButton();
	}

	toggleLoading(loading) {
		this.isLoading = loading;
		this.updateTotalPrice();
		this.statusManager.toggleLoading(loading);
	}

	mainBtnClicked() {
		if (!this.canPay || this.isLoading || this.isClosed) {
			return;
		}
		console.log("clicked");
		switch (this.statusManager.modeOrder) {
			case Modes.ITEMS:
				this.statusManager.toggleMode(Modes.OVERVIEW);
				break;
			case Modes.OVERVIEW:
				this.order();
				break;
			case Modes.INITIAL:
				this.statusManager.toggleMode(Modes.ITEMS);
				break;
		}
	}

	showStatus(text) {
		clearTimeout(this.statusTo);
		$(".js-status").text(text).addClass("status--shown");
		if (!this.isClosed) {
			this.statusTo = setTimeout(() => {
				this.hideStatus();
			}, 2500);
		}
	}

	hideStatus() {
		clearTimeout(this.statusTo);
		$(".js-status").removeClass("status--shown");
	}

	// helpers

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
	}

	order() {
		const comment = $(".js-order-comment-field").val();
		const params = {
			order_data: this.getOrderData(),
			comment,
			price: this.totalPrice
		};
		this.toggleLoading(true);
		this.apiManager.request("order", params, (result) => {
			console.log(result);
			this.toggleLoading(false);
			if (result.ok) {
				Telegram.WebApp.close();
			}
			if (result.error) {
				this.showStatus(result.error);
			}
		});
	}

};

export default Cafe;
