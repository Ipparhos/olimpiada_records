from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout, get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, TemplateView, DetailView, RedirectView, CreateView, UpdateView, \
    DeleteView
from django.utils.decorators import method_decorator
from django.db.models import Case, When, Value, CharField

from .forms import RecordForm, UserSignupForm, GoalForm, RecordFilterForm
from .models import Record, Discipline, Goal, road_disciplines

User = get_user_model()
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


class AboutUsView(TemplateView):
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

class RecordListView(ListView):
    """ app_name = records
        model = record
        view_name = list
        template_name = <app_name>/<model>_<view_name>.html"""
    model = Record

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = RecordFilterForm(self.request.GET)
        context['title'] = 'Records'
        return context

    def get_queryset(self):
        queryset = Record.objects.annotate(
            discipline_type=Case(
                When(discipline__name__in=road_disciplines, then=Value('road')),
                default=Value('field'),
                output_field=CharField()
            )
        ).order_by('age_group__age_group', 'discipline_type', 'performance')

        indoors_outdoors = self.request.GET.get('indoors_outdoors')
        if indoors_outdoors:
            queryset = queryset.filter(discipline__stadium__indoors_outdoors=indoors_outdoors)

        return queryset

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


def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)  # Note: Pass 'request' to save
            login(request, user)
            return redirect('/')  # Redirect to home or desired page
    else:
        form = UserSignupForm()

    return render(request, 'signup.html', {'form': form})


class GoalListView(ListView):
    """ app_name = records
        model = record
        view_name = list
        template_name = <app_name>/<model>_<view_name>.html"""
    model = Goal

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.get_title()
        # print(context)
        return context

    def get_title(self):
        return self.title

    # template_name = 'record_list.html'
    title = 'Goals'


class GoalCreateView(LoginRequiredMixin, CreateView):
    form_class = GoalForm
    template_name = 'goal_forms.html'
    success_url = '/goals'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        # print(form.cleaned_data)
        return super().form_valid(form)


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    form_class = GoalForm
    model = Goal
    template_name_suffix = '_detail'

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def get_success_url(self):
        return self.object.get_edit_url()


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'forms_delete.html'

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def get_success_url(self):
        return "/goals/"


def records_view(request):
    filter_form = RecordFilterForm(request.GET)
    records = Record.objects.annotate(
        discipline_type=Case(
            When(discipline__name__in=road_disciplines, then=Value('road')),
            default=Value('field'),
            output_field=CharField()
        )
    ).order_by('age_group__age_group', 'discipline_type', 'performance')

    indoors_outdoors = request.GET.get('indoors_outdoors')
    if indoors_outdoors:
        records = records.filter(discipline__stadium__indoors_outdoors=indoors_outdoors)

    return render(request, 'records/records_list.html', {'records': records, 'filter_form': filter_form})