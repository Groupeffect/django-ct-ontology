from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ontology import models

User = get_user_model()


class DomainAPITests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", password="password"
        )
        self.user = User.objects.create_user(username="user", password="password")

        self.public_domain = models.Domain.objects.create(
            name="Public Domain",
            namespace="public",
            uri="http://public.org",
            is_public=True,
            is_private=False,
            has_owner=self.superuser,
        )
        self.private_domain = models.Domain.objects.create(
            name="Private Domain",
            namespace="private",
            uri="http://private.org",
            is_public=False,
            is_private=True,
            has_owner=self.user,
        )

        self.list_url = reverse("domain-list", query={"limit": 100})
        self.detail_url = reverse("domain-detail", kwargs={"pk": self.public_domain.pk})

    def test_list_unauthenticated_sees_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        results = response.json().get("results", response.json())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Public Domain")

    def test_list_authenticated_sees_own_and_public(self):
        self.client.force_authenticate(user=self.user)
        # self.client.login(username="user", password="password")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        results = response.json().get("results", response.json())

        self.assertEqual(len(results), 2)

    def test_create_unauthenticated_fails(self):
        payload = {"name": "New Domain", "namespace": "new", "uri": "http://new.org"}
        response = self.client.post(self.list_url, payload)
        self.assertIn(response.status_code, [401, 403])

    def test_create_authenticated_succeeds(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "name": "New Domain",
            "namespace": "new",
            "uri": "http://new.org",
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(models.Domain.objects.filter(name="New Domain").exists())

    def test_retrieve_domain(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Public Domain")

    def test_update_domain(self):
        self.client.force_authenticate(user=self.user)
        payload = {"name": "Updated Domain"}
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, 200)
        self.public_domain.refresh_from_db()
        self.assertEqual(self.public_domain.name, "Updated Domain")

    def test_delete_domain(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            models.Domain.objects.filter(pk=self.public_domain.pk).exists()
        )


class PredicateAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password")
        self.superuser = User.objects.create_superuser(
            username="admin", password="password"
        )
        self.domain = models.Domain.objects.create(
            name="Domain", uri="http://domain.org", has_owner=self.user
        )

        self.public_predicate = models.Predicate.objects.create(
            name="Public Predicate",
            domain=self.domain,
            is_public=True,
            is_private=False,
            has_owner=self.superuser,
        )

        self.list_url = reverse("predicate-list", query={"limit": 100})
        self.detail_url = reverse(
            "predicate-detail", kwargs={"pk": self.public_predicate.pk}
        )

    def test_list_predicate(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        results = response.json().get("results", response.json())
        self.assertEqual(len(results), 1)

    def test_create_predicate(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "name": "New Predicate",
            "domain": self.domain.pk,
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, 201)

    def test_update_predicate(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, {"name": "Updated"})
        self.assertEqual(response.status_code, 200)


class SubjectAPITests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", password="password"
        )
        self.user = User.objects.create_user(username="user", password="password")
        self.domain = models.Domain.objects.create(
            name="Domain",
            uri="http://domain.org",
            has_owner=self.superuser,
        )

        self.public_subject = models.Subject.objects.create(
            name="Public Subject",
            domain=self.domain,
            is_public=True,
            is_private=False,
            has_owner=self.superuser,
        )

        self.list_url = reverse("subject-list", query={"limit": 100})
        self.detail_url = reverse(
            "subject-detail", kwargs={"pk": self.public_subject.pk}
        )

    def test_list_subject(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        results = response.json().get("results", response.json())
        self.assertEqual(len(results), 1)

    def test_create_subject(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "name": "New Subject",
            "domain": self.domain.pk,
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, 201)

    def test_update_subject(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, {"name": "Updated"})
        self.assertEqual(response.status_code, 200)


class ObjectAPITests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", password="password"
        )
        self.user = User.objects.create_user(username="user", password="password")
        self.domain = models.Domain.objects.create(
            name="Domain",
            uri="http://domain.org",
            has_owner=self.superuser,
        )

        self.public_object = models.Object.objects.create(
            name="Public Object",
            domain=self.domain,
            is_public=True,
            is_private=False,
            has_owner=self.superuser,
        )

        self.list_url = reverse("object-list", query={"limit": 100})
        self.detail_url = reverse("object-detail", kwargs={"pk": self.public_object.pk})

    def test_list_object(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        results = response.json().get("results", response.json())
        self.assertEqual(len(results), 1)

    def test_create_object(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "name": "New Object",
            "domain": self.domain.pk,
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, 201)

    def test_update_object(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, {"name": "Updated"})
        self.assertEqual(response.status_code, 200)


class TripleAPITests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", password="password"
        )
        self.user = User.objects.create_user(username="user", password="password")
        self.domain = models.Domain.objects.create(
            name="Domain",
            uri="http://domain.org",
            has_owner=self.superuser,
        )
        self.subject = models.Subject.objects.create(
            name="Subject",
            domain=self.domain,
            has_owner=self.superuser,
        )
        self.predicate = models.Predicate.objects.create(
            name="Predicate",
            domain=self.domain,
            has_owner=self.superuser,
        )
        self.object = models.Object.objects.create(
            name="Object",
            domain=self.domain,
            has_owner=self.superuser,
        )

        self.public_triple = models.Triple.objects.create(
            name="Public Triple",
            domain=self.domain,
            sub=self.subject,
            pred=self.predicate,
            obj=self.object,
            is_public=True,
            is_private=False,
            has_owner=self.superuser,
        )

        self.list_url = reverse("triple-list", query={"limit": 100})
        self.detail_url = reverse("triple-detail", kwargs={"pk": self.public_triple.pk})

    def test_list_triple(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        results = response.json().get("results", response.json())
        self.assertEqual(len(results), 1)

    def test_create_triple(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "name": "New Triple",
            "domain": self.domain.pk,
            "sub": self.subject.pk,
            "pred": self.predicate.pk,
            "obj": self.object.pk,
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, 201)

    def test_update_triple(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, {"name": "Updated"})
        self.assertEqual(response.status_code, 200)


class GraphAPITests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", password="password"
        )
        self.user = User.objects.create_user(username="user", password="password")
        self.domain = models.Domain.objects.create(
            name="Domain",
            uri="http://domain.org",
            has_owner=self.superuser,
        )

        self.public_graph = models.Graph.objects.create(
            name="Public Graph",
            domain=self.domain,
            is_public=True,
            is_private=False,
            has_owner=self.superuser,
        )

        self.list_url = reverse("graph-list", query={"limit": 100})
        self.detail_url = reverse("graph-detail", kwargs={"pk": self.public_graph.pk})

    def test_list_graph(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        results = response.json().get("results", response.json())
        self.assertEqual(len(results), 1)

    def test_create_graph(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "name": "New Graph",
            "domain": self.domain.pk,
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, 201)

    def test_update_graph(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, {"name": "Updated"})
        self.assertEqual(response.status_code, 200)
