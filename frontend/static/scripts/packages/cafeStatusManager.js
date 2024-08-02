import $ from 'jquery';
import './redraw';
import { formatPrice } from './utils';


// Define the enumeration for modes
export const Modes = {
	INITIAL: 0,
	OVERVIEW: 2,
	ITEMS: 1,
};

export class StatusManager {
	constructor() {
		this.modeOrder = Modes.INITIAL; // Default mode
		this.status_manager = $("#mode-manager");
		this.isLoading = false;
		this.canPay = false;
		this.totalPrice = 0;
	}

	init() {
		this.show();
	}

	setTotalPrice(price) {
		this.totalPrice = price;
	}

	setCanPay(canPay) {
		this.canPay = canPay;
	}

	show() {
		this.status_manager.show();
	}

	toggleLoading(loading) {
		this.isLoading = loading;
		this.status_manager.toggleClass("loading", !!this.isLoading);
		this.updateMainButton();

	}

	toggleMode(modeOrder) {
		this.modeOrder = modeOrder;

		console.log("Change mode: " + this.modeOrder);

		if (modeOrder === Modes.OVERVIEW) {
			const height = $(".page--order-overview").height();
			this.status_manager.addClass("mode--payment");
			$(".page--order-overview").css("maxHeight", height).redraw();
			$(".page--payment").show();
		} else if (modeOrder === Modes.ITEMS) {
			const height = $(".page--items").height();
			this.status_manager.removeClass("mode--payment");
			$(".page--order-overview").show();
			if (height) $(".page--items").css("maxHeight", height).redraw();
			this.status_manager.addClass("mode--order");
			// $(".js-order-comment-field").each(function () {
			//     autosize.update(this);
			// });
			Telegram.WebApp.expand();
		} else if (modeOrder === Modes.INITIAL) {
			this.status_manager.removeClass("mode--order");
		}

		this.updateMainButton();
	}


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
					text: `PAY ${formatPrice(this.totalPrice)}`,
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
	}
}

