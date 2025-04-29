// calendar.js

import $ from 'jquery';
import CalendarDay from './calendarDay';
import SlotsHandler from './slotsHandler';

class Calendar {
	constructor(busyData) {
		this.busyData = busyData;
		this.selectedDate = null;
		this.selectedTime = null;
		this.slotsHandler = new SlotsHandler(this.busyData);
		this.init();
	}

	init() {
		this.generateCalendar();
		this.setupEventListeners();
	}

	generateCalendar() {
		const calendar = $('#calendar');
		calendar.empty();

		const today = new Date();
		const currentDayOfWeek = today.getDay() || 7;
		const startDate = new Date(today);

		startDate.setDate(today.getDate());

		const daysToShow = 14;

		for (let i = 1; i < currentDayOfWeek; i++) {
			const calendarDay = new CalendarDay("", "", false);
			calendar.append(calendarDay.getHtml());
		}

		for (let i = 0; i < daysToShow; i++) {
			const currentDate = new Date(startDate);
			currentDate.setDate(startDate.getDate() + i);

			const formattedDate = currentDate.toISOString().split('T')[0];
			const isAvailable = true; // !!this.busyData[formattedDate];

			const calendarDay = new CalendarDay(currentDate.getDate(), formattedDate, isAvailable);
			calendar.append(calendarDay.getHtml());
		}

		for (let i = 0; i < 8 - currentDayOfWeek; i++) {
			const calendarDay = new CalendarDay("", "", false);
			calendar.append(calendarDay.getHtml());
		}
	}

	setupEventListeners() {
		$(document).on('click', '.calendar__day', (e) => {
			const date = $(e.currentTarget).data('date');

			$('.calendar__day--selected').removeClass('calendar__day--selected');
			$(e.currentTarget).addClass('calendar__day--selected');

			this.selectedDate = date;
			this.slotsHandler.showSlots(date);
		});

		this.slotsHandler.setupEventListeners();
	}
}

export default Calendar;
