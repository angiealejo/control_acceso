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
    var ipAddresInput = function(){
        jQuery.validator.addMethod("ipAddresInput",function(value, element) {
            return this.optional(element) || value != '___.___.___.___';
        },
        "Este campo es obligatorio."
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
                'nombre': {
                    required: true
                },
                'instalacion': {
                    required: true
                },
                'ip_publica': {
                    required: true,
                    ipAddresInput: true
                },
                'ip_privada': {
                    required: true,
                    ipAddresInput: true
                },
                'puerto_publico': {
                    required: true,
                    digits: true,
                    min: 0
                },
                'puerto_privado': {
                    required: true,
                    digits: true,
                    min: 0
                }
            },
            messages: {
                'puerto_publico': {
                    digits: 'Solo se aceptan numeros positivos',
                    min: 'Solo se aceptan numeros positivos'
                },
                'puerto_privado': {
                    digits: 'Solo se aceptan numeros positivos',
                    min: 'Solo se aceptan numeros positivos'
                }
            }
        });
    };

    return {
        init: function () {
            validarRegex();
            ipAddresInput();
            initValidationPuntoControl();
        }
    };
}();

jQuery(function(){
    FormPuntoControl.init();
});