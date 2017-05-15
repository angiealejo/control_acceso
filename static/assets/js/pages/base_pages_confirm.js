/*
 *  Document   : base_pages_register.js
 *  Author     : pixelcave
 *  Description: Custom JS code used in Register Page
 */

var BasePagesRegister = function() {
    // Init Register Form Validation, for more examples you can check out https://github.com/jzaefferer/jquery-validation
    var initValidationRegister = function(){
        jQuery('.js-validation-register').validate({
            errorClass: 'help-block text-right animated fadeInDown',
            errorElement: 'div',
            errorPlacement: function(error, e) {
                jQuery(e).parents('.form-group .form-material').append(error);
            },
            highlight: function(e) {
                jQuery(e).closest('.form-group').removeClass('has-error').addClass('has-error');
                jQuery(e).closest('.help-block').remove();
            },
            success: function(e) {
                jQuery(e).closest('.form-group').removeClass('has-error');
                jQuery(e).closest('.help-block').remove();
            },
            rules: {

                'new_password1': {
                    required: true,
                    minlength: 5
                },
                'new_password2': {
                    required: true,
                    equalTo: '#new_password1'
                }
            },
            messages: {

                'new_password1': {
                    required: 'Por favor ingrese su contraseña',
                    minlength: 'Su nombre de usuario debe tener al menos 5 caracteres'
                },
                'new_password2': {
                    required: 'Por favor ingrese su contraseña',
                    minlength: 'Su nombre de usuario debe tener al menos 5 caracteres',
                    equalTo: 'Por favor, introduzca la misma contraseña que arriba'
                }
            }
        });
    };

    return {
        init: function () {
            // Init Register Form Validation
            initValidationRegister();
        }
    };
}();

// Initialize when page loads
jQuery(function(){ BasePagesRegister.init(); });