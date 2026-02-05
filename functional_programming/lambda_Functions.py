""" 
def squared(x):
  return x * x

def cubed(x):
  return x*x*x
"""
def odd_or_even(n, even_function, odd_function):
  # Remove this statement for Checkpoint 1.
  if n%2==0:
    return even_function(n)
  else:
    return odd_function(n)
# Checkpoint 2 code goes here.
square = lambda n : n*n
cube = lambda n : n*n*n
# Checkpoint 3 code goes here.
test = odd_or_even(5,cube,square)
print(test) # Uncomment the print function to see the results of Checkpoint 3.