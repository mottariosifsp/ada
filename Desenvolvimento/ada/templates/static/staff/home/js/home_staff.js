var lang = document.currentScript.getAttribute("data-lang");

function redirect(url){
    window.location.href = url;
}

function validateFormFields(value) {
    var allFieldsFilled = true;
    var missingFields = [];

    if(value == 1) {
        $("input#title-input, input#comment-input, input#start-input, input#end-input, textarea[required]").each(function() {
            var fieldValue = $(this).val();
            var fieldLabel = $("label[for='" + $(this).attr("id") + "']").text().trim();
    
            if (!fieldValue) {
                allFieldsFilled = false;
                missingFields.push(fieldLabel);                                   
            }
            
        });
    
        $("select[required]").each(function() {
            var fieldValue = $(this).val();
            var fieldLabel = $("label[for='" + $(this).attr("id") + "']").text().trim();
    
            if (fieldValue == null) {
                allFieldsFilled = false;
                missingFields.push(fieldLabel);                                   
            }
            
        });
    } else {
        $("input#link-input").each(function() {
            var fieldValue = $(this).val();
            var fieldLabel = $("label[for='" + $(this).attr("id") + "']").text().trim();
    
            if (!fieldValue) {
                allFieldsFilled = false;
                missingFields.push(fieldLabel);                                   
            }
            
        });
    }

    

    return {
        isValid: allFieldsFilled,
        missingFields: missingFields
    };
}

$(document).ready(function() {
    $('#add-alert-button').click(function() {        
        let csrftoken = get_cookie("csrftoken");
        var validation = validateFormFields(1);

        if (!validation.isValid) {
            var missingFieldsMessage = "Preencha os seguintes campos obrigatórios\n" + validation.missingFields.join(', ');
            $('#error-message-modal').text(missingFieldsMessage);
            $('#error-alert-modal').show();
            return false;
        }

        var formData = $("#add-alert-form").serialize();
        if(lang) {
            url = "/" + lang + "/staff/";
        } else {
            url = "/staff/";
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            headers: {
                "X-CSRFToken": csrftoken,
            },
            success: function(response) {
                $('#add-alert-form').trigger("reset");
                $('#error-alert-modal').hide();
            },
            error: function(error) {
                $('#error-message-modal').text('Erro ao adicionar alerta');
                $('#error-alert-modal').show();
            }
        });
    });

    $('#add-link-button').click(function() {        
        let csrftoken = get_cookie("csrftoken");
        var validation = validateFormFields(2);

        if (!validation.isValid) {
            var missingFieldsMessage = "Preencha os seguintes campos obrigatórios\n" + validation.missingFields.join(', ');
            $('#error-message-link-modal').text(missingFieldsMessage);
            $('#error-link-modal').show();
            return false;
        }

        var formData = $("#add-link-form").serialize();
        if(lang) {
            url = "/" + lang + "/staff/";
        } else {
            url = "/staff/";
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            headers: {
                "X-CSRFToken": csrftoken,
            },
            success: function(response) {
                $('#add-link-form').trigger("reset");
                $('#error-link-modal').hide();
            },
            error: function(error) {
                $('#error-message-link-modal').text('Erro ao adicionar alerta');
                $('#error-link-modal').show();
            }
        });
    });
});

function get_cookie(name) {
    var cookie_value = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookie_value = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookie_value;
}