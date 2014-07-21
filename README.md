vgg_rules
==============

This is an experimental project for implementing rule engine(business_rule) in Python.

The project is a console application based on Django 1.6, implementing promotion calculations in business system:
* All goods are priced individually. Some items are also multi-priced based on quantity bought. Buy n of them, and they’ll cost you y cents.
* Pricing changes frequently
* Items could have multiple rules

The rule script in json format is saved in database and will be read and implemented to all the items ordered.

Rule Script Examples:

The "name" in "condtions" is defined in python class `OrderDetailVariables`. The "name" in "action" is defined in python class `OrderDetailActions`.

####1. Buy 3 oranges in a group at price $1.80 each(10% off).

```json

{ "conditions": { "all": [
      { "name": "product_code",
        "operator": "equal_to",
        "value": "ORANGE"
      },
      { "name": "product_amount",
        "operator": "greater_than_or_equal_to",
        "value": 3
      }
  ]},
  "actions": [
      { "name": "buy_group_and_cheaper",
        "params": {"group_count": 3,  "sale_price": 180}
      }
  ]
}
```

####2. Buy 5 apple, get 2 free

```json
{ "conditions": { "all": [
      { "name": "product_code",
        "operator": "equal_to",
        "value": "APPLE"
      },
      { "name": "product_amount",
        "operator": "greater_than_or_equal_to",
        "value": 5
      }
  ]},
  "actions": [
      { "name": "buy_and_get_cheaper",
        "params": {"buy_count": 5,  "cheaper_count": 2, "sale_percentage": 0}
      }
  ]
}
```


## Command Usage

### 1. Create a new order

This command will create a new order.

`$ python manage.py createorder`


### 2. Purchase Items

This command will add item to specified order. If the same item has been added, the amount will add up.

`$ python manage.py additem <order_number> <product_code> <amount>`


### 3. List orders

List all the orders.

`$ python manage.py listorders`

A sample order list:

<pre><code>
Order Count: 2
Order Num: 6QIE1405909818 | Status: Checkout(1) | Date: 2014-07-21 02:30:18+00:00
Order Num: WIY51405918562 | Status: New(0) | Date: 2014-07-21 04:56:02+00:00
<\pre><\code>


### 4. Checkout Order

Check out order, change the order status, and implement all the available promotion rules to purchased items.


### 5. Print the order invoice

`$ python manage.py invoice <ordre_number>`

A sample invoice:

<pre><code>
Order Number: WIY51405918562
REGLR PRICE  3800.00
PRMTN PRICE  3120.00
================= ITEMS ==============
CODE:APPLE     NAME:red apple
REGLR PRICE  2000.00
PRMTN PRICE  1500.00
Promotion APPLE2_1
Buy 5 apple, get 2 free
-----------------------------
CODE:ORANGE     NAME:big orange
REGLR PRICE  1800.00
PRMTN PRICE  1620.00
Promotion ORANGE_3
Buy 3 oranges in a group at price $1.80 each(10% off)
-----------------------------
</code></pre>


