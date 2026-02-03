"""
Story Generator using Gemma:2b and LangChain
Generates creative stories based on user-provided characters, place, and story type
"""

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

def get_user_inputs():
    """Get story parameters from user"""
    print("=" * 60)
    print("STORY GENERATOR".center(60))
    print("=" * 60)
    
    # Get number of characters
    while True:
        try:
            num_characters = int(input("\nHow many characters in the story? "))
            if num_characters > 0:
                break
            print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")
    
    # Get character names
    characters = []
    print(f"\nEnter {num_characters} character name(s):")
    for i in range(num_characters):
        name = input(f"  Character {i+1}: ").strip()
        if name:
            characters.append(name)
    
    # Get place
    place = input("\nWhere does the story take place? ").strip()
    
    # Get story type
    print("\nWhat type of story?")
    print("  1. Adventure")
    print("  2. Mystery")
    print("  3. Romance")
    print("  4. Horror")
    print("  5. Fantasy")
    print("  6. Sci-Fi")
    print("  7. Comedy")
    
    story_types = {
        '1': 'Adventure',
        '2': 'Mystery',
        '3': 'Romance',
        '4': 'Horror',
        '5': 'Fantasy',
        '6': 'Sci-Fi',
        '7': 'Comedy'
    }
    
    choice = input("Enter choice (1-7): ").strip()
    story_type = story_types.get(choice, 'Adventure')
    
    return characters, place, story_type


def create_story_prompt():
    """Create the prompt template for story generation"""
    template = """You are a creative story writer. Write an engaging {story_type} story.

Story Details:
- Characters: {characters}
- Setting: {place}
- Genre: {story_type}

Write a complete short story (300-500 words) with a beginning, middle, and end. 
Make it exciting and engaging!

Story:"""
    
    return PromptTemplate(
        input_variables=["characters", "place", "story_type"],
        template=template
    )


def generate_story(characters, place, story_type):
    """Generate story using Gemma:2b model with streaming output"""
    try:
        # Initialize Ollama with Gemma:2b model
        llm = OllamaLLM(
            model="gemma:2b",
            temperature=0.8
        )

        # Create prompt template
        prompt = create_story_prompt()

        # Create chain
        chain = prompt | llm

        # Format characters
        characters_str = ", ".join(characters)

        print("\n" + "=" * 60)
        print("Generating your story (streaming)...".center(60))
        print("=" * 60 + "\n")

        story_chunks = []

        # 🔥 STREAMING HERE
        for chunk in chain.stream({
            "characters": characters_str,
            "place": place,
            "story_type": story_type
        }):
            print(chunk, end="", flush=True)   # live output
            story_chunks.append(chunk)

        print("\n" + "=" * 60)

        return "".join(story_chunks)

    except Exception as e:
        return (
            f"Error generating story: {str(e)}\n\n"
            "Make sure Ollama is running and gemma:2b model is installed.\n"
            "Run: ollama pull gemma:2b"
        )

def main():
    """Main function"""
    while True:
        # Get user inputs
        characters, place, story_type = get_user_inputs()
        
        # Generate story
        story = generate_story(characters, place, story_type)
        
        # Display story
        print("\n" + "=" * 60)
        print(f"{story_type.upper()} STORY".center(60))
        print("=" * 60)
        print(f"\nCharacters: {', '.join(characters)}")
        print(f"Place: {place}")
        print(f"Genre: {story_type}")
        print("\n" + "-" * 60)
    
        print("-" * 60)
        
        # Ask if user wants to generate another story
        print("\n")
        again = input("Generate another story? (yes/no): ").strip().lower()
        if again not in ['yes', 'y']:
            print("\nThank you for using Story Generator! Goodbye!")
            break


if __name__ == "__main__":
    main()