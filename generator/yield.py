 
def  class_standing_genertor():
  yield 'Freshman'
  yield 'Sophomore'
  yield  'Junior'
  yield 'Senior'
class_standings=class_standing_genertor()
for standing in class_standings:
  print(standing)