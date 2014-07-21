from django.core.management.base import BaseCommand, CommandError

from rules_engine.models import Order
from rules_engine.service import checkout_order


class Command(BaseCommand):

    args = '<order_number>'
    help = 'Add item to known order(Specified by order number.)'

    def handle(self, *args, **options):
        try:

            order_number = args[0]
            order = checkout_order(order_number)

        except Order.DoesNotExist, e:
            raise CommandError('Order "%s" does not exist' % order_number)
        except Exception, e:
            raise CommandError(e.message)

        self.stdout.write('Successfully checked out order "%s"' % order_number)
