from collections import OrderedDict

# The first 15 orders are provided
order_data = [['Order: 1', 'purchased'],
              ['Order: 2', 'purchased'],
              ['Order: 3', 'purchased'],
              ['Order: 4', 'returned'],
              ['Order: 5', 'purchased'],
              ['Order: 6', 'canceled'],
              ['Order: 7', 'returned'],
              ['Order: 8', 'purchased'],
              ['Order: 9', 'returned'],
              ['Order: 10', 'canceled'],
              ['Order: 11', 'purchased'],
              ['Order: 12', 'returned'],
              ['Order: 13', 'purchased'],
              ['Order: 14', 'canceled'],
              ['Order: 15', 'purchased']]


orders = OrderedDict(order_data)
to_move=[]
to_remove=[]
print(orders.items())
for key,value in orders.items():
  if value=='returned':
    to_move.append(key)
  elif value=='canceled':
    to_remove.append(key)

for remove in to_remove:
  orders.pop(remove)

for move in to_move:
  orders.move_to_end(move)
print(orders)