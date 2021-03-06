//modular bug fix for negative numbers
function mod(n, m) {
    return ((n % m) + m) % m;
}

// return calendar p months prior
function past_month(p) {
    
    var cal;    // return value
    var DAYS_OF_WEEK = 7;    // "constant" for number of days in a week
    var DAYS_OF_MONTH = 31;    // "constant" for number of days in a month
    var day_of_week = new Array('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
    var month_of_year = new Array('January','February','March',
				  'April',  'May',     'June',
				  'July',   'August',  'September',
				  'October','November','December');

    //  DECLARE AND INITIALIZE VARIABLES
    var Calendar = new Date();

    var year = Calendar.getFullYear();     // Returns year
    var month = Calendar.getMonth();    // Returns month (0-11)
    var today = Calendar.getDate();    // Returns day (1-31)
    var weekday = Calendar.getDay();    // Returns day (1-31)

    year -= Math.floor(p/12)
    if (p % 12 > month) {
        year--;
    }
    month = mod(month - p, 12);

    Calendar.setDate(1);    // Start the calendar day at '1'
    Calendar.setMonth(month);    // Start the calendar month at now
    Calendar.setYear(year);

    /* VARIABLES FOR FORMATTING
    NOTE: You can format the 'BORDER', 'BGCOLOR', 'CELLPADDING', 'BORDERCOLOR'
          tags to customize your caledanr's look. */
    var TR_start = '<TR>';
    var TR_end = '</TR>';
    var TD_start = '<TD WIDTH="70"><CENTER>';
    var TD_end = '</CENTER></TD>';

    /* BEGIN CODE FOR CALENDAR
    NOTE: You can format the 'BORDER', 'BGCOLOR', 'CELLPADDING', 'BORDERCOLOR'
    tags to customize your calendar's look.*/

    cal =  '<TABLE ALIGN="center" BORDER=1 CELLSPACING=0 CELLPADDING=10 BORDERCOLOR=BBBBBB><TR><TD>';
    cal += '<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=10>' + TR_start;
    cal += '<TD COLSPAN="' + DAYS_OF_WEEK + '" BGCOLOR="#EFEFEF"><CENTER><B>';
    cal += month_of_year[month]  + '   ' + year + '</B>' + TD_end + TR_end;
    cal += TR_start;
    
    // LOOPS FOR EACH DAY OF WEEK
    for(index=0; index < DAYS_OF_WEEK; index++) {
        cal += TD_start + day_of_week[index] + TD_end;
    }

    cal += TD_end + TR_end;
    cal += TR_start;

    // FILL IN BLANK GAPS UNTIL TODAY'S DAY
    for(index=0; index < Calendar.getDay(); index++)
        cal += TD_start + '  ' + TD_end;

    // LOOPS FOR EACH DAY IN CALENDAR
    for(index=0; index < DAYS_OF_MONTH; index++) {
        if( Calendar.getDate() > index ) {
            // RETURNS THE NEXT DAY TO PRINT
            week_day = Calendar.getDay();

            // START NEW ROW FOR FIRST DAY OF WEEK
            if(week_day == 0) cal += TR_start;

            if(week_day != DAYS_OF_WEEK) {
                // SET VARIABLE INSIDE LOOP FOR INCREMENTING PURPOSES
                var day  = Calendar.getDate();
                cal += TD_start +'<a href="logs/'+ Calendar.getFullYear() +'-'
                    + ('0'+(Calendar.getMonth()+1)).slice(-2) +'-'
                    + ('0'+day).slice(-2) +'.svg">'+ day +'</a>'+ TD_end;
            }
            // END ROW FOR LAST DAY OF WEEK
            else cal += TR_end;
        }
        // INCREMENTS UNTIL END OF THE MONTH
        Calendar.setDate(Calendar.getDate()+1);
    }
    cal += '</TD></TR></TABLE></TABLE>';
    return cal;
}
