from django.core.management.base import BaseCommand, CommandError
from storage.models import Item
from io import StringIO
import csv

class Command(BaseCommand):
    help = 'Imports book library from specified wiki page dump'

    def add_arguments(self, parser):
        parser.add_argument('parent')
        parser.add_argument('file')

    def handle(self, *args, **options):
        with open(options['file']) as fd:
            sio = StringIO(fd.read())
            reader = csv.reader(sio, delimiter='|')
            parent = Item.objects.get(pk=options['parent'])
            for line in reader:
                line = list(map(str.strip, line))
                item = Item(parent=parent)
                item.name = line[2]
                item.props['author'] = line[1]
                item.props['owner'] = line[3]
                item.props['can_borrow'] = line[4]
                item.props['borrowed_by'] = line[5]
                item.save()

                self.stdout.write(self.style.NOTICE('Book added: %r') % item)

            self.stdout.write(self.style.SUCCESS('Successfully imported data'))
