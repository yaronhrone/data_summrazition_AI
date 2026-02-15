import os
from openai import OpenAI, APIError, RateLimitError



client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_summary(article):
    """Generate a summary for the given article using OpenAI API."""
    try:
        prompt = f"""
        Provide a concise factual summary of the following text.

        Rules:
        - Only use information explicitly present in the provided text.
        - Do NOT infer, assume, or add external knowledge.
        - If the abstract lacks detail, acknowledge that limited information is available.
        - Maximum 2–3 sentences.

        Text:
        Title: {article.title}
        Abstract: {article.abstract}
        Author: {article.author}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional news editor. Provide a clear and neutral summary."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
        )

        return response.choices[0].message.content.strip()

    except RateLimitError:
        raise AIServiceError("AI quota exceeded.")

    except APIError as e:
        raise AIServiceError("AI service error.")

    except Exception:
        raise AIServiceError("Unexpected AI error.")

class AIServiceError(Exception):
    """Raised when AI service fails."""
    pass
