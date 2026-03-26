from rest_framework import serializers
from ontology import models


class MetaModelSerializer(serializers.ModelSerializer):
    has_owner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = None

    def get_has_owner(self, instance):
        return instance.has_owner.username

    def create(self, validated_data):
        validated_data["has_owner"] = self.context["request"].user
        return super().create(validated_data)


class PredicateSerializer(MetaModelSerializer):
    class Meta:
        model = models.Predicate
        fields = "__all__"


class SubjectSerializer(MetaModelSerializer):
    class Meta:
        model = models.Subject
        fields = "__all__"


class ObjectSerializer(MetaModelSerializer):
    class Meta:
        model = models.Object
        fields = "__all__"


class TripleSerializer(MetaModelSerializer):
    class Meta:
        model = models.Triple
        fields = "__all__"


class DomainSerializer(MetaModelSerializer):
    class Meta:
        model = models.Domain
        fields = "__all__"


class GraphSerializer(MetaModelSerializer):
    class Meta:
        model = models.Graph
        fields = "__all__"
