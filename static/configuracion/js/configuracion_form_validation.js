/*
 *  Validacion para el punto_control_form.html -> PuntoControl Form
 */

var FormPuntoControl = function() {
    var validarRegex = function(){
        jQuery.validator.addMethod("regex",function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Formato invalido"
    )};


    var initValidationPuntoControl = function(){
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
                'empleado': {
                    required: true
                },
                'horas_ley': {
                    required: true,
                    max: 12,
                    min: 0
                },
                'horas_extras': {
                    required: true,
                    max: 6,
                    min: 0
                },
                'minutos_tolerancia': {
                    required: true,
                    max: 60,
                    min: 0
                },
                'lapso_entrada_salida':{
                    required: true,
                    regex: '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
                }
            },
            messages: {
                'lapso_entrada_salida': {
                    regex: 'Formato de hora erroneo'
                }
            }
        });
    };

    return {
        init: function () {
            validarRegex();
            initValidationPuntoControl();
        }
    };
}();

jQuery(function(){
    FormPuntoControl.init();
});