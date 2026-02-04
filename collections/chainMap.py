from collections import ChainMap

customer_info = {'name': 'Dmitri Buyer', 'age': '31', 'address': '123 Python Lane', 'phone_number': '5552930183'}

shirt_dimensions = {'shoulder': 20, 'chest': 42, 'torso_length': 29}

pants_dimensions = {'waist': 36, 'leg_length': 42.5, 'hip': 21.5, 'thigh': 25, 'bottom': 18}

customer_data = ChainMap(customer_info, shirt_dimensions, pants_dimensions)
print(customer_data)
customer_leg_length = customer_data['leg_length']
print(customer_leg_length)
customer_size_data = customer_data.parents
print(customer_size_data)
customer_data['address'] = '456 ChainMap Drive'

print(customer_data)


year_profit_data = [
    {'jan_profit': 15492.30, 'jan_holiday_profit': 2589.12},
    {'feb_profit': 17018.05, 'feb_holiday_profit': 3701.88},
    {'mar_profit': 11849.13},
    {'apr_profit': 9870.68},
    {'may_profit': 13662.34},
    {'jun_profit': 12903.54},
    {'jul_profit': 16965.08, 'jul_holiday_profit': 4360.21},
    {'aug_profit': 17685.69},
    {'sep_profit': 9815.57},
    {'oct_profit': 10318.28},
    {'nov_profit': 23295.43, 'nov_holiday_profit': 9896.55},
    {'dec_profit': 21920.19, 'dec_holiday_profit': 8060.79}
]

new_months_data = [
    {'jan_profit': 13977.85, 'jan_holiday_profit': 2176.43},
    {'feb_profit': 16692.15, 'feb_holiday_profit': 3239.74},
    {'mar_profit': 17524.35, 'mar_holiday_profit': 4301.92}
]

# Write your code below!
profit_map=ChainMap(*year_profit_data)
def get_profits(profit_map):
  total_standard_profit = 0.0
  total_holiday_profit = 0.0
  for key in profit_map.keys():
    if 'holiday' in key:
        total_holiday_profit += profit_map[key]
    else:
      total_standard_profit += profit_map[key]
  
  return total_standard_profit , total_holiday_profit

last_year_standard_profit,last_year_holiday_profit=get_profits(profit_map)


for item in new_months_data:
  profit_map = profit_map.new_child(item)

current_year_standard_profit,current_year_holiday_profit=get_profits(profit_map)

year_diff_standard_profit = current_year_standard_profit - last_year_standard_profit
year_diff_holiday_profit = current_year_holiday_profit - last_year_holiday_profit

print(year_diff_standard_profit)
print(year_diff_holiday_profit)