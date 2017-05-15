/*
 *  Validacion para el registration/password_change_form -> Password Change
 */

var PasswordChange = function() {
    var initPasswordChangeFormValidation = function(){
        jQuery('.js-validation-reminder').validate({
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
                'old_password': {
                    required: true,
                    minlength: 4
                },
                'new_password1': {
                    required: true,
                    minlength: 4
                },
                'new_password2': {
                    required: true,
                    minlength: 4,
                    equalTo: '#id_new_password1'
                }

            },
            messages: {
                'old_password': {
                    required: 'Por favor introduzca su contraseña anterior',
                    minlength: 'Su nombre usuario debe tener al menos 4 caracteres'
                },
                'new_password1': {
                    required: 'Por favor introduzca su nueva contraseña',
                    minlength: 'Su contraseña debe tener al menos 4 caracteres'
                },
                'new_password2': {
                    required: 'Por favor confirme su nueva contraseña',
                    minlength: 'Su contraseña debe tener al menos 4 caracteres',
                    equalTo: 'Por favor escriba la misma nueva contraseña'
                }
            }
        });
    };

    return {
        init: function () {
            initPasswordChangeFormValidation();
        }
    };
}();

jQuery(function(){ PasswordChange.init(); });