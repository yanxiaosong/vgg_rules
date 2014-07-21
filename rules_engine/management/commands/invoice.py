from django.core.management.base import BaseCommand, CommandError
from rules_engine.models import OrderDetail, Product, Order
from rules_engine.service import checkout_order


class Command(BaseCommand):

    args = '<order_number>'
    help = 'Add item to known order(Specified by order number.)'

    def handle(self, *args, **options):
        try:

            order_number = args[0]
            invoice = print_invoice(order_number)

        except Order.DoesNotExist, e:
            raise CommandError('Order "%s" does not exist' % order_number)
        except Exception, e:
            raise CommandError(e.message)

        self.stdout.write(invoice)
