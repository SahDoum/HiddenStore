// jquery.redraw.js

import $ from 'jquery';

$.fn.redraw = function () {
	return this.map(function () {
		this.offsetTop; // Trigger a reflow
		return this;
	});
};
