from django.core.management.base import BaseCommand, CommandError
from rules_engine.models import Order


class Command(BaseCommand):

    help = 'create an new order.'

    def handle(self, *args, **options):
        try:
            order = Order.objects.create_order()
        except Exception, e:
            raise CommandError('order was not created successfully. Error: %s' % e.message)

        self.stdout.write('Successfully created order. Order Number = "%s"' % order.order_number)