from operator import mod
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import BaseVariables, numeric_rule_variable, string_rule_variable
import datetime
from rules_engine.models import OrderPromotionLog


class OrderDetailVariables(BaseVariables):

    def __init__(self, order_detail):
        self.order_detail = order_detail

    @string_rule_variable
    def product_code(self):
        return self.order_detail.product.code

    @numeric_rule_variable()
    def product_amount(self):
        return self.order_detail.amount

    @numeric_rule_variable()
    def product_amount(self):
        return self.order_detail.amount


class OrderDetailActions(BaseActions):
    def __init__(self, order_detail):
        self.order_detail = order_detail
        self.product = order_detail.product

    @rule_action(params={"buy_count": FIELD_NUMERIC,
                         "cheaper_count": FIELD_NUMERIC,
                         "sale_percentage": FIELD_NUMERIC,
                         "promotion_id": FIELD_NUMERIC})
    def buy_and_get_cheaper(self, buy_count, cheaper_count, sale_percentage, promotion_id):

        """
        buy x at regular price,  get y at promotion price
        """

        # caculate the promtion price
        total_cnt = self.order_detail.amount
        mod_cnt = mod(total_cnt, (buy_count + cheaper_count))
        mod_cnt_regular = (mod_cnt if mod_cnt <= buy_count else buy_count)
        mod_cnt_promotion = (mod_cnt-buy_count) if (mod_cnt-buy_count) > 0 else 0
        group_cnt = int (total_cnt / (buy_count + cheaper_count))

        regular_price_cnt = group_cnt * buy_count + mod_cnt_regular
        promotion_price_cnt = group_cnt * cheaper_count + mod_cnt_promotion

        actual_price = regular_price_cnt * self.order_detail.unit_price \
            + promotion_price_cnt * self.order_detail.unit_price * sale_percentage

        self.order_detail.actual_price = actual_price
        self.order_detail.save()

        # add promotion log
        log_promotion(self.order_detail, promotion_id)


    @rule_action(params={"group_count": FIELD_NUMERIC, "sale_price": FIELD_NUMERIC, "promotion_id": FIELD_NUMERIC})
    def buy_group_and_cheaper(self, group_count, sale_price, promotion_id):
        """
        buy X as a group at price Y, instead of regular price
        """

        # calculate promotion price
        group_price_count = int(self.order_detail.amount / group_count)
        regular_price_count = self.order_detail.amount - group_price_count * group_count
        actual_price = group_price_count * sale_price + regular_price_count * self.order_detail.unit_price

        # update the order price
        self.order_detail.actual_price = actual_price
        self.order_detail.save()

        # add promotion log
        log_promotion(self.order_detail, promotion_id)


def log_promotion(order_detail, promotion_id):
    p_log = OrderPromotionLog()
    p_log.promotion_date = datetime.datetime.today()
    p_log.order = order_detail.order
    p_log.order_detail = order_detail
    p_log.amount = order_detail.regular_price - order_detail.actual_price
    p_log.promotion_id = promotion_id

    p_log.save()


def get_rules():
    pass

