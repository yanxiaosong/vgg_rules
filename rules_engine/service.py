from business_rules import run_all
from rules_engine.models import Order
from rules_engine.rules.definition import get_rules, OrderDetailVariables, OrderDetailActions


def checkout_order(order_number):

    order = Order.objects.get(order_number=order_number)
    rules = get_rules()

    # implement promotion rules
    order_regular_price = 0
    order_actual_price = 0

    for od in order.details.all():

        x = OrderDetailVariables(od)

        run_all(rule_list=rules,
                defined_variables=OrderDetailVariables(od),
                defined_actions=OrderDetailActions(od),
                )

        order_regular_price += od.regular_price
        order_actual_price += od.actual_price or 0

    order.regular_price = order_regular_price
    order.actual_price = order_actual_price
    order.status = Order.ORDER_STATUS_READY
    order.save()

    return order


def print_invoice(order_number):

    order = Order.objects.get(order_number=order_number)

    print "Order Number: %s"
    print "CODE"
    print "=============================="





