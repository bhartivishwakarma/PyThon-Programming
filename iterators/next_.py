dog_foods = {
  "Great Dane Foods": 4,
  "Min Pip Pup Foods": 10,
  "Pawsome Pup Foods": 8
}


dog_food_iterator=iter(dog_foods)
next_dog_food1=next(dog_food_iterator)
next_dog_food2=next(dog_food_iterator)
next_dog_food3=next(dog_food_iterator)
print(next_dog_food2)
print(next_dog_food3)

next(dog_food_iterator)