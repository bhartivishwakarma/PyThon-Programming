from collections import UserList

# Create a class which inherits from the UserList class
class CondenseList(UserList):

    # A new method to remove duplicate items from the list
    def condense(self):
        self.data = list(set(self.data))
        print(self.data)


    # We can also overwrite a method from the list class
    def clear(self):
        print("Deleting all items from the list!")
        super().clear()

condense_list = CondenseList(['t-shirt', 'jeans', 'jeans', 't-shirt', 'shoes'])

condense_list.condense()

condense_list.clear()
