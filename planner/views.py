from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Project, Place
from .serializers import ProjectSerializer, PlaceSerializer

from .art_api import fetch_artwork_by_id



#Projects
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def delete(self, request, *args, **kwargs):
        project = self.get_object()

        # rule:
        # A project cannot be deleted if any place is visited
        if project.places.filter(is_visited=True).exists():
            raise ValidationError(
                "Project cannot be deleted because it has visited places."
            )

        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#Places
class PlaceListCreateView(generics.ListCreateAPIView):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        return Place.objects.filter(
            project_id=self.kwargs["project_id"]
        )

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs["project_id"])

        # Max 10 places per project
        if project.places.count() >= 10:
            raise ValidationError(
                "A project can have a maximum of 10 places."
            )

        external_id = serializer.validated_data["external_id"]

        #Validate 
        artwork = fetch_artwork_by_id(external_id)

        # Prevent duplicates
        if project.places.filter(
            external_id=external_id
        ).exists():
            raise ValidationError(
                "This place is already added to the project."
            )

        serializer.save(
            project=project,
            external_id=artwork["external_id"],
            title=artwork["title"],
        )


class PlaceRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        return Place.objects.filter(project_id=project_id)