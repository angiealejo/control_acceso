/*
 *  Validacion para el importar_excel.html -> Importar Excel Empleado
 */

var FormFotoEmpleado = function() {

    var initValidationImportarEmpleado = function(){
        jQuery('.js-validation-material').validate({
            errorElement: 'div',
            errorClass: 'help-block text-right',
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
                'puntocontrol': {
                    required: true
                },
                'archivo': {
                    required: true
                }
            },
            messages: {
                'archivo': {
                    required: 'Debe subir un archivo excel (.xlsx).'
                }
            }
        });
    };

    return {
        init: function () {
            initValidationImportarEmpleado();
        }
    };
}();

jQuery(function(){
    FormFotoEmpleado.init();
});