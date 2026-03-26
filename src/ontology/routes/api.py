from rest_framework import routers
from ontology import views

router = routers.DefaultRouter()

router.register(r"predicate", views.PredicateViewset, basename="predicate")
router.register(r"subject", views.SubjectViewset, basename="subject")
router.register(r"object", views.ObjectViewset, basename="object")
router.register(r"triple", views.TripleViewset, basename="triple")
router.register(r"domain", views.DomainViewset, basename="domain")
router.register(r"graph", views.GraphViewset, basename="graph")

urlpatterns = router.urls
