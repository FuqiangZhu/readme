$(document).ready(function(){
    $('a#clickCaptcha').click(function() {
       $("#captcha_img").attr("src", "/flow/auth/captcha?d="+Math.random());
    });
    $('#start_time_picker').datetimepicker(
    {
            format: 'YYYY-MM-DD HH:mm:ss'
     });
    $('#end_time_picker').datetimepicker(
    {
        format: 'YYYY-MM-DD HH:mm:ss'
    });
    $('#date_picker').datetimepicker(
    {
        format: 'YYYY-MM-DD'
    });
});