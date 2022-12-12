function parseDate(dateStr) {
	var parts = dateStr.split("/");
	var d1 = new Date(Number(parts[2]), Number(parts[1]) - 1, Number(parts[0]));
	return d1;
}

function parseDates(datesArray) {
    let result = [];
	for (let i = 0; i < datesArray.length; i++) {
        let dateElementParsed = parseDate(datesArray[i]);
        result.push(dateElementParsed);
    }
    return result;
}

function dateInRange(datesArray, dateString) {
	// expecting datesArray already sorted
	console.log(`dateInRange start with values: ${dateString} and ${datesArray}`);
	let rangeStart = datesArray[0];
	let rangeEnd = datesArray[datesArray.length-1];
	let inputDate = parseDate(dateString);
	console.log(`Parsed values: input: ${inputDate} | Range: [${rangeStart} | ${rangeEnd}]`);
	let result = inputDate >= rangeStart && inputDate <= rangeEnd;
	console.log(`Result: ${result}`);
	return result;
}

function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
    return false;
};