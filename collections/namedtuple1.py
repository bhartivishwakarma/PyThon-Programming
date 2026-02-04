from collections import namedtuple

clothes = [('t-shirt', 'green', 'large', 9.99),
           ('jeans', 'blue', 'medium', 14.99),
           ('jacket', 'black', 'x-large', 19.99),
           ('t-shirt', 'grey', 'small', 8.99),
           ('shoes', 'white', '12', 24.99),
           ('t-shirt', 'grey', 'small', 8.99)]


actor_data_tuple = ('Leonardo DiCaprio', 1974, 'Titanic', 1997)
print(actor_data_tuple[3])
ClothingItem=namedtuple('ClothingItem',['type','color','size','price'])
new_coat=ClothingItem('coat','black','small',14.99)
coat_cost=new_coat.price
updated_clothes_data=[]
for cloth in clothes:
  updated_clothes_data.append(ClothingItem(cloth[0],cloth[1],cloth[2],cloth[3]))
print(updated_clothes_data)
