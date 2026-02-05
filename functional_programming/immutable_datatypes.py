from collections import namedtuple

# Checkpoint 1 code goes here.
country=namedtuple("country",["name","capital","continent"])
# Checkpoint 2 code goes here.
France = country("France","Paris","Europe")
Japan = country("Japan","Tokyo","Asia")
Senegal = country("Senegal","Dakar","Africa")
# Checkpoint 3 code goes here.
countries=(France,Japan,Senegal)