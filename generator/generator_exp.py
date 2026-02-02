
def cs_generator():
  for i in range(1,5):
    yield "Computer Science " + str(i)


cs_courses=cs_generator()

for course in cs_courses:
  print(course)
cs_generator_exp=("Computer Science "+str(i) for i in range(1,5))
for i in cs_generator_exp:
  print(i)
