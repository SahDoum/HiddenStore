export function formatNumber(number, decimals, decPoint, thousandsSep) {
	const n = !isFinite(+number) ? 0 : +number;
	const prec = !isFinite(+decimals) ? 0 : Math.abs(decimals);
	const sep = thousandsSep || ",";
	const dec = decPoint || ".";
	let s = "";
	const toFixedFix = (n, prec) => {
		if (String(n).indexOf("e") === -1) {
			return +(Math.round(n + "e+" + prec) + "e-" + prec);
		} else {
			const arr = String(n).split("e");
			const sig = +arr[1] + prec > 0 ? "+" : "";
			return (+(
				Math.round(+arr[0] + "e" + sig + (+arr[1] + prec)) +
				"e-" +
				prec
			)).toFixed(prec);
		}
	};
	s = (prec ? toFixedFix(n, prec).toString() : String(Math.round(n))).split(".");
	if (s[0].length > 3) {
		s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
	}
	if ((s[1] || "").length < prec) {
		s[1] = s[1] || "";
		s[1] += new Array(prec - s[1].length + 1).join("0");
	}
	return s.join(dec);
}


export function formatPrice(price) {
	return `₾${formatNumber(price, 2, ".", ",")}`;
}
