/*
 *  Validacion para el fotoempleado_form.html -> Foto Empleado Form
 */

var FormFotoEmpleado = function() {

    var initValidationFotoEmpleado = function(){
        jQuery('.js-validation-material').validate({
            errorElement: 'div',
            errorClass: 'help-block text-right',
            errorPlacement: function(error, e) {
                jQuery(e).parents('.form-group .form-material').append(error);
                $("input.guardar").attr("disabled", true);
            },
            highlight: function(e) {
                jQuery(e).closest('.form-group').removeClass('has-error').addClass('has-error');
                jQuery(e).closest('.help-block').remove();
                $("input.guardar").removeAttr("disabled");
            },
            success: function(e) {
                jQuery(e).closest('.form-group').removeClass('has-error');
                jQuery(e).closest('.help-block').remove();
                $("input.guardar").removeAttr("disabled");
            },
            rules: {
                'foto': {
                    required: true
                }
            },
            messages: {
                'foto': {
                    required: 'Debe subir una foto.'
                }
            }
        });
    };

    return {
        init: function () {
            initValidationFotoEmpleado();
        }
    };
}();

jQuery(function(){
    FormFotoEmpleado.init();
});