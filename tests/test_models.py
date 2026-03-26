from ontology import models
from ontology.db import core
from django.test import SimpleTestCase, TestCase


class MetaModelTests(SimpleTestCase):
    """Tests for the abstract MetaModel base class."""

    def test_meta_model_is_abstract(self):
        self.assertTrue(core.MetaModel._meta.abstract)


class MetaTestCase(TestCase):
    def setUp(self):
        self.domain, created = models.Domain.objects.update_or_create(
            name="test",
            namespace="test",
            label="test",
            tag="test",
            is_public=True,
            is_private=False,
            uri="http://test.com",
            api="http://test.com",
            wiki="http://test.com",
            meta="http://test.com",
            has_owner=None,
        )


class PredicateTests(MetaTestCase):
    def test_meta(self):
        self.assertEqual(models.Predicate._meta.db_table, "ontology_predicate")
        self.assertFalse(models.Predicate._meta.abstract)

    def test_fields(self):
        field_names = [f.name for f in models.Predicate._meta.get_fields()]
        for expected in [
            "name",
            "description",
            "domain",
            "namespace",
            "label",
            "tag",
            "is_public",
            "is_private",
            "has_owner",
            "has_members",
            "meta",
        ]:
            self.assertIn(expected, field_names)

    def test_create_read_update_delete(self):
        """CRUD test instance"""
        # create
        instance = models.Predicate.objects.create(
            name="test",
            description="test",
            domain=self.domain,
            namespace="test",
            label="test",
            tag="test",
            is_public=True,
            is_private=False,
            has_owner=None,
        )

        # read
        fetched = models.Predicate.objects.get(pk=instance.pk)
        self.assertEqual(fetched.name, "test")
        self.assertEqual(fetched.description, "test")
        self.assertEqual(fetched.domain, self.domain)
        self.assertEqual(fetched.namespace, "test")
        self.assertEqual(fetched.label, "test")
        self.assertEqual(fetched.tag, "test")
        self.assertEqual(fetched.is_public, True)
        self.assertEqual(fetched.is_private, False)
        self.assertEqual(fetched.has_owner, None)

        # update
        fetched.name = "test2"
        fetched.save()
        updated = models.Predicate.objects.get(pk=instance.pk)
        self.assertEqual(updated.name, "test2")

        # delete
        pk = instance.pk
        instance.delete()
        self.assertFalse(models.Predicate.objects.filter(pk=pk).exists())


class SubjectTests(MetaTestCase):
    def test_meta(self):
        self.assertEqual(models.Subject._meta.db_table, "ontology_subject")
        self.assertFalse(models.Subject._meta.abstract)

    def test_fields(self):
        field_names = [f.name for f in models.Subject._meta.get_fields()]
        for expected in [
            "name",
            "description",
            "domain",
            "namespace",
            "label",
            "tag",
            "is_public",
            "is_private",
            "has_owner",
            "has_members",
        ]:
            self.assertIn(expected, field_names)

    def test_create_read_update_delete(self):
        """CRUD test instance"""
        # create
        instance = models.Subject.objects.create(
            name="test",
            description="test",
            domain=self.domain,
            namespace="test",
            label="test",
            tag="test",
            is_public=True,
            is_private=False,
            has_owner=None,
        )

        # read
        fetched = models.Subject.objects.get(pk=instance.pk)
        self.assertEqual(fetched.name, "test")
        self.assertEqual(fetched.description, "test")
        self.assertEqual(fetched.domain, self.domain)
        self.assertEqual(fetched.namespace, "test")
        self.assertEqual(fetched.label, "test")
        self.assertEqual(fetched.tag, "test")
        self.assertEqual(fetched.is_public, True)
        self.assertEqual(fetched.is_private, False)
        self.assertEqual(fetched.has_owner, None)

        # update
        fetched.name = "test2"
        fetched.save()
        updated = models.Subject.objects.get(pk=instance.pk)
        self.assertEqual(updated.name, "test2")

        # delete
        pk = instance.pk
        instance.delete()
        self.assertFalse(models.Subject.objects.filter(pk=pk).exists())


class DomainTests(TestCase):
    def test_meta(self):
        self.assertEqual(models.Domain._meta.db_table, "ontology_domain")
        self.assertFalse(models.Domain._meta.abstract)

    def test_fields(self):
        field_names = [f.name for f in models.Domain._meta.get_fields()]
        for expected in [
            "name",
            "description",
            "namespace",
            "label",
            "tag",
            "is_public",
            "is_private",
            "uri",
            "api",
            "wiki",
            "meta",
            "has_owner",
            "has_members",
        ]:
            self.assertIn(expected, field_names)

    def test_create_read_update_delete(self):
        """CRUD test instance"""
        # create
        instance = models.Domain.objects.create(
            name="test2",
            description="test2",
            namespace="test2",
            label="test2",
            tag="test2",
            is_public=True,
            is_private=False,
            uri="http://test2.com",
            has_owner=None,
        )

        # read
        fetched = models.Domain.objects.get(pk=instance.pk)
        self.assertEqual(fetched.name, "test2")
        self.assertEqual(fetched.description, "test2")
        self.assertEqual(fetched.namespace, "test2")
        self.assertEqual(fetched.label, "test2")
        self.assertEqual(fetched.tag, "test2")
        self.assertEqual(fetched.is_public, True)
        self.assertEqual(fetched.is_private, False)
        self.assertEqual(fetched.uri, "http://test2.com")
        self.assertEqual(fetched.has_owner, None)

        # update
        fetched.name = "test3"
        fetched.save()
        updated = models.Domain.objects.get(pk=instance.pk)
        self.assertEqual(updated.name, "test3")

        # delete
        pk = instance.pk
        instance.delete()
        self.assertFalse(models.Domain.objects.filter(pk=pk).exists())


