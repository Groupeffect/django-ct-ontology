# Test tools for RDF parsing and saving

from django.test import SimpleTestCase
from ontology.management.tools import rdf


class MetaTestCase(SimpleTestCase):
    pass


class RDFToolsTests(MetaTestCase):
    def test_parse_rdf_to_graph(self):
        g = rdf.parse_rdf_to_graph(rdf.ONTOLOGIES["qudt"]["main"], "ttl")
        self.assertIsNotNone(g)
