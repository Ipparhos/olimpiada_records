from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout, get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, TemplateView, DetailView, RedirectView, CreateView, UpdateView, \
    DeleteView
from django.utils.decorators import method_decorator

from .forms import RecordForm#, UserCreationForm, UserLoginForm
from .models import Record, Discipline

User= get_user_model()
# Create your views here.

class LoginRequiredMixin(object):
    # @classmethod
    # def as_view(cls, **initkwargs):
    #     view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
    #     return login_required(view)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class RecordRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url_params = self.kwargs
        pk = url_params['pk']
        obj = get_object_or_404(Record, pk=pk)
        # print(url_params)
        return f'/records/{obj.pk}'


class RecordRedirectToListView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return '/records/'


class AboutUsView(LoginRequiredMixin, TemplateView):
    template_name = 'about.html'


# class RecordsView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'record_list.html')
#
#     def post(self, request, *args, **kwargs):
#         return
#
# class RecordsListView(ListView):
#     queryset = Record.objects.all()

class RecordListView(LoginRequiredMixin, ListView):
    """ app_name = records
        model = record
        view_name = list
        template_name = <app_name>/<model>_<view_name>.html"""
    model = Record

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.get_title()
        # print(context)
        return context

    def get_title(self):
        return self.title

    # template_name = 'record_list.html'
    title = 'Records'


class RecordDetailView(LoginRequiredMixin, DetailView):
    model = Record

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user)


class RecordCreateView(LoginRequiredMixin, CreateView):
    form_class = RecordForm
    template_name = 'forms.html'
    success_url = '/records'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        # print(form.cleaned_data)
        return super().form_valid(form)


class RecordUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RecordForm
    model = Record
    template_name_suffix = '_detail'

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user)

    def get_success_url(self):
        return self.object.get_edit_url()


class RecordDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'forms_delete.html'

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user)

    def get_success_url(self):
        return "/records/"


def load_disciplines(request):
    stadium_id = request.GET.get('stadium')
    print('stadium_id:', stadium_id)
    disciplines = Discipline.objects.filter(stadium_id=stadium_id).order_by('name')
    return render(request, 'records/disciplines_dropdown_list_options.html', {'disciplines': disciplines})


# from django.contrib.auth.views import LogoutView
#
# class CustomLogoutView(LogoutView):
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.method == 'GET':
#             return self.get(request, *args, **kwargs)
#         return super().dispatch(request, *args, **kwargs)



# def register(request, *args, **kwargs):
#     form = UserCreationForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect('/login')
#     return render(request, 'records/register.html',{"form": form})
#
#
# def user_login(request, *args, **kwargs):
#     form = UserLoginForm(request.POST or None)
#     if form.is_valid():
#         user_obj = form.cleaned_data.get('user_obj')
#         login(request, user_obj)
#         print(f"User {user_obj} logged in successfully")
#         return HttpResponseRedirect('/')
#     return render(request, 'records/login.html', {"form": form})
#
#
# def user_logout(request, *args, **kwargs):
#     logout(request)
#
#     return HttpResponseRedirect('/login')