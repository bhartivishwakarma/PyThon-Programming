from collections import deque

queue = deque()

while True:
    print("\n--- Customer Service Queue ---")
    print("1. Add Customer")
    print("2. Add VIP Customer")
    print("3. Serve Customer")
    print("4. View Queue")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        name = input("Enter customer name: ")
        queue.append(name)
        print(f"{name} added to the queue.")

    elif choice == "2":
        name = input("Enter VIP customer name: ")
        queue.appendleft(name)
        print(f"VIP {name} added to the front of the queue.")

    elif choice == "3":
        if queue:
            served = queue.popleft()
            print(f"Serving customer: {served}")
        else:
            print("Queue is empty!")

    elif choice == "4":
        if queue:
            print("Current Queue:")
            for person in queue:
                print(person)
        else:
            print("Queue is empty!")

    elif choice == "5":
        print("Exiting program. Thank you!")
        break

    else:
        print("Invalid choice! Try again.")
