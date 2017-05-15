/*
 *  Validacion para el index.html -> Login
 */

var Login = function() {
    var initLoginFormValidation = function(){
        jQuery('.login-form-validation').validate({
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
                'username': {
                    required: true,
                    minlength: 1
                },
                'password': {
                    required: true,
                    minlength: 4
                }
            },
            messages: {
                'username': {
                    required: 'Por favor introduzca un nombre de usuario',
                    minlength: 'Su nombre usuario debe tener al menos 4 caracteres'
                },
                'password': {
                    required: 'Por favor introduzca su contraseña',
                    minlength: 'Su contraseña debe tener al menos 4 caracteres'
                }
            }
        });
    };

    return {
        init: function () {
            initLoginFormValidation();
        }
    };
}();

jQuery(function(){ Login.init(); });