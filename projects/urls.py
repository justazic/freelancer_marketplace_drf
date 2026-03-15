from django.urls import path
from .views import CancelProjectView, ProjectListView, ProjectCreateView, ProjectDetailView, ProjectUpdateView

urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("create/", ProjectCreateView.as_view(), name="project_create"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("<int:pk>/update/", ProjectUpdateView.as_view(), name="project_update"),
    path("<int:pk>/cancel/", CancelProjectView.as_view(), name="cancel_project"),
]