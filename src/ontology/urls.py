from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = []

if (
    not hasattr(settings, "ONTOLOGY_DISABLE_MODELS")
    or settings.ONTOLOGY_DISABLE_MODELS is False
):
    urlpatterns = [
        path("ontology/", include("ontology.routes.api")),
    ]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
