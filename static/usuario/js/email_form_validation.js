/*
 *  Validacion para el usuario_modificar_email.html -> Usuario Change Email Form
 */

var FormEmail = function() {
    var initValidationEmail = function(){
        jQuery('.js-validation-reminder').validate({
            errorElement: 'div',
            errorClass: 'help-block text-right',
            errorPlacement: function(error, e) {
                jQuery(e).parents('.form-group .form-material').append(error);
                $("input#flag").val('F');
                $("input.guardar").attr("disabled", true);
            },
            highlight: function(e) {
                jQuery(e).closest('.form-group').removeClass('has-error').addClass('has-error');
                jQuery(e).closest('.help-block').remove();
            },
            success: function(e) {
                jQuery(e).closest('.form-group').removeClass('has-error');
                jQuery(e).closest('.help-block').remove();
                $("input#flag").val('T');
                $("input.guardar").removeAttr("disabled");
            },
            rules: {
                'email': {
                    required: true,
                    email: true
                }
            }
        });
    };

    return {
        init: function () {
            initValidationEmail();
        }
    };
}();

jQuery(function(){
    FormEmail.init();
});