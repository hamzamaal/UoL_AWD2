jQuery(document).ready(function ($) {
    "use strict";

    /**
     * Display or clear the validation message for a field.
     *
     * @param {jQuery} field - Input or textarea element.
     * @param {boolean} hasError - Whether the field has failed validation.
     * @param {string} message - Message to display when invalid.
     */
    function showValidation(field, hasError, message) {
        const validationBox = field.next(".validation");

        if (!validationBox.length) {
            return;
        }

        if (hasError) {
            validationBox.html(message).show("blind");
        } else {
            validationBox.html("").hide("blind");
        }
    }

    /**
     * Validate a single field using its data-rule and data-msg attributes.
     *
     * Supported rules:
     * - required
     * - minlen:x
     * - email
     * - checked
     * - regexp:pattern
     *
     * @param {jQuery} field - Input or textarea element.
     * @returns {boolean} True if valid, otherwise false.
     */
    function validateField(field) {
        const emailExp = /^[^\s()<>@,;:\/]+@\w[\w.-]+\.[a-z]{2,}$/i;
        let rule = field.attr("data-rule");

        if (typeof rule === "undefined" || rule === "") {
            showValidation(field, false, "");
            return true;
        }

        let ruleName = rule;
        let ruleValue = "";
        const pos = rule.indexOf(":");

        if (pos >= 0) {
            ruleName = rule.substring(0, pos);
            ruleValue = rule.substring(pos + 1);
        }

        let hasError = false;
        const value = $.trim(field.val());
        const message = field.attr("data-msg") || "Wrong input";

        switch (ruleName) {
            case "required":
                hasError = value === "";
                break;

            case "minlen":
                hasError = value.length < parseInt(ruleValue, 10);
                break;

            case "email":
                hasError = !emailExp.test(value);
                break;

            case "checked":
                hasError = !field.is(":checked");
                break;

            case "regexp":
                hasError = !(new RegExp(ruleValue).test(value));
                break;

            default:
                hasError = false;
                break;
        }

        showValidation(field, hasError, message);
        return !hasError;
    }

    /**
     * Validate all relevant fields in the form.
     *
     * @param {jQuery} form - The submitted form.
     * @returns {boolean} True if all fields are valid.
     */
    function validateForm(form) {
        let isValid = true;

        form.find(".form-group input, .form-group textarea, .form-group select").each(function () {
            const field = $(this);
            if (!validateField(field)) {
                isValid = false;
            }
        });

        return isValid;
    }

    /**
     * Reset all form fields and validation messages.
     *
     * @param {jQuery} form - The form to reset.
     */
    function resetForm(form) {
        form.find("input[type='text'], input[type='email'], input[type='tel'], textarea").val("");
        form.find("input[type='checkbox'], input[type='radio']").prop("checked", false);
        form.find("select").prop("selectedIndex", 0);
        form.find(".validation").html("").hide();
    }

    $("form.contactForm").on("submit", function (event) {
        event.preventDefault();

        const form = $(this);
        const action = form.attr("action") || "contactform/contactform.php";

        $("#sendmessage").removeClass("show");
        $("#errormessage").removeClass("show").html("");

        if (!validateForm(form)) {
            return false;
        }

        $.ajax({
            type: "POST",
            url: action,
            data: form.serialize(),
            dataType: "text",
            success: function (response) {
                const msg = $.trim(response);

                if (msg === "OK") {
                    $("#sendmessage").addClass("show");
                    $("#errormessage").removeClass("show").html("");
                    resetForm(form);
                } else {
                    $("#sendmessage").removeClass("show");
                    $("#errormessage").addClass("show").html(msg);
                }
            },
            error: function (xhr, status, error) {
                $("#sendmessage").removeClass("show");
                $("#errormessage")
                    .addClass("show")
                    .html("An unexpected error occurred. Please try again later.");
                console.error("Contact form AJAX error:", status, error);
            }
        });

        return false;
    });
});