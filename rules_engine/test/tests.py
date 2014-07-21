from django.test import TestCase
from ..models import Order, OrderDetail, Product
from ..service import checkout_order, print_invoice

class RuleEngineTest(TestCase):

    def test_create_order(self):
        order = Order.objects.create_order()
        self.assertIsNotNone(order)
        self.assertEqual(order.status, Order.ORDER_STATUS_NEW)
        print order.order_number
        self.assertGreater(len(order.order_number), 1)

    def test_add_item(self):

        order = Order.objects.create_order()

        od = OrderDetail.objects.purchase_item(order.order_number,'APPLE',1)
        self.assertIsNotNone(od)
        self.assertGreater(od.amount, 0)
        self.assertGreater(od.unit_price, 0)
        self.assertGreater(od.regular_price, 0)

        od = OrderDetail.objects.purchase_item(order.order_number,'PEAR',100)
        self.assertIsNotNone(od)
        self.assertGreater(od.amount, 0)
        self.assertGreater(od.unit_price, 0)
        self.assertGreater(od.regular_price, 0)

        od = OrderDetail.objects.purchase_item(order.order_number,'PEAR',0)
        self.assertIsNone(od)

        od = OrderDetail.objects.purchase_item(order.order_number,'PEAR',-10)
        self.assertIsNone(od)

        try:
            od = OrderDetail.objects.purchase_item(order.order_number,'PEAR_NO_EXIST',99)
        except Exception, e:
            self.assertIsInstance(e, Product.DoesNotExist)

        self.assertEqual(order.details.count(), 2)

    def test_show_orders(self):
        pass

    def test_check_out(self):

        # Test case 1: no promotion
        order = Order.objects.create_order()
        od = OrderDetail.objects.purchase_item(order.order_number, 'APPLE', 1)
        od = OrderDetail.objects.purchase_item(order.order_number, 'PEAR', 100)

        order = checkout_order(order.order_number)

        self.assertEqual(order.details.count(), 2)
        self.assertEqual(order.regular_price, 15100)
        self.assertEqual(order.order_promotions.count(), 0)

        # Test case 2: promotion: Buy 2 apple, get 1 free
        order = Order.objects.create_order()
        od = OrderDetail.objects.purchase_item(order.order_number, 'APPLE', 7)
        od = OrderDetail.objects.purchase_item(order.order_number, 'PEAR', 100)

        order = checkout_order(order.order_number)

        self.assertEqual(order.details.count(), 2)
        self.assertEqual(order.regular_price, 15700)
        self.assertEqual(order.actual_price, 15500)
        self.assertEqual(order.order_promotions.count(), 1)
        self.assertEqual(order.order_promotions.get().amount, 200)


        # Test case 3: promotion: Buy 2 apple, get 1 free
        order = Order.objects.create_order()
        od = OrderDetail.objects.purchase_item(order.order_number, 'APPLE', 17)
        od = OrderDetail.objects.purchase_item(order.order_number, 'PEAR', 100)

        order = checkout_order(order.order_number)

        self.assertEqual(order.details.count(), 2)
        self.assertEqual(order.regular_price, 16700)
        self.assertEqual(order.actual_price, 16300)
        self.assertEqual(order.order_promotions.count(), 1)
        self.assertEqual(order.order_promotions.get().amount, 400)

        # Test case 4: promotion: Buy 2 apple, get 1 free
        order = Order.objects.create_order()
        od = OrderDetail.objects.purchase_item(order.order_number, 'APPLE', 20)
        od = OrderDetail.objects.purchase_item(order.order_number, 'PEAR', 100)

        order = checkout_order(order.order_number)

        self.assertEqual(order.details.count(), 2)
        self.assertEqual(order.regular_price, 17000)
        self.assertEqual(order.actual_price, 16500)
        self.assertEqual(order.order_promotions.count(), 1)
        self.assertEqual(order.order_promotions.get().amount, 500)