import os
from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_summary(article):
    """Generate a summary for the given article using OpenAI API."""
    prompt = f"""
    Summarize the following news article in 3-4 concise sentences.

    Title: {article.title}
    Author: {article.author}
    Section: {article.section_name}

    Abstract:
    {article.abstract}
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