from django.urls import path

from .views import ProjectListView,ProjectCreateView,ProjectDetailView,ProjectUpdateView,CancelProjectView

urlpatterns = [
    path("projects/", ProjectListView.as_view()),
    path("projects/create/", ProjectCreateView.as_view()),
    path("projects/<int:pk>/", ProjectDetailView.as_view()),
    path("projects/<int:pk>/update/", ProjectUpdateView.as_view()),
    path("projects/<int:pk>/cancel/", CancelProjectView.as_view()),
]