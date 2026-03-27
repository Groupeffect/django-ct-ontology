"""
Ontology	Base URI
Main QUDT Ontology	http://qudt.org/schema/shacl/qudt
QUDT Datatype Ontology	http://qudt.org/schema/shacl/datatype
QUDT Units Vocabulary	http://qudt.org/vocab/unit
QUDT QuantityKinds Vocabulary	http://qudt.org/vocab/quantitykind
QUDT DimensionVectors Vocabulary	http://qudt.org/vocab/dimensionvector
QUDT Physical Constants Vocabulary	http://qudt.org/vocab/constant
QUDT Systems of Units Vocabulary	http://qudt.org/vocab/sou
QUDT Systems of Quantity Kinds Vocabulary	http://qudt.org/vocab/soqk

"""

import rdflib as RL


ONTOLOGIES = {
    "qudt": {
        "unit": "https://qudt.org/vocab/unit/",
        "datatype": "https://qudt.org/schema/datatype/",
        "quantitykind": "http://qudt.org/vocab/quantitykind/",
        "main": "http://qudt.org/schema/shacl/qudt",
        "dimensionvector": "http://qudt.org/vocab/dimensionvector",
        "constant": "http://qudt.org/vocab/constant",
        "sou": "http://qudt.org/vocab/sou",
        "soqk": "http://qudt.org/vocab/soqk",
    },
}


def parse_rdf_to_graph(url_or_file_path, format="ttl"):
    g = RL.Graph()
    g.parse(url_or_file_path, format=format)
    return g
