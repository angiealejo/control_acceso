/*
 *  Validacion para el usuario_datos_admin_form.html -> Usuario Datos Admin Form
 */

var FormDatos = function() {
    var validarRegex = function(){
        jQuery.validator.addMethod("regex",function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Formato invalido"
    )};
    var validarCompararHoraEntradaSalida = function(){
        jQuery.validator.addMethod("hora_entrada",function(value, element) {
            var hora_entrada = parseInt(value);
            var hora_salida = parseInt(jQuery('input#id_hora_salida').val());
            return this.optional(element) || (hora_entrada < hora_salida);
        },
        "La hora de entrada debe ser menor a la de salida"
    )};
    var validarCompararHoraSalidaEntrada = function(){
        jQuery.validator.addMethod("hora_salida",function(value, element) {
            var hora_entrada = parseInt(jQuery('input#id_hora_entrada').val());
            var hora_salida = parseInt(value);
            return this.optional(element) || (hora_salida > hora_entrada);
        },
        "La hora de salida debe ser mayor a la de entrada"
    )};


    var initValidationDatos = function(){
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
                    required: true,
                    regex: "^[A-Za-zÑñÁÉÍÓÚáéíóú ]*$"
                },
                'apellido_paterno': {
                    required: true,
                    regex: "^[A-Za-zÑñÁÉÍÓÚáéíóú ]*$"
                },
                'apellido_materno': {
                    regex: "^[A-Za-zÑñÁÉÍÓÚáéíóú ]*$"
                },
                'fecha_nacimiento': {
                    regex: "^[0-9]{4}-((0[0-9])|(1[012]))-(([012][0-9])|3[01])$"
                },
                'curp': {
                    regex: "[A-Z]{1}[AEIOUX]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}"
                },
                'rfc': {
                    regex: "([A-Z,Ñ,&]{3,4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[A-Z|0-9]{3,4})"
                },
                'puntocontrol': {
                    required: true
                },
                'hora_entrada': {
                    regex: '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$',
                    hora_entrada: true
                },
                'hora_salida': {
                    regex: '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$',
                    hora_salida: true
                }
            },
            messages: {
                'nombre': {
                    regex: 'Solo se aceptan caracteres alfabeticos'
                },
                'apellido_paterno': {
                    regex: 'Solo se aceptan caracteres alfabeticos'
                },
                'apellido_materno': {
                    regex: 'Solo se aceptan caracteres alfabeticos'
                },
                'fecha_nacimiento': {
                    regex: 'Formato de fecha invalido'
                },
                'curp': {
                    regex: 'Formato de CURP invalido'
                },
                'rfc': {
                    regex: 'Formato de RFC invalido'
                },
                'hora_entrada': {
                    regex: 'Formato de hora erroneo'
                },
                'hora_salida': {
                    regex: 'Formato de hora erroneo'
                }
            }
        });
    };

    return {
        init: function () {
            validarRegex();
            validarCompararHoraEntradaSalida();
            validarCompararHoraSalidaEntrada();
            initValidationDatos();
        }
    };
}();

jQuery(function(){
    FormDatos.init();
});