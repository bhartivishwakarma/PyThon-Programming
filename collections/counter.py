from collections import Counter

text = ""
word_counter = Counter()

while True:
    print("\n--- Text Analyzer ---")
    print("1. Enter Text")
    print("2. View Word Frequencies")
    print("3. Most Common Words")
    print("4. Search Word Count")
    print("5. Exit")

    choice = input("Enter choice (1-5): ")

    if choice == "1":
        text = input("Enter text:\n").lower()
        words = text.split()
        word_counter = Counter(words)
        print("Text analyzed successfully.")

    elif choice == "2":
        if word_counter:
            print("\nWord Frequencies:")
            for word, count in word_counter.items():
                print(f"{word}: {count}")
        else:
            print("No text analyzed yet.")

    elif choice == "3":
        if word_counter:
            n = int(input("How many top words? "))
            print("\nMost Common Words:")
            for word, count in word_counter.most_common(n):
                print(f"{word}: {count}")
        else:
            print("No text analyzed yet.")

    elif choice == "4":
        word = input("Enter word to search: ").lower()
        print(f"'{word}' appears {word_counter[word]} times.")

    elif choice == "5":
        print("Exiting program.")
        break

    else:
        print("Invalid choice! Try again.")
