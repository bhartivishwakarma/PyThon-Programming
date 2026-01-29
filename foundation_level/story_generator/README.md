# Story Generator with Gemma:2b and LangChain

A Python program that generates creative stories using the Gemma:2b language model and LangChain.

## Features
- Input number of characters and their names
- Specify story location/place
- Choose from 7 story types (Adventure, Mystery, Romance, Horror, Fantasy, Sci-Fi, Comedy)
- Generates engaging 300-500 word stories

## Prerequisites

1. **Install Ollama**
   - Download from: https://ollama.ai
   - Install for your OS

2. **Pull Gemma:2b model**
   ```bash
   ollama pull gemma:2b
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start Ollama** (in a separate terminal)
   ```bash
   ollama serve
   ```

2. **Run the program**
   ```bash
   python story_generator.py
   ```

3. **Follow the prompts:**
   - Enter number of characters
   - Enter each character's name
   - Enter the story location
   - Choose story type (1-7)

## Example

```
How many characters in the story? 2

Enter 2 character name(s):
  Character 1: Alice
  Character 2: Bob

Where does the story take place? Ancient Egypt

What type of story?
  1. Adventure
  ...
Enter choice (1-7): 1
```

The program will generate a unique adventure story with Alice and Bob in Ancient Egypt!

## Notes
- Make sure Ollama is running before starting the program
- You can generate multiple stories in one session
- Temperature is set to 0.8 for creative outputs
