import requests
from rest_framework.exceptions import ValidationError

ARTIC_BASE_URL = "https://api.artic.edu/api/v1/artworks"


def fetch_artwork_by_id(external_id: int) -> dict:
    
    url = f"{ARTIC_BASE_URL}/{external_id}"
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        raise ValidationError(
            {"external_id": "Artwork does not exist in Art Institute API."}
        )

    data = response.json().get("data")

    if not data:
        raise ValidationError(
            {"external_id": "Invalid artwork response from external API."}
        )

    return {
        "external_id": data["id"],
        "title": data["title"],
    }