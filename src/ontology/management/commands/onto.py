from django.template.defaultfilters import default
from django.core.management.base import BaseCommand, CommandError
from ontology.management.tools import rdf
from ontology import models


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument(
            "-l",
            "--load",
            required=False,
            help="load ontology",
            action="store_true",
        )
        parser.add_argument(
            "-o",
            "--ontology",
            required=False,
            type=str,
            default="qudt",
            help=f"presets: {[i for i in rdf.ONTOLOGIES.keys()]}",
        )
        parser.add_argument(
            "-n",
            "--namespace",
            required=False,
            type=str,
            default="unit",
            help=f"presets: {[f"{i} : { [x for x in rdf.ONTOLOGIES[i].keys()] }" for i in rdf.ONTOLOGIES]}",
        )
        parser.add_argument(
            "-uf",
            "--url_or_file_path",
            required=False,
            type=str,
            default=None,
            help="If url_or_file_path is set then presets will be ignored.",
        )

    def handle(self, *args, **options):
        print(options)

        if options["load"]:
            upload = input(
                f"do you want to upload  {options["ontology"]} {options["namespace"]} [y/n]: "
            )
            if upload in ["y", "Y", "yes", "Yes", "YES"]:
                print(upload)
                if options["url_or_file_path"]:
                    G = rdf.parse_rdf_to_graph(options["url_or_file_path"], "ttl")
                    res = rdf.structured_triple(G)
                    print(res)
        # self.stdout.write(
        #     self.style.SUCCESS('Successfully closed poll "%s"' % poll_id)
        # )
