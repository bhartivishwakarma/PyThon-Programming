def student_counter():
  for i in range(1,5001):
    yield i

student_generator = student_counter()
for student_id in student_generator:
  
  if student_id==100:
    student_generator.throw(ValueError,"Invalid student ID")
  print(student_id)