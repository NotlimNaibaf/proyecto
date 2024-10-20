from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from pyexpat.errors import messages

from datos.forms import CursoForm
from datos.models import RegistroUsuarioForm, Curso


class ListaCursosView(LoginRequiredMixin, ListView):
    model=Curso
    template_name = 'cursos/Lista_cursos.html'
    context_object_name = 'cursos'

    def get_queryset(self):
        if self.request.user.rol == 'admin':
            return Curso.objects.all()
        return Curso.objects.filter(estado=True)


class DetalleCursoView(LoginRequiredMixin, DetailView):
    model = Curso
    template_name = 'cursos/Detalle_curso.html'
    context_object_name = 'curso'

class InscribirCursoView(LoginRequiredMixin, DetailView):
    model = Curso

    def get(self,request,*args, **kwargs):
        curso = self.get_object()
        if request.user not in curso.inscriptos.all() and curso.inscriptos.count() < curso.cupos:
            curso.inscriptos.add(request.user)
            messages.success(request, f'se ha inscrito exitosamente en el curso {curso.nombre}')
        else:
            messages.error(request, 'No se ha inscrito en el curso')
        return redirect('detalle_curso', pk=curso.pk)

class CrearCursoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/cursos_form.html'
    success_url = reverse_lazy('listar_cursos')

    def test_func(self):
        return self.request.user.rol == 'admin'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'el Curso Se ha creado correctamente')
        return response

class MisCursosView(LoginRequiredMixin, ListView):
    model = Curso
    template_name = 'cursos/lista_cursos.html'
    context_object_name = 'cursos'

    def get_queryset(self):
        return self.request.user.cursos_inscritos.all()



class CustomLoginView(LoginView):
    template_name = 'registro/login.html'

    def form_valid(self, form):
        messages.error(self.request, 'Usuario o contrasena Incorrecto. Por intente nuevamente')
        return super().form_valid(form)

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Sesion cerrada correctamente')
        response = redirect('login')
        response = ['Cache-Control'] ='no-cache, no-store, must-revalidate'
        response = ['Pragma'] = 'no-cahe'
        response = ['Expires'] = '0'
        return response



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




