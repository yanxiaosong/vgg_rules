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

    def test_show_orders(self):
        pass

    def tets_check_out(self):
        pass


{ "conditions": { "all": [
      { "name": "product_code",
        "operator": "equal_to",
        "value": "APPLE"
      },
      { "name": "product_amount",
        "operator": "greater_than_or_equal_to",
        "value": 2
      }
  ]},
  "actions": [
      { "name": "buy_and_get_cheaper",
        "fields": [{"name": "buy_count", "value": 1},
                   {"name": "cheaper_count", "value": 1},
                   {"name": "sale_percentage", "value": 0.5}
                   ]
      }
  ]
}

