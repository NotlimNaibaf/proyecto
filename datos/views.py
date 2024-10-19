from django.shortcuts import render
from django.views.generic import CreateView
from pyexpat.errors import messages

from datos.models import RegistroUsuarioForm


class RegistroUsuarioView(CreateView):
    form_class = RegistroUsuarioForm
    template_name = 'registro/registro.html'
    success_url = reverse_lazy('lista_cursos')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Registrado exitosamente')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
            return super().form_valid(form)



# Create your views here.
