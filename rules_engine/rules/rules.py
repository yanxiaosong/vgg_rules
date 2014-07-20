rules=[
# APPLE buy 2 get 1 free
{ "conditions": { "all": [
      { "name": "product_code",
        "operator": "equal_to",
        "value": "APPLE",
      },
      { "name": "product_amount",
        "operator": "greater_than_or_equal_to",
        "value": 2,
      },
  ]},
  "actions": [
      { "name": "buy_and_get_cheaper",
        "fields": [{"name": "buy_count", "value": 1},
                   {"name": "cheaper_count", "value": 1},
                   {"name": "sale_percentage", "value": 0.5},
                   ],
      },
  ],
},

# current_inventory < 5 OR (current_month = "December" AND current_inventory < 20)
# { "conditions": { "any": [
#       { "name": "current_inventory",
#         "operator": "less_than",
#         "value": 5,
#       },
#     ]},
#       { "all": [
#         {  "name": "current_month",
#           "operator": "equals",
#           "value": "December",
#         },
#         { "name": "goes_well_with",
#           "operator": "shares_at_least_one_element_with",
#           "value": ["eggnog", "sugar cookies"],
#         }
#       ]},
#   },
#   "actions": [
#     { "name": "order_more",
#       "fields":[{"name":"number_to_order", "value": 40}]}
#   ]
# }

]