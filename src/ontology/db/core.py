from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from rest_framework.reverse import reverse
import rdflib as RL

bn = {"blank": True, "null": True}


class MetaModel(models.Model):
    name = models.CharField(max_length=255, help_text="The name of the instance.")
    description = models.TextField(**bn, help_text="The description of the instance.")
    namespace = models.CharField(
        max_length=255, **bn, help_text="The namespace of the instance."
    )
    label = models.CharField(
        max_length=255, **bn, help_text="The label of the instance."
    )
    tag = models.CharField(max_length=255, **bn, help_text="The tag of the instance.")
    is_public = models.BooleanField(
        default=True, help_text="Whether the instance is public."
    )
    is_private = models.BooleanField(
        default=False, help_text="Whether the instance is private."
    )
    uri = models.URLField(**bn, help_text="The URI of the instance.")
    api = models.URLField(**bn, help_text="The REST API of the instance.")
    wiki = models.URLField(**bn, help_text="The wiki of the instance.")
    meta = models.JSONField(**bn, help_text="The meta data in json format.")
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

    @property
    def admin_url(self):
        MODEL = self.__class__.__name__.lower()
        return reverse(f"admin:{self._meta.app_label}_{MODEL}_change", args=[self.id])

    @property
    def api_url(self):
        MODEL = self.__class__.__name__.lower()
        return reverse(f"{MODEL}-detail", args=[self.id])

    @property
    def model_uri(self):
        MODEL = self.__class__.__name__.lower()
        MODEL_URI = RL.URIRef(
            reverse(f"admin:{self._meta.app_label}_{MODEL}_changelist")
        )
        return MODEL_URI

    @property
    def graph(self):
        MODEL_URI = self.model_uri
        MODEL = self.__class__.__name__.lower()
        g = RL.Graph()
        g.bind(f"ns-{MODEL}", RL.Namespace(MODEL_URI + "#Entity"))

        g.add((MODEL_URI, RL.RDF.type, RL.RDFS.Class))
        g.add(
            (
                RL.URIRef(self.admin_url),
                RL.RDFS.subClassOf,
                MODEL_URI,
            )
        )
        g.add((RL.URIRef(self.admin_url), RL.DC.source, RL.URIRef(self.api_url)))
        g.add(
            (
                RL.URIRef(self.admin_url),
                RL.URIRef(f"{MODEL_URI}#has_owner"),
                RL.Literal(self.has_owner.username),
            )
        )
        g.add(
            (
                RL.URIRef(f"{MODEL_URI}#has_owner"),
                RL.RDFS.subPropertyOf,
                MODEL_URI,
            )
        )
        for field in self._meta.get_fields():
            if field.name not in [
                "id",
                "has_members",
                "has_owner",
                "_state",
                "_cache_version",
                "predicate",
                "subject",
                "object",
                "triple",
                "graph",
                "rdf",
                "model_uri",
            ]:
                g.add(
                    (
                        MODEL_URI,
                        RL.SSN.hasProperty,
                        RL.URIRef(f"{MODEL_URI}#{field.name}"),
                    )
                )

                g.add(
                    (
                        RL.URIRef(self.admin_url),
                        RL.URIRef(f"{MODEL_URI}#{field.name}"),
                        RL.Literal(getattr(self, field.name)),
                    )
                )

        for member in self.has_members.all():
            g.add(
                (
                    RL.URIRef(self.admin_url),
                    RL.ORG.hasMember,
                    RL.Literal(member.username),
                )
            )
        return g

    @property
    def rdf(self):
        return self.graph.serialize(format="ttl")


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
