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


def get_tripples(graph):
    g = RL.Graph()
    g += graph
    # return [[x[2] for x in g.triples([i, RL.RDFS.label, None])] for i in g.subjects()]
    # return [i for i in g.subjects()][0]
    # domain = g.namespaces
    return [i for i in g.predicates()]


def prepare_instance(instance, graph):

    try:
        curie = graph.namespace_manager.curie(instance)

        namespace = curie.split(":")[0]
        label = curie.split(":")[1]
        description = list(graph.triples([instance, RL.DC.description, None]))
        data = {
            "namespace": namespace,
            "name": instance.lower(),
            "tag": "preset",
            "label": label,
            "description": description,
        }
        print(data)
        return data
    except Exception as e:
        print(e)
        return {}


def prepare_triple(graph, triple):
    return {
        "sub": prepare_instance(triple[0], graph),
        "pred": prepare_instance(triple[1], graph),
        "obj": prepare_instance(triple[2], graph),
    }


def structured_triple(graph):
    """a loop to structure rdf"""
    triples = list(graph.triples([None, None, None]))
    result = []
    for triple in triples:
        result.append(prepare_triple(graph, triple))
        break

    return result


if __name__ in ["__main__"]:
    # G = parse_rdf_to_graph(ONTOLOGIES["qudt"]["unit"], "ttl")
    G = parse_rdf_to_graph("/app/.local/django/qudt-unit.ttl", format="ttl")
    # T = get_tripples(G)
    U = structured_triple(G)
    print(U)
