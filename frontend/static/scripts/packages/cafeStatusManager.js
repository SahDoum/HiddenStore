import $ from 'jquery';
import autosize from 'autosize';

import './redraw';
import { formatPrice } from './utils';


// Define the enumeration for modes
export const Modes = {
	INITIAL: 0,
	ITEMS: 1,
	DELIVERY: 2,
	OVERVIEW: 3,
};

/// 


const ModePages = {
	[Modes.INITIAL]: $(".mode--items"),
	[Modes.ITEMS]: $(".mode--order-overview"),
	[Modes.DELIVERY]: $(".mode--delivery"),
	[Modes.OVERVIEW]: $(".mode--payment"),
};

export class StatusManager {
	constructor() {
		this.modeOrder = -1; // Default mode
		this.status_manager = $("#mode-manager");
		this.isLoading = false;
		this.totalPrice = 0;

		this.mainButton = Telegram.WebApp.MainButton;

	}

	init() {
		this.status_manager.show();
		this.mainButton.setParams({
			text_color: "#fff",
		});

		console.log('init()')
		var fields = $(".js-order-comment-field");
		autosize(fields);

		// fields.each(function () {
		// 	autosize(this);
		// }).on('autosize:resized', function () {
		// 	console.log('textarea height updated');
		// });

	}

	setTotalPrice(price) {
		this.totalPrice = price;
	}

	toggleLoading(loading) {
		this.isLoading = loading;
		this.status_manager.toggleClass("loading", !!this.isLoading);
		this.updateMainButton();
	}

	toggleMode(modeOrder) {
		console.log("Change mode: " + modeOrder);

		ModePages[modeOrder].addClass("mode--active");//.redraw();

		if (this.modeOrder != -1) {
			ModePages[this.modeOrder].removeClass("mode--active");
			ModePages[this.modeOrder].css("maxHeight", "0");//.redraw();
		}
		// ModePages[modeOrder].css("maxHeight", "none");
		// const height = ModePages[modeOrder].scrollHeight;
		const height = $(".mode--active > .page").height();
		ModePages[modeOrder].css("maxHeight", height);//.redraw();
		this.modeOrder = modeOrder;

		switch (modeOrder) {
			case Modes.INITIAL:
				break;
			case Modes.ITEMS:
				Telegram.WebApp.expand();
				break;
			case Modes.OVERVIEW:
				break;
		}

		this.updateMainButton();
	}

	updateMainButton() {
		if (this.modeOrder == 0) {
			this.mainButton.setParams({
				is_visible: (this.totalPrice > 0),
				text: "ЗАКАЗ",
				color: "#31b545",
			}).hideProgress();
			return;
		}

		if (this.isLoading) {
			this.mainButton.setParams({
				is_visible: true,
				color: "#65c36d",
			}).showProgress();
			return;
		}

		this.mainButton.setParams({
			is_visible: (this.totalPrice > 0),
			text: `PAY ${formatPrice(this.totalPrice)}`,
			color: "#31b545",
		}).hideProgress();


	}
}

