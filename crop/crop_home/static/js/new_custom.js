$(document).ready(function() {
    $(".zoom").hover(function() {

        $(this).addClass('transition');
    }, function() {

        $(this).removeClass('transition');
    });

    $('#year').each(function() {
        var year = (new Date()).getFullYear();
        var current = year;
        year -= 10;
        for (var i = 0; i < 16; i++) {
        if ((year+i) == current)
            $(this).append('<option selected value="' + (year + i) + '">' + (year + i) + '</option>');
        else
            $(this).append('<option value="' + (year + i) + '">' + (year + i) + '</option>');
        }
    })
    // Start prediction serach
    $('#prediction_area').hide()
    $('#searching_div').hide()
    $('#img_show').hide()
    $('#reduce_button').hide()
    $('#search_button').on( 'click', function () {
        event.preventDefault()
        $('#img_show').hide()
        $('#reduce_button').hide()
        $('#prediction_area').hide()
        $('#searching_div').show()
        console.log('btn clicked')
        var district = $("#district").val();
        var year = $("#year").val();
        var season = $('#season').val();
        console.log(season + '' + year + '' + district)

        jQuery.ajax({
            url: '/getPrediction/',
            data: {
                'district': district,
                'year' : year,
                'season' : season
            },
            type : "GET",
            dataType : "json",
            success:function(data)
            {
                console.log(data)
                $('#searching_div').hide()
                $('#prediction_area').delay(5000).show()
                $('#prediction_percent').text(data.prediction)
                $('#suggested_crop').text(data.suggestion)
                // Progress bar start
                progressVal = data.prediction
                totalPercentageVal = 100
                var strokeVal = (4.64 * 100) /  totalPercentageVal;
                var x = document.querySelector('.progress-circle-prog');
                x.style.strokeDasharray = progressVal * (strokeVal) + ' 999';
                var el = document.querySelector('.progress-text');
                var from = $('.progress-text').data('progress');
                $('.progress-text').data('progress', progressVal);
                var start = new Date().getTime();
                $('#n_text').text(data.N + '%')
                $('#p_text').text(data.P + '%')
                $('#k_text').text(data.K + '%')
                $('#n_div').attr("style", "width:"+ data.N + "%");
                $('#p_div').attr("style", "width:"+ data.P + "%");
                $('#k_div').attr("style", "width:"+ data.K + "%");


                setTimeout(function() {
                    var now = (new Date().getTime()) - start;
                    var progress = now / 700;
                    el.innerHTML = progressVal / totalPercentageVal * 100 + '%';
                    if (progress < 1) setTimeout(arguments.callee, 10);
                }, 10);
                // Progress bar end
            }, error: function(XMLHttpRequest, textStatus, errorThrown) {
                $('#searching_div').hide()
                alert("Status 404: No data found for the given input");
            }
        });
    });
    // End prediction serach
    $('#hide_button').on( 'click', function () {
        event.preventDefault()
        console.log('hide btn clicked')
        progressVal = 0
        totalPercentageVal = 100
        var strokeVal = (4.64 * 100) /  totalPercentageVal;
        var x = document.querySelector('.progress-circle-prog');
        x.style.strokeDasharray = progressVal * (strokeVal) + ' 999';
        var el = document.querySelector('.progress-text');
        var from = $('.progress-text').data('progress');
        $('.progress-text').data('progress', progressVal);
        var start = new Date().getTime();

        setTimeout(function() {
            var now = (new Date().getTime()) - start;
            var progress = now / 700;
            el.innerHTML = progressVal / totalPercentageVal * 100 + '%';
            if (progress < 1) setTimeout(arguments.callee, 10);
        }, 10);
        $('#prediction_area').hide()
    });
    // End of Hide
    $('#expand_button').on( 'click', function () {
        $('#img_show').show()
        $('#expand_button').hide()
        $('#reduce_button').show()
    });

    $('#reduce_button').on( 'click', function () {
        $('#img_show').hide()
        $('#reduce_button').hide()
        $('#expand_button').show()
    });

});