from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


bn = {"blank": True, "null": True}


class MetaModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(**bn)
    namespace = models.CharField(max_length=255, **bn)
    label = models.CharField(max_length=255, **bn)
    tag = models.CharField(max_length=255, **bn)
    is_public = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    uri = models.URLField(**bn)
    api = models.URLField(**bn)
    wiki = models.URLField(**bn)
    meta = models.JSONField(**bn)
    has_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **bn,
        related_name="owner",
        verbose_name="owner",
    )
    has_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        verbose_name="members",
        related_name="members",
    )

    class Meta:
        abstract = True
        unique_together = ["uri", "name", "namespace", "tag", "has_owner"]
        app_label = "ontology"


class Domain(MetaModel):
    uri = models.URLField()
    has_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="domain_owner",
        verbose_name="domain_owner",
    )
    has_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        verbose_name="domian_members",
        related_name="domian_members",
    )

    class Meta:
        unique_together = ["uri", "name", "namespace", "tag", "has_owner"]
        abstract = True
        app_label = "ontology"


class Predicate(MetaModel):
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, **bn)
    has_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="predicate_owner",
        verbose_name="predicate_owner",
    )
    has_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        verbose_name="predicate_members",
        related_name="predicate_members",
    )

    class Meta:
        unique_together = ["domain", "name", "namespace", "tag", "has_owner"]
        abstract = True
        app_label = "ontology"


class Subject(MetaModel):
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, **bn)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, **bn)
    object_id = models.PositiveIntegerField(**bn)
    content_object = GenericForeignKey("content_type", "object_id")
    links = models.JSONField(**bn)
    has_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subject_owner",
        verbose_name="subject_owner",
    )
    has_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        verbose_name="subject_members",
        related_name="subject_members",
    )

    class Meta:
        unique_together = ["domain", "name", "namespace", "tag", "has_owner"]
        abstract = True
        app_label = "ontology"


class Object(MetaModel):
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, **bn)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, **bn)
    object_id = models.PositiveIntegerField(**bn)
    content_object = GenericForeignKey("content_type", "object_id")
    links = models.JSONField(**bn)
    has_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="object_owner",
        verbose_name="object_owner",
    )
    has_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        verbose_name="object_members",
        related_name="object_members",
    )

    class Meta:
        unique_together = ["domain", "name", "namespace", "tag", "has_owner"]
        abstract = True
        app_label = "ontology"


class Triple(MetaModel):
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, **bn)

    sub = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name="Subject",
        related_name="subject",
    )
    pred = models.ForeignKey(
        Predicate,
        on_delete=models.CASCADE,
        verbose_name="Predicate",
        related_name="predicate",
    )
    obj = models.ForeignKey(
        Object, on_delete=models.CASCADE, verbose_name="Object", related_name="object"
    )
    has_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tripple_owner",
        verbose_name="tripple_owner",
    )
    has_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        verbose_name="tripple_members",
        related_name="tripple_members",
    )

    def __str__(self):
        return f"{self.sub} | {self.pred} | {self.obj}"

    class Meta:
        unique_together = ["domain", "name", "namespace", "tag", "has_owner"]
        abstract = True
        app_label = "ontology"


class Graph(MetaModel):
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, **bn)
    tripples = models.ManyToManyField(Triple, blank=True)
    has_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="graph_owner",
        verbose_name="graph_owner",
    )
    has_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        verbose_name="graph_members",
        related_name="graph_members",
    )

    class Meta:
        unique_together = ["domain", "name", "namespace", "tag", "has_owner"]
        abstract = True
        app_label = "ontology"
