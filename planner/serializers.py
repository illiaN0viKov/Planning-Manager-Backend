from rest_framework import serializers
from django.db import transaction
from .models import Project, Place
from .art_api import fetch_artwork_by_id
from rest_framework.exceptions import ValidationError


class PlaceCreateInputSerializer(serializers.Serializer):
    external_id = serializers.IntegerField()


class PlaceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            "id",
            "title",
            "notes",
            "is_visited",
            "external_id",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    # WRITE-only input
    places_input = PlaceCreateInputSerializer(
        many=True, write_only=True, required=False
    )

    # READ-only output
    places = PlaceReadSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "is_completed",
            "created_at",
            "updated_at",
            "places",
            "places_input",
        ]
        read_only_fields = ["id",  "created_at", "updated_at"]

    def create(self, validated_data):
        places_data = validated_data.pop("places_input", [])

        with transaction.atomic():
            project = Project.objects.create(**validated_data)

            for place in places_data:
                external_id = place["external_id"]

                artwork = fetch_artwork_by_id(external_id)

                if project.places.filter(external_id=external_id).exists():
                    raise ValidationError(
                        "Duplicate place in project creation."
                    )

                Place.objects.create(
                    project=project,
                    external_id=artwork["external_id"],
                    title=artwork["title"],
                )

        return project

class PlaceSerializer(serializers.ModelSerializer):
    external_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Place
        fields = [
            "id",
            "external_id",
            "title",
            "notes",
            "is_visited",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "title",
            "created_at",
            "updated_at",
        ]

