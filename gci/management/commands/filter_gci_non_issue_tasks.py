import os.path

from ruamel.yaml import YAML
from django.core.management.base import BaseCommand

from gci.gitorg import get_issue


class Command(BaseCommand):
    help = 'Extract the tasks which dont have an issue associated with them'

    def add_arguments(self, parser):
        parser.add_argument('output_dir', type=str)

    def handle(self, *args, **options):
        output_dir = options.get('output_dir')

        non_issue_tasks = {}

        yaml = YAML()

        with open(os.path.join(output_dir, 'tasks.yaml')) as f:
            tasks = yaml.load(f)

            for task in tasks:
                issue = get_issue(tasks[task]['external_url'])
                if not issue:
                    non_issue_tasks[task] = tasks[task]

        with open(os.path.join(output_dir, 'non_issue_tasks.yaml'), 'w') as nf:
            yaml.dump(non_issue_tasks, nf)
