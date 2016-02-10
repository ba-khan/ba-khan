from django.core.management.base import BaseCommand, CommandError
from bakhanapp.models import Assesment

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('id_assesment', nargs='+', type=int)

    def handle(self, *args, **options):
        for id_assesment in options['id_assesment']:
            try:
                assesment = Assesment.objects.get(pk=id_assesment)
                self.stdout.write(str(assesment))
            except Assesment.DoesNotExist:
                raise CommandError('Assesment "%s" does not exist' % id_assesment)

            assesment.name = 'False'
            assesment.save()

            self.stdout.write('cambiado a false evaluated en assesment id %d'%(id_assesment))