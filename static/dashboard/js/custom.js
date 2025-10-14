$(function() {
   $("#datepicker").datepicker({
        dateFormat: "dd/mm/yy",
        changeMonth: true,
        maxDate: 0
    });

    // Set current date as default
    $("#datepicker").datepicker("setDate", new Date());
});