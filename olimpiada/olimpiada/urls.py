"""
URL configuration for olimpiada project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView, RedirectView

from records.views import (RecordListView, RecordDetailView, RecordRedirectView,
                           RecordRedirectToListView, RecordCreateView, RecordUpdateView,
                           RecordDeleteView, load_events)#, register, user_login


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('register/', register, name='register'),
    # path('login/', user_login, name='login'),
    # path('logout/', user_logout, name='logout'),
    # path('about-us/', RedirectView.as_view(url='www.about-us.com')),
    path('accounts/', include('allauth.urls')),
    path('', RecordRedirectToListView.as_view()),
    path('records/', RecordListView.as_view(), name='records-list'),
    path('r/<int:pk>/', RecordRedirectView.as_view()),
    # path('records/<int:pk>/', RecordDetailView.as_view(), name='records-detail'),
    path('records/<int:pk>/', RecordUpdateView.as_view(), name='records-update'),
    path('records/<int:pk>/delete/', RecordDeleteView.as_view(), name='records-delete'),
    path('records/create/', RecordCreateView.as_view(), name='records-create'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),

    path('ajax/load-events/', load_events, name='ajax_load_events'),
]
