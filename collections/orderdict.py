from collections import OrderedDict

inventory = OrderedDict()

while True:
    print("\n--- Product Inventory System ---")
    print("1. Add Product")
    print("2. Update Product Price")
    print("3. Delete Product")
    print("4. View Inventory")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        name = input("Enter product name: ")
        price = float(input("Enter product price: "))

        if name in inventory:
            print("Product already exists!")
        else:
            inventory[name] = price
            print("Product added successfully.")

    elif choice == "2":
        name = input("Enter product name to update: ")
        if name in inventory:
            new_price = float(input("Enter new price: "))
            inventory[name] = new_price
            print("Product price updated.")
        else:
            print("Product not found.")

    elif choice == "3":
        name = input("Enter product name to delete: ")
        if name in inventory:
            inventory.pop(name)
            print("Product removed.")
        else:
            print("Product not found.")

    elif choice == "4":
        if inventory:
            print("\nProduct Name   Price")
            print("--------------------")
            for product, price in inventory.items():
                print(f"{product:<14} ₹{price}")
        else:
            print("Inventory is empty.")

    elif choice == "5":
        print("Exiting program.")
        break

    else:
        print("Invalid choice! Try again.")
