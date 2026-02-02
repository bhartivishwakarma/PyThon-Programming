def generator():
  i = 0
  while True:
    try:
      yield i
    except GeneratorExit:
      print("Early exit, BYE!")
      break
    i += 1

my_generator = generator()
for item in my_generator:
  print(item)
  if item == 1:
    my_generator.close()
