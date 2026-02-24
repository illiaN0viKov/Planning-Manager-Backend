
from django.urls import path
from .views import (
    ProjectListCreateView,
    ProjectRetrieveUpdateDeleteView,
    PlaceListCreateView, 
    PlaceRetrieveUpdateView
)

urlpatterns = [
 
    path("projects/", ProjectListCreateView.as_view(), name="project-list-create"),

    path("projects/<int:pk>/", ProjectRetrieveUpdateDeleteView.as_view(), name="project-detail"),

    path("projects/<int:project_id>/places/", PlaceListCreateView.as_view(), name="place-list-create"),

    path("projects/<int:project_id>/places/<int:pk>/", PlaceRetrieveUpdateView.as_view(), name="place-detail"),

    
]