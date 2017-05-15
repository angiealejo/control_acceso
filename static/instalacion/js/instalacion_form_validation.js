/*
 *  Validacion para el instalacion_form.html -> Instalacion Form
 */

var FormInstalacion = function() {
    var validarRegex = function(){
        jQuery.validator.addMethod("regex",function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Formato invalido"
    )};


    var initValidationInstalacion = function(){
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
            },
            success: function(e) {
                jQuery(e).closest('.form-group').removeClass('has-error');
                jQuery(e).closest('.help-block').remove();
                $("input.guardar").removeAttr("disabled");
            },
            rules: {
                'nombre': {
                    required: true
                },
                'numero_interior': {
                    regex: '^[0-9a-zA-ZñÑ]*$'
                },
                'numero_exterior': {
                    regex: '^[0-9a-zA-ZñÑ]*$'
                },
                'codigo_postal': {
                    regex: '^[0-9]*$'
                }
            },
            messages: {
                'numero_interior': {
                    regex: 'Solo se acepta caracteres alfanumericos'
                },
                'numero_exterior': {
                    regex: 'Solo se acepta caracteres alfanumericos'
                },
                'codigo_postal': {
                    regex: 'Formato de codigo postal erroneo'
                }
            }
        });
    };

    return {
        init: function () {
            validarRegex();
            initValidationInstalacion();
        }
    };
}();

jQuery(function(){
    FormInstalacion.init();
});