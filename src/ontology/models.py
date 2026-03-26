from django.conf import settings

if (
    not hasattr(settings, "ONTOLOGY_DISABLE_MODELS")
    or settings.ONTOLOGY_DISABLE_MODELS is False
):
    from ontology.db.models import *

else:
    print("set: ONTOLOGY_DISABLE_MODELS = False, if you want to load models.")
