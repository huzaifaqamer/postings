from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostView.as_view(), name='list-create-post'),
    path('<int:pk>', views.PostRetrieveUpdateView.as_view(), name='retrieve-update-post'),
]
