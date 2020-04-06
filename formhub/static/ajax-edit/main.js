$(document).ready(function() {
    $("#FirstnameForm").submit(function(event) {
        $.ajax({
            type: "POST",
            url: endpoint,
            data: {
                'Firstname': $('#Firstname').val() // from form
                CSRF: getCSRFTokenValue()
            },
            success: function() {
                $('#Firstname').html("<h2>Contact Form Submitted!</h2>")
            }
        });
        return false;
    });
});

$(document).ready(function() {
    $("#LastnameForm").submit(function(event) {
        $.ajax({
            type: "POST",
            url: endpoint,
            data: {
                'Lastname': $('#Lastname').val() // from form
                CSRF: getCSRFTokenValue()
            },
            success: function() {
                $('#Lastname').html("<h2>Contact Form Submitted!</h2>")
            }
        });
        return false;
    });
});

$(document).ready(function() {
    $("#DepartmentForm").submit(function(event) {
        $.ajax({
            type: "POST",
            url: endpoint,
            data: {
                'Department': $('#Department').val() // from form
                CSRF: getCSRFTokenValue()
            },
            success: function() {
                $('#Department').html("<h2>Contact Form Submitted!</h2>")
            }
        });
        return false;
    });
});

$(document).ready(function() {
    $("#SkillsForm").submit(function(event) {
        $.ajax({
            type: "POST",
            url: endpoint,
            data: {
                'Skills': $('#Skills').val() // from form
                CSRF: getCSRFTokenValue()
            },
            success: function() {
                $('#Skills').html("<h2>Contact Form Submitted!</h2>")
            }
        });
        return false;
    });
});