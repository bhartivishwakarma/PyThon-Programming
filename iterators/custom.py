class CustomerCounter:
    def __init__(self,count):
        self.count=count
    def __iter__(self):
      self.count=0
      return self
    def __next__(self):
    
          self.count +=1
        
          if self.count>100:
              raise StopIteration
          return self.count
customer_counter=CustomerCounter(0)
for customer_count in customer_counter:
  print(customer_count)