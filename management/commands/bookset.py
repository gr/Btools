# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from ...models import BookSet

class Command(BaseCommand):
    args = '<bookset_name>'
    help = 'Update Bookset'

    def handle(self, *args, **options):       
        try:
            bset = BookSet.objects.get(name = args[1])
        except BookSet.DoesNotExist:
           raise CommandError('BookSet "%s" does not exist' % args[1])
        except IndexError:
           raise CommandError('Set bookset which need to update')
        
        subcommands = ['update']
        if args[0] not in subcommands:
            raise CommandError('%s isn\'t in subcommands %s' % (args[0], str(subcommands)))
        
        if args[0] == 'update':
            bset.bookset_update()
            self.stdout.write('Successfully updates bookset "%s"\n' % args[1])

