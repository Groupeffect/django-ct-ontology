from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from ontology import serializers
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.conf import settings


def set_filterset_fields_exclude(serializer_class):
    fields = [
        "JSONField",
        "PointField",
        "MultiPointField",
        "PolygonField",
        "MultiPolygonField",
        "LineStringField",
        "MultiLineStringField",
        "GenericForeignKey",
        "FileField",
        "CompositePrimaryKey",
        "GeometryField",
        "ForeignKey",
        "OneToOneField",
        "ManyToManyField",
        "ManyToManyRel",
        "ManyToOneRel",
    ]
    result = []
    for field in serializer_class.Meta.model._meta.get_fields():
        if field.__class__.__name__ not in fields:
            result.append(field.name)

    return result


class MetaViewset(ModelViewSet):
    serializer_class = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.serializer_class.Meta.model.objects.all()
        elif self.request.user.is_authenticated:
            qs = self.serializer_class.Meta.model.objects.filter(
                Q(
                    Q(has_owner=self.request.user)
                    | Q(has_members__in=[self.request.user])
                    | Q(is_private=False, is_public=True)
                )
            )
            return qs
        else:
            return self.serializer_class.Meta.model.objects.filter(
                is_public=True, is_private=False
            )


class PredicateViewset(MetaViewset):
    serializer_class = serializers.PredicateSerializer
    filterset_fields = set_filterset_fields_exclude(serializer_class)
    search_fields = filterset_fields + ["id"]


class SubjectViewset(MetaViewset):
    serializer_class = serializers.SubjectSerializer
    filterset_fields = set_filterset_fields_exclude(serializer_class)
    search_fields = filterset_fields + ["id"]


class ObjectViewset(MetaViewset):
    serializer_class = serializers.ObjectSerializer
    filterset_fields = set_filterset_fields_exclude(serializer_class)
    search_fields = filterset_fields + ["id"]


class TripleViewset(MetaViewset):
    serializer_class = serializers.TripleSerializer
    filterset_fields = set_filterset_fields_exclude(serializer_class)
    search_fields = filterset_fields + ["id"]


class DomainViewset(MetaViewset):
    serializer_class = serializers.DomainSerializer
    filterset_fields = set_filterset_fields_exclude(serializer_class)
    search_fields = filterset_fields + ["id"]


class GraphViewset(MetaViewset):
    serializer_class = serializers.GraphSerializer
    filterset_fields = set_filterset_fields_exclude(serializer_class)
    search_fields = filterset_fields + ["id"]
