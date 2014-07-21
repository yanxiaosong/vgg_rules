vgg_rules
==============

This is an experimental project for implementing rule engine(business_rule) in Python.

The project is a console application based on Django 1.6, implementing promotion calculations in business system:
* `All goods are priced individually. Some items are also multi-priced based on quantity bought. Buy n of them, and they’ll cost you y cents.`
* `Pricing changes frequently`
* `Items could have multiple rules`

The rule script in json format is saved in database and will be read and implemented to all the items ordered.




## Command Usage

### 1. Create a new order




