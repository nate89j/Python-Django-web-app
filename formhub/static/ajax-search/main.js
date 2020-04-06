const user_input = $("#user-input")
const search_icon = $('#search-icon')
const projects_div = $('#replaceable-content')
var endpoint = window.location.pathname;
const delay_by_in_ms = 200
let scheduled_function = false

let ajax_call = function(endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            // fade out the artists_div, then:
            projects_div.fadeTo('fast', 0).promise().then(() => {
                // replace the HTML contents
                projects_div.html(response['html_from_view'])
                    // fade-in the div with new contents
                projects_div.fadeTo('fast', 1)
                    // stop animating search icon
            })
        })
}


user_input.on('keyup', function() {

    const request_parameters = {
        q: $(this).val() // value of user_input: the HTML element with ID user-input
    }

    // start animating the search icon with the CSS class)

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
});

$('.replaceable-content').click(function(e) { //button click class name is myDiv
    e.stopPropagation();
})

$(function() {
    $(document).click(function() {
        $('.replaceable-content').hide(); //hide the button

    });
});