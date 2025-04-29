// slotElement.js

import $ from 'jquery';

class SlotElement {
	constructor(startTime_str, endTime_str, isBusy) {
		this.start_time_str = startTime_str
		this.end_time_str = endTime_str
		this.time = new Date(`1970-01-01T${startTime_str}:00`);
		this.endTime = new Date(`1970-01-01T${endTime_str}:00`);
		this.isBusy = isBusy;
		this.element = null;
	}

	getElement() {
		const element_class = this.isBusy ? 'slots__selected--busy' : 'slots__selected--select';
		const slotElement = `
			<div class="slots__selected ${element_class}">
				${this.start_time_str} - ${this.end_time_str}
			</div>
			`;

		this.element = $(slotElement).css({
			top: this.getSlotPosition(),
			height: this.getSlotHeight(),
		});


		return this.element;
	}

	update(startTime, endTime) {
		this.time = startTime;
		this.endTime = endTime;

		this.start_time_str = startTime.toTimeString().split(' ')[0].slice(0, 5);
		this.end_time_str = endTime.toTimeString().split(' ')[0].slice(0, 5);

		this.element.css({
			top: this.getSlotPosition(),
			height: this.getSlotHeight(),
		});

		this.element.text(`${this.start_time_str} - ${this.end_time_str}`);
	}

	getSlotPosition() {
		if (!this.time) return 0;
		const baseTime = new Date(`1970-01-01T08:00:00`);
		const ratio = 2 * (this.time.getHours() - baseTime.getHours() + this.time.getMinutes() / 60);
		return ratio * $('.slots__slot').outerHeight();
	}

	getSlotHeight() {
		if (!this.time) return 0;
		duration = this.endTime - this.time;
		console.log((duration / 3600 / 1000 * 2) * $('.slots__slot').outerHeight());
		return (duration / 3600 / 1000 * 2) * $('.slots__slot').outerHeight();
	}
}

export default SlotElement;
