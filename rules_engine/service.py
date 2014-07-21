from business_rules import run_all
from rules_engine.models import Order
from rules_engine.rules.definition import get_rules, OrderDetailVariables, OrderDetailActions
from rules_engine.util import format_money


def checkout_order(order_number):

    order = Order.objects.get(order_number=order_number)
    rules = get_rules()

    # implement promotion rules
    order_regular_price = 0
    order_actual_price = 0

    for od in order.details.all():

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
    if order.status != Order.ORDER_STATUS_READY:
        raise Exception("Invoice is not available. Order %s has not been checked out. " % order_number)

    invoice = "Order Number: %s\n" + \
              "REGLR PRICE %s\n" % format_money(order.regular_price) + \
              "PRMTN PRICE %s\n" % format_money(order.actual_price) + \
              "===============================\n"

    for od in order.details:
        invoice += "CODE:%s     NAME:%s" % (od.product.product_code, od.product.name)
        invoice += "REGLR PRICE %s\n" % format_money(od.regular_price)
        invoice += "PRMTN PRICE %s\n" % format_money(od.actual_price)
        for promotion in od.order_detail_promotions:
            invoice += "Promotion %s\n" % promotion.code
            invoice += "%s\n" % promotion.description
        invoice += "-----------------------------"

    return invoice
