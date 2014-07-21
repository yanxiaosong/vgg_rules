from django.core.management.base import BaseCommand, CommandError
from rules_engine.models import OrderDetail, Product, Order


class Command(BaseCommand):

    args = '<order_number product_code amount>'
    help = 'Add item to known order(Specified by order number.)'

    def handle(self, *args, **options):
        try:

            order_number, product_code, amount = args
            order_detail = OrderDetail.objects.purchase_item(order_number, product_code.upper, int(amount))

        except Product.DoesNotExist, e:
            raise CommandError('Product "%s" does not exist' % product_code)
        except Order.DoesNotExist, e:
            raise CommandError('Order "%s" does not exist' % order_number)
        except ValueError, e:
            raise CommandError('Amount(%s) is not a number. ' % amount)
        except Exception, e:
            raise CommandError(e.message)

        self.stdout.write('Successfully add item "%s" to order "%s"' % (product_code, order_number))
