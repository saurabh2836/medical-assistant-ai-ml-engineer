from google import genai
from google.genai import types

GOOGLE_API_KEY ="AIzaSyC6vpxALcPou2trfG-1Ojv72H7pO3ZuipU"

client = genai.Client(api_key=GOOGLE_API_KEY)

with open('test.pdf', 'rb') as f:
    pdf_bytes = f.read()

    result = client.models.embed_content(
    model='gemini-embedding-2',
    contents=[
        types.Part.from_bytes(
            data=pdf_bytes,
            mime_type='application/pdf',
        ),
    ]
)

print(result.embeddings)