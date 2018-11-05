import os.path

from ruamel.yaml import YAML
from django.core.management.base import BaseCommand

from gci.gitorg import get_issue


class Command(BaseCommand):
    help = 'Extract the tasks which dont have an issue associated with them'

    def add_arguments(self, parser):
        parser.add_argument('output_dir', type=str,
                            help='directory of tasks.yaml file')

    def handle(self, *args, **options):
        output_dir = options.get('output_dir')

        non_issue_tasks = {}

        yaml = YAML()

        try:
            with open(os.path.join(output_dir, 'tasks.yaml')) as f:
                tasks = yaml.load(f)

                for task in tasks:
                    external_url = tasks[task]['external_url']
                    print('external issue for task is {}'.format(external_url))
                    try:
                        issue = get_issue(external_url)
                        if not issue:
                            print('task {} is a non-issue task'.format(task))
                            non_issue_tasks[task] = tasks[task]
                        else:
                            print('task {} has a valid issue link'.format(task))
                    except Exception:
                        print('task {} has no external_url'.format(task))
                        non_issue_tasks[task] = tasks[task]

        except Exception:
            print('tasks.yaml file not found')

        with open(os.path.join(output_dir, 'non_issue_tasks.yaml'), 'w') as nf:
            print('dumping tasks to {}/non_issue_tasks.yaml'.format(output_dir))
            yaml.dump(non_issue_tasks, nf)
