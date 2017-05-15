# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from apps.bitacora.models import Bitacora
from apps.empleado.mixins import GenerarExcelMixin
from apps.reporte.forms import ReporteForm


class Reporte(GenerarExcelMixin, FormView):
    form_class = ReporteForm
    success_url = reverse_lazy('reporte:reporte_recursos')
    template_name = 'reporte/reporte_recursos_humanos.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        filtros = [form['fecha_inicio'].data, form['fecha_fin'].data,
                   form['instalacion'].data, form['puntocontrol'].data, form['empleado'].data, form['evento'].data]
        consulta = Bitacora.objects.all().values('empleado__numero_empleado', 'empleado__empleado__nombre',
                                                 'empleado__empleado__apellido_paterno',
                                                 'empleado__empleado__apellido_materno',
                                                 'instalacion__nombre', 'puntocontrol__nombre',
                                                 'evento', 'fecha', 'hora')
        if filtros[0] != u'' and filtros[1] != u'' and filtros[0] is not None and filtros[1] is not None:
            consulta = consulta.filter(fecha__range=[filtros[0], filtros[1]])
        if filtros[2] != u'' and filtros[2] is not None:
            consulta = consulta.filter(instalacion__id__icontains=filtros[2])
        if filtros[3] != u'' and filtros[3] is not None:
            consulta = consulta.filter(puntocontrol__id__icontains=filtros[3])
        if filtros[4] != u'' and filtros[4] is not None:
            consulta = consulta.filter(empleado__id=filtros[4])
        if filtros[5] != u'' and filtros[5] is not None:
            consulta = consulta.filter(evento=filtros[5])
        consulta = consulta.order_by('empleado__numero_empleado', 'id')
        if consulta.count() > 0:
            nombre_archivo_excel = "Reporte"
            columnas_ancho = [
                (u"No. Empleado", 20), (u"Nombre", 30), (u"Apellido Paterno", 20), (u"Apellido Materno", 20),
                (u"Instalacion", 20), (u"Punto de Control", 20), (u"Evento", 20), (u"Fecha", 15), (u"Hora", 15)
            ]
            fila_titulo = 'A1:I1'
            return self.generarexcelresponse(nombre_archivo_excel, columnas_ancho, fila_titulo, consulta)
        else:
            return HttpResponseRedirect(self.get_success_url())
