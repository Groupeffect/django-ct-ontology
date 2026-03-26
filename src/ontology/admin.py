from django.contrib import admin
from django.apps import apps
from django.conf import settings

if (
    not hasattr(settings, "ONTOLOGY_DISABLE_MODELS")
    or settings.ONTOLOGY_DISABLE_MODELS is False
) and (
    not hasattr(settings, "ONTOLOGY_DISABLE_ADMIN")
    or settings.ONTOLOGY_DISABLE_ADMIN is False
):
    app_models = apps.get_app_config("ontology").get_models()

    for model in app_models:
        # Create a dynamic Admin class
        class DynamicAdmin(admin.ModelAdmin):
            verbose_name = "Ontology"
            list_display = [field.name for field in model._meta.fields]

        try:
            admin.site.register(model, DynamicAdmin)
        except admin.sites.AlreadyRegistered:
            pass
