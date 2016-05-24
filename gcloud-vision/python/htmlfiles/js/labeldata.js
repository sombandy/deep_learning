$(document).ready(function() {
    $('#labeltable').DataTable( {
        "ajax": {
            "url": "data/labels.json",
            "dataSrc": ""
        },
        
        "order": [[ 0, "desc" ]],

        "columns": [
            { "data" : "score" },
            { "data" : "mid" },
            { "data" : "description" }
        ],

        "searching": false,
        "paging":   false,
        "info":     false
    } );
} );