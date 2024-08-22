import $ from 'jquery';
import { formatPrice } from './utils';


export class Item {
	constructor(event) {
		this.itemEl = $(event.currentTarget).closest(".js-item");;
	}

	updateCount(delta) {
		let count = +this.itemEl.data("item-count") || 0;
		count += delta;
		if (count < 0) {
			count = 0;
		}
		this.itemEl.data("item-count", count);
	}

	getOrderItem() {
		const id = this.itemEl.data("item-id");
		return $(".js-order-item").filter(function () {
			return $(this).data("item-id") === id;
		});
	}

	updateItem(delta) {
		itemEl = this.itemEl;

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

		const orderItemEl = item.getOrderItem();
		const orderCounterEl = $(".js-order-item__counter", orderItemEl);
		orderCounterEl.text(count ? count : 1);
		orderItemEl.toggleClass("list-item--selected", count > 0);
		const orderPriceEl = $(".js-order-item__price", orderItemEl);
		const itemPrice = count * price;
		orderPriceEl.text(formatPrice(itemPrice));
	}
}