class ObjectTests(MetaTestCase):
    def test_meta(self):
        self.assertEqual(models.Object._meta.db_table, "ontology_object")
        self.assertFalse(models.Object._meta.abstract)

    def test_fields(self):
        field_names = [f.name for f in models.Object._meta.get_fields()]
        for expected in [
            "name",
            "description",
            "domain",
            "namespace",
            "label",
            "tag",
            "is_public",
            "is_private",
            "has_owner",
            "has_members",
        ]:
            self.assertIn(expected, field_names)

    def test_create_read_update_delete(self):
        """CRUD test instance"""
        # create
        instance = models.Object.objects.create(
            name="test",
            description="test",
            domain=self.domain,
            namespace="test",
            label="test",
            tag="test",
            is_public=True,
            is_private=False,
            has_owner=None,
        )

        # read
        fetched = models.Object.objects.get(pk=instance.pk)
        self.assertEqual(fetched.name, "test")
        self.assertEqual(fetched.description, "test")
        self.assertEqual(fetched.domain, self.domain)
        self.assertEqual(fetched.namespace, "test")
        self.assertEqual(fetched.label, "test")
        self.assertEqual(fetched.tag, "test")
        self.assertEqual(fetched.is_public, True)
        self.assertEqual(fetched.is_private, False)
        self.assertEqual(fetched.has_owner, None)

        # update
        fetched.name = "test2"
        fetched.save()
        updated = models.Object.objects.get(pk=instance.pk)
        self.assertEqual(updated.name, "test2")

        # delete
        pk = instance.pk
        instance.delete()
        self.assertFalse(models.Object.objects.filter(pk=pk).exists())


class TripleTests(MetaTestCase):
    def test_meta(self):
        self.assertEqual(models.Triple._meta.db_table, "ontology_triple")
        self.assertFalse(models.Triple._meta.abstract)

    def test_fields(self):
        field_names = [f.name for f in models.Triple._meta.get_fields()]
        for expected in [
            "name",
            "description",
            "domain",
            "namespace",
            "label",
            "tag",
            "is_public",
            "is_private",
            "sub",
            "pred",
            "obj",
            "has_owner",
            "has_members",
        ]:
            self.assertIn(expected, field_names)

    def test_create_read_update_delete(self):
        """CRUD test instance"""
        # create
        sub = models.Subject.objects.create(name="test_sub")
        pred = models.Predicate.objects.create(name="test_pred")
        obj = models.Object.objects.create(name="test_obj")

        instance = models.Triple.objects.create(
            name="test",
            description="test",
            domain=self.domain,
            namespace="test",
            label="test",
            tag="test",
            is_public=True,
            is_private=False,
            sub=sub,
            pred=pred,
            obj=obj,
            has_owner=None,
        )

        # read
        fetched = models.Triple.objects.get(pk=instance.pk)
        self.assertEqual(fetched.name, "test")
        self.assertEqual(fetched.description, "test")
        self.assertEqual(fetched.domain, self.domain)
        self.assertEqual(fetched.namespace, "test")
        self.assertEqual(fetched.label, "test")
        self.assertEqual(fetched.tag, "test")
        self.assertEqual(fetched.is_public, True)
        self.assertEqual(fetched.is_private, False)
        self.assertEqual(fetched.sub, sub)
        self.assertEqual(fetched.pred, pred)
        self.assertEqual(fetched.obj, obj)
        self.assertEqual(fetched.has_owner, None)

        # update
        fetched.name = "test2"
        fetched.save()
        updated = models.Triple.objects.get(pk=instance.pk)
        self.assertEqual(updated.name, "test2")

        # delete
        pk = instance.pk
        instance.delete()
        self.assertFalse(models.Triple.objects.filter(pk=pk).exists())


class GraphTests(MetaTestCase):
    def test_meta(self):
        self.assertEqual(models.Graph._meta.db_table, "ontology_graph")
        self.assertFalse(models.Graph._meta.abstract)

    def test_fields(self):
        field_names = [f.name for f in models.Graph._meta.get_fields()]
        for expected in [
            "name",
            "description",
            "domain",
            "namespace",
            "label",
            "tag",
            "is_public",
            "is_private",
            "tripples",
            "has_owner",
            "has_members",
        ]:
            self.assertIn(expected, field_names)

    def test_create_read_update_delete(self):
        """CRUD test instance"""
        # create
        instance = models.Graph.objects.create(
            name="test",
            description="test",
            domain=self.domain,
            namespace="test",
            label="test",
            tag="test",
            is_public=True,
            is_private=False,
            has_owner=None,
        )

        # read
        fetched = models.Graph.objects.get(pk=instance.pk)
        self.assertEqual(fetched.name, "test")
        self.assertEqual(fetched.description, "test")
        self.assertEqual(fetched.domain, self.domain)
        self.assertEqual(fetched.namespace, "test")
        self.assertEqual(fetched.label, "test")
        self.assertEqual(fetched.tag, "test")
        self.assertEqual(fetched.is_public, True)
        self.assertEqual(fetched.is_private, False)
        self.assertEqual(fetched.has_owner, None)

        # update
        fetched.name = "test2"
        fetched.save()
        updated = models.Graph.objects.get(pk=instance.pk)
        self.assertEqual(updated.name, "test2")

        # delete
        pk = instance.pk
        instance.delete()
        self.assertFalse(models.Graph.objects.filter(pk=pk).exists())
