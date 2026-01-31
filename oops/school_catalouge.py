# ---------------- PARENT CLASS ----------------
class School:
    def __init__(self, name, level, number_of_students):
        self._name = name
        self._level = level
        self._number_of_students = number_of_students

    # -------- GETTERS --------
    def get_name(self):
        return self._name

    def get_level(self):
        return self._level

    def get_number_of_students(self):
        return self._number_of_students

    # -------- SETTER --------
    def set_number_of_students(self, new_number):
        if isinstance(new_number, int) and new_number >= 0:
            self._number_of_students = new_number

    # -------- REPR METHOD --------
    def __repr__(self):
        return (
            f"School Name: {self._name}, "
            f"Level: {self._level}, "
            f"Number of Students: {self._number_of_students}"
        )


# ---------------- PRIMARY SCHOOL ----------------
class Primary(School):
    def __init__(self, name, number_of_students, pickup_policy):
        super().__init__(name, "primary", number_of_students)
        self._pickup_policy = pickup_policy

    def get_pickup_policy(self):
        return self._pickup_policy

    def __repr__(self):
        return (
            super().__repr__() +
            f", Pickup Policy: {self._pickup_policy}"
        )


# ---------------- MIDDLE SCHOOL ----------------
class Middle(School):
    def __init__(self, name, number_of_students):
        super().__init__(name, "middle", number_of_students)
    # No extra properties or methods


# ---------------- HIGH SCHOOL ----------------
class High(School):
    def __init__(self, name, number_of_students, sports_teams):
        super().__init__(name, "high", number_of_students)
        self._sports_teams = sports_teams

    def get_sports_teams(self):
        return self._sports_teams

    def __repr__(self):
        return (
            super().__repr__() +
            f", Sports Teams: {self._sports_teams}"
        )


# ---------------- TESTING ----------------
primary_school = Primary(
    "PS 101",
    500,
    "Pickup after 3pm"
)

middle_school = Middle(
    "MS 202",
    800
)

high_school = High(
    "HS 303",
    1200,
    ["basketball", "tennis", "soccer"]
)

print(primary_school)
print(middle_school)
print(high_school)
