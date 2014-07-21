from django.core.management.base import BaseCommand, CommandError
from rules_engine.models import Order


class Command(BaseCommand):

    help = 'List orders'

    def handle(self, *args, **options):

        try:
            orders = Order.objects.all()
            print "perf"
            order_lists = "Order Count: %d\n" % orders.count()

            for order in orders:
                order_lists += "Order Num: %s | Status: %s | Date: %s \n" % (order.order_number, order.order_status, order.create_time)

            print "perf123"
        except ValueError, e:
            raise CommandError(e.message)

        self.stdout.write(order_lists)
