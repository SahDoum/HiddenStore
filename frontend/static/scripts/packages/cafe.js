// cafe.js

import $ from 'jquery';
import { StatusManager, Modes } from './cafeStatusManager'
import { Item } from './cafeItem'
import { ApiManager } from './apiManager'


class Cafe {
	constructor() {
		this.totalPrice = 0;
		this.isLoading = false;
		this.isClosed = false;
		this.statusManager = new StatusManager();
	}

	// setup

	init(options) {
		console.log("init");
		Telegram.WebApp.ready();
		this.statusManager.init();
		this.statusManager.toggleMode(Modes.INITIAL);
		this.setupEventListeners();

		this.apiManager = new ApiManager(
			options.apiUrl,
			options.userId,
			options.initDataHash,
			options.dataCheckString
		);
	}

	setupEventListeners() {
		Telegram.WebApp.MainButton.onClick(this.mainBtnClicked.bind(this));

		$(".js-item-incr-btn").on("click", this.eIncrClicked.bind(this));
		$(".js-item-decr-btn").on("click", this.eDecrClicked.bind(this));
		$(".js-order-edit").on("click", this.eEditClicked.bind(this));
		$(".js-payment-edit").on("click", this.ePaymentClicked.bind(this));
		$(".js-status").on("click", this.eStatusClicked.bind(this));

		$(".js-delivery-edit").on("click", this.eDeliveryEditClicked.bind(this));
		// $(".js-order-comment-field").each((_, el) => {
		// 	autosize(el);
		// });

		document.addEventListener("keydown", (e) => {
			if (e.keyCode === 13) this.mainBtnClicked();
		});
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

	eDeliveryEditClicked(e) {
		e.preventDefault();
		this.statusManager.toggleMode(Modes.ITEMS);
	}

	ePaymentClicked(e) {
		e.preventDefault();
		this.statusManager.toggleMode(Modes.DELIVERY);
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
		this.totalPrice = totalPrice;
		this.statusManager.setTotalPrice(this.totalPrice);
		this.statusManager.updateMainButton();
	}

	toggleLoading(loading) {
		this.isLoading = loading;
		this.updateTotalPrice();
		this.statusManager.toggleLoading(loading);
	}

	mainBtnClicked() {
		if (this.totalPrice <= 0 || this.isLoading || this.isClosed) {
			return;
		}

		switch (this.statusManager.modeOrder) {
			case Modes.INITIAL:
				this.statusManager.toggleMode(Modes.ITEMS);
				break;
			case Modes.ITEMS:
				this.statusManager.toggleMode(Modes.DELIVERY);
				break;
			case Modes.DELIVERY:
				if (!this.validatePickupPoint()) {
					this.showStatus("Выбери пункт доставки");
					break;
				}
				this.statusManager.toggleMode(Modes.OVERVIEW);
				break;
			case Modes.OVERVIEW:
				if (!this.validatePayment()) {
					this.showStatus("Выбери тип оплаты");
					break;
				}
				this.order();
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
		return orderData;
	}

	order() {
		const comment = $(".js-order-comment-field").val();
		const params = {
			items: this.getOrderData(),
			comment,
			price: this.totalPrice,
			pickup_point_id: this.getPickupPoint(),
			payment_method: this.getPayment(),
		};
		this.toggleLoading(true);
		this.apiManager.request("order", params, (result) => {
			console.log(result);
			this.toggleLoading(false);
			if (result.error) {
				this.showStatus(result.error);
			}
			else {
				Telegram.WebApp.close();
			}
		});
	}

	// form validators and getters

	validatePickupPoint() {
		return $('input[name="pickup-group"]:checked').length > 0;
	}

	getPickupPoint() {
		return $('input[name="pickup-group"]:checked').attr('id');
	}

	validatePayment() {
		return $('input[name="payment-group"]:checked').length > 0;
	}

	getPayment() {
		return $('input[name="payment-group"]:checked').attr('id');
	}

};

export default Cafe;
