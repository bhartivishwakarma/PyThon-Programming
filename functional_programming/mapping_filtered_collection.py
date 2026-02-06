nums = (2, 12, 5, 8, 9, 3, 16, 7, 13, 19, 21, 1, 15, 4, 22, 20, 11)

# Checkpoint 1 code goes here.
greater_than_10_doubled = map(lambda x: x*2 , filter(lambda y: y>10,nums))
print(tuple(greater_than_10_doubled))
# Checkpoint 2 code goes here.
functional_way= map(lambda i: i*3,filter(lambda x : x%3 ==0,nums))
print(tuple(functional_way))