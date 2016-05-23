$.getJSON( "colordata.json", function( data ) {
	for(i = 0; i < data.length; i++) {
		var rgbcolor = rgbColor(data[i].color);
		var hexcolor = rgbToHex(data[i].color);

		var tr = $("<tr/>")
		tr.append("<td>" + data[i].score.toFixed(4) + "</td>");
		tr.append("<td>" + data[i].pixelFraction .toFixed(4) + "</td>");
		tr.append("<td>" + rgbcolor + "</td>");
		tr.append("<td bgcolor='" + hexcolor +"' width='50px'></td>");
		$('#colordata tbody').append(tr);
	}
});

function rgbColor(color) {
	var r = color.red.toString();
	var g = color.green.toString();
	var b = color.blue.toString();
	return [r, g, b].join(", ")
}

function rgbToHex(color) {
	var r = color.red;
	var g = color.green;
	var b = color.blue;

	var rgb = b | (g << 8) | (r << 16);
	return '#' + rgb.toString(16);
}
