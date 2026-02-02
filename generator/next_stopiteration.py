def student_standing_generator():
  student_standings = ['Freshman','Senior', 'Junior', 'Freshman']

  for standing in student_standings:
    if standing == 'Freshman':
      yield 500
standing_values=student_standing_generator()
print(next(standing_values))
print(next(standing_values))
print(next(standing_values))
print(next(standing_values))
