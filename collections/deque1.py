from helper_functions import process_csv_supplies
from collections import deque

# The first row is skipped since it only contains labels
csv_data = process_csv_supplies()[1:]

# Here is a sample of 2 elements in csv_data:
# [ ['nylon', '10', 'unimportant'], ['wool', '1', 'important'] ]


supplies_deque = deque()
for data in csv_data:
  if 'important' in data:
    supplies_deque.appendleft(tuple(data))
  else:
    supplies_deque.append(tuple(data))

ordered_important_supplies = deque()
for supply in range(25):

       ordered_important_supplies.append(supplies_deque.popleft())
ordered_unimportant_supplies = deque()
for supply in range(10):

       ordered_unimportant_supplies.append(supplies_deque.pop())
