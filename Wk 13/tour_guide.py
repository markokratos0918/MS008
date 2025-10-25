"""AI Itinerary Recommender using Gemini API"""
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY or GEMINI_API_KEY == "Enter your API Key":
    print("❌ ERROR: GEMINI_API_KEY not found!")
    print("\nPlease follow these steps:")
    print("1. Go to https://aistudio.google.com/app/apikey")
    print("2. Create an API key")
    print("3. Create a .env file with: GEMINI_API_KEY=your_key_here")
    sys.exit()

genai.configure(api_key=GEMINI_API_KEY)

def instructor_chatbot():
    """Command-line AI Itinerary Chatbot using Gemini API."""   
    print("="*70)
    print("   Welcome to AI Itinerary Recommender (Powered by Gemini API)")
    print("="*70)
    print("\nAnswer a few questions to get personalized itinerary advice.\n")
    # Collect user inputs
    days = input("How many days: ")
    location = input("Where is the destination (city name): ")
    age = input("Enter your age: ")
    interests = input("Your interests (e.g., history, food, nature) [Optional]: ")
    budget = input("Budget level (budget/moderate/luxury) [Optional]: ")
    # Construct prompt
    prompt = f"""
You are a professional tourist recommender named Marko. Provide a detailed itinerary recommendation based on user data.
User Details:
- Duration: {days} days
- Destination: {location}
- Age: {age} years
- Budget: {budget if budget else 'Not specified'}
- Interests: {interests if interests else 'Not specified'}

Based on this personal information, create a structured itinerary following these guidelines:

1. For each day, provide maximum 3 activities (morning, afternoon, evening)
2. Include the name of the place, complete address, and a short description
3. Consider the user's age
4. Make sure activities are age-appropriate and logistically feasible
5. Format each day clearly with Day number as heading
6. Reply as if you are a tour guide of a tourism agent in Auckland
7. limits the number of probable words to 500 words
8. 200 tokens that signal the model to stop generating output
Present the itinerary in an organized, easy-to-read format.
"""
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')       
        # Configure generation parameters
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "max_output_tokens": 2048,
        }        
        print("\n" + "="*70)
        print("Generating your personalized itinerary...")
        print("="*70 + "\n")        
        # Generate response
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )        
        print("My Name is Marko, your AI Itinerary Expert:\n")
        print(response.text)        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify your API key at https://aistudio.google.com/app/apikey")
        print("2. Check your .env file contains: GEMINI_API_KEY=your_key")
        print("3. Ensure you have internet connection")

if __name__ == "__main__":
    instructor_chatbot()
