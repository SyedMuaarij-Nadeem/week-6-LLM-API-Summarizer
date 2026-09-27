import os
from google import genai

MODEL_NAME = "gemini-3.8-flash"

def create_client():
    """Create and return a Gemini API client using environment variables."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    return genai.Client(api_key=api_key)

def validate_text(text):
    """Validate user-provided text."""
    text = text.strip()
    if not text:
        raise ValueError("Text cannot be empty.")
    if len(text.split()) < 20:
        raise ValueError("Please provide at least 20 words for summarization.")
    return text

def summarize_text(client, text):
    """Send text to Gemini and return a 3-point summary with prompt engineering."""
    prompt = f"""
You are a professional text summarization assistant.

Your task is to summarize the provided text.

Rules:
1. Produce exactly 3 bullet points.
2. Each bullet should contain one important idea.
3. Keep each bullet concise and informative.
4. Do not add information that is not present in the text.
5. Return only the 3 bullet points.
6. Do not include an introduction or conclusion.

TEXT:{text}
"""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        if not response.text:
            raise RuntimeError("The Gemini API returned an empty response.")
        return response.text
    except Exception as error:
        return f"API Error: {error}"

def main():
    print("=" * 60)
    print("           GEMINI AI TEXT SUMMARIZER")
    print("=" * 60)

    try:
        client = create_client()
        text = input("\nEnter a long paragraph to summarize:\n\n")
        text = validate_text(text)

        print("\nGenerating summary...\n")
        summary = summarize_text(client, text)

        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(summary)

    except ValueError as error:
        print(f"\nInput/Configuration Error: {error}")
    except Exception as error:
        print(f"\nUnexpected Error: {error}")

if __name__ == "__main__":
    main()
