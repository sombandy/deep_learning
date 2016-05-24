$(document).ready(function() {
    $('#colortable').DataTable( {
        "ajax": {
            "url": "data/colors.json",
            "dataSrc": function(json) {
                data = []
                for(var i = 0; i < json.length; i++) {
                    var row = {
                        "score" : json[i].score.toFixed(4),
                        "pixelFraction" : json[i].pixelFraction.toFixed(4),
                        "rgb" : rgbColor(json[i].color),
                        "hexcolor": rgbToHex(json[i].color),
                        "blank": ""
                    };

                    data.push(row);
                }
                return data;
            }
        },

        "order": [[ 0, "desc" ]],

        "columnDefs": [{
            "className": "dt-center",
            "targets": "_all"
            }],

        "columns": [
            { "data" : "score" },
            { "data" : "pixelFraction" },
            { "data" : "rgb" },
            { "data" : "blank" },
        ],

        "createdRow": function( row, data, dataIndex ) {
            $('td', row).eq(3).css('background-color', data['hexcolor']);
        },

        "searching": false,
        "paging":   false,
        "info":     false
    } );
} );

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