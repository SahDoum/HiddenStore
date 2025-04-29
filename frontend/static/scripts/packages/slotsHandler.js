// slotsHandler.js

import $ from 'jquery';
import SlotElement from './slotElement';

class SlotsHandler {
	constructor(busyData) {
		this.busyData = busyData;
		this.selectedTime = null;
		this.selectedSlot = new SlotElement('00:00', '00:00', false);
	}

	showSlots(date) {
		this.selectedSlot = new SlotElement('00:00', '00:00', false);
		this.date = date

		$('#selectedDate').text(date);
		const slotsContainer = $('#slots');
		slotsContainer.empty();

		const timeSlots = this.generateTimeSlots(); // Указываем диапазон времени
		timeSlots.forEach(slot => {
			const slotElement = this.createTimeSlotElement(slot, date);
			slotsContainer.append(slotElement);
		});

		this.busyData.forEach((busySlot) => {
			if (busySlot.date != date) return;

			const busySlotElement = new SlotElement(
				busySlot.start_time,
				busySlot.end_time,
				true,
			);
			slotsContainer.append(busySlotElement.getElement());
		});

		slotsContainer.append(this.selectedSlot.getElement());

		$('#slotsContainer').addClass('slots--active');
	}

	generateTimeSlots() {
		const slots = [];
		let currentTime = new Date(`1970-01-01T08:00:00`);
		const endTimeDate = new Date(`1970-01-01T18:00:00`);

		while (currentTime <= endTimeDate) {
			slots.push(currentTime.toString());
			console.log(currentTime);
			currentTime.setMinutes(currentTime.getMinutes() + 30);
		}

		return slots;
	}

	createTimeSlotElement(time_string, date) {
		let time = new Date(time_string);
		const isBusy = this.isSlotBusy(date, time);

		const formattedTime = time.toTimeString().split(' ')[0].slice(0, 5);
		const slotElement = `<div class="slots__slot" data-time="${time}">${formattedTime}</div>`;

		return $(slotElement).on('click', (e) => {
			if (isBusy) return;
			this.updateSelectedTime(time);
			console.log('Selected time:', this.selectedTime);
		});
	}

	// updateSelectedTime(time) {
	// 	this.selectedTime = time;
	// 	let endTime = new Date(this.selectedTime.getTime() + 60 * 60 * 1000);
	// 	this.selectedSlot.update(this.selectedTime, endTime);
	// }
	updateSelectedTime(time) {
		const slotDuration = 60 * 60 * 1000;
		let proposedEndTime = new Date(time.getTime() + slotDuration);

		if (this.isSlotOverlapping(time, proposedEndTime)) {
			const overlappingSlot = this.getOverlappingSlot(time, proposedEndTime);
			const busyEnd = new Date(`1970-01-01T${overlappingSlot.end_time}:00`);

			let shiftedTime = new Date(busyEnd.getTime());
			let shiftedEndTime = new Date(shiftedTime.getTime() + slotDuration);

			if (!this.isSlotOverlapping(shiftedTime, shiftedEndTime)) {
				this.selectedTime = shiftedTime;
				this.selectedSlot.update(this.selectedTime, shiftedEndTime);
				console.log('Slot shifted to:', this.selectedTime, ' - ', shiftedEndTime);
			} else {
				console.log('No available slot for shifting.');
			}
		} else {
			this.selectedTime = time;
			this.selectedSlot.update(this.selectedTime, proposedEndTime);
			console.log('Selected time:', this.selectedTime, ' - ', proposedEndTime);
		}
	}

	isSlotOverlapping(startTime, endTime) {
		return this.busyData.some(busySlot => {
			if (busySlot.date != this.date) return false;
			const busyStart = new Date(`1970-01-01T${busySlot.start_time}:00`);
			const busyEnd = new Date(`1970-01-01T${busySlot.end_time}:00`);
			return (startTime < busyEnd && endTime > busyStart);
		});
	}

	// Метод для получения пересекающегося слота (если есть)
	getOverlappingSlot(startTime, endTime) {
		return this.busyData.find(busySlot => {
			if (busySlot.date != this.date) return false;
			const busyStart = new Date(`1970-01-01T${busySlot.start_time}:00`);
			const busyEnd = new Date(`1970-01-01T${busySlot.end_time}:00`);
			return (startTime < busyEnd && endTime > busyStart);
		});
	}


	isSlotBusy(date, time) {
		return this.busyData.some(busySlot =>
			busySlot.date === date &&
			busySlot.start_time <= time &&
			busySlot.end_time > time
		);
	}

}

export default SlotsHandler;
