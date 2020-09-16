from mainsite.models import Person
from django.core.management.base import BaseCommand
from django.db.models import Count


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # All this method needs is the path to your CSV.
        # (If you don't provide one, the method will return the CSV as a string.)
       # Person.objects.to_csv('./media/export.csv')
        Person.objects.annotate(name_count=Count('name')).to_csv('./media/export1.csv')