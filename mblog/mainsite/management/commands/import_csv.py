from mainsite.models import Person
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Since the CSV headers match the model fields,
        # you only need to provide the file's path (or a Python file object)
        insert_count = Person.objects.from_csv('./media/data.csv')
        print("{} records inserted".format(insert_count))
