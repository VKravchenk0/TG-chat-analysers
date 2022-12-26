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

function getMonthStartsArray(datesArray) {
    let result = [];
    for (let i = 0; i < datesArray.length; i++) {
        let date = datesArray[i];
        let firstDayOfMonth = new Date(date.getFullYear(), date.getMonth(), 1);
        result.push(firstDayOfMonth);
    }
    return result;
}