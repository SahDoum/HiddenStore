// calendarDay.js

class CalendarDay {
	constructor(day, formattedDate, isAvailable) {
		this.day = day;
		this.formattedDate = formattedDate;
		this.isAvailable = isAvailable;
	}

	// Generates the HTML for a calendar day
	getHtml() {
		if (this.isAvailable) {
			return `
				<div class="calendar__day ripple-wrapper" data-date="${this.formattedDate}">${this.day}
					<span class="ripple-mask"><span class="ripple"></span></span>
				</div>
				`;
		} else {
			return `<div class="calendar__day calendar__day--disabled">${this.day}</div>`;
		}
	}
}

export default CalendarDay;
