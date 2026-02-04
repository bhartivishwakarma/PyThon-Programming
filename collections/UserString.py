from collections import UserString

# Create a class which inherits from the UserString class
class IntenseString(UserString):

    # A new method to capitalize and add exclamation points to our string
    def exclaim(self):
        self.data = self.data.upper() + '!!!'
        return self.data


    # Overwrite the count method to only count a certain letter
    def count(self, sub=None, start=0, end=0):
        num = 0
        for let in self.data:
            if let == 'P':
                num+=1
        return num


intense_string = IntenseString("python rules")

print(intense_string.exclaim())
print(intense_string.count())

str_name = 'python powered patterned products'
str_word = 'patterned '


class SubtractString(UserString):

    def __sub__(self, other):
        if other in self.data:
            self.data = self.data.replace(other, '')


subtract_string = SubtractString(str_name)
subtract_string - str_word
print(subtract_string)