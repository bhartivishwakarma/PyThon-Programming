
#with statement
with open("file_name.txt", "w") as file:
   file.write("How you gonna win when you ain't right within?")


#without with statement
file = open("file_name.txt", "w")
try:
   file.write("How you gonna win when you ain't right within?")
finally:
   file.close()
