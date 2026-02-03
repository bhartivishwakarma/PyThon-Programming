from collections import ChainMap

default_config = {
    "theme": "light",
    "language": "English",
    "timeout": 30
}

app_config = {
    "timeout": 60
}

user_config = {}

config = ChainMap(user_config, app_config, default_config)

while True:
    print("\n--- Configuration Manager ---")
    print("1. View Configuration")
    print("2. Set User Configuration")
    print("3. Delete User Configuration")
    print("4. Exit")

    choice = input("Enter choice (1-4): ")

    if choice == "1":
        print("\nCurrent Configuration:")
        for key, value in config.items():
            print(f"{key}: {value}")

    elif choice == "2":
        key = input("Enter setting name: ")
        value = input("Enter setting value: ")
        user_config[key] = value
        print("User setting added/updated.")

    elif choice == "3":
        key = input("Enter setting to delete: ")
        if key in user_config:
            del user_config[key]
            print("User setting removed.")
        else:
            print("Setting not found in user config.")

    elif choice == "4":
        print("Exiting program.")
        break

    else:
        print("Invalid choice! Try again.")
