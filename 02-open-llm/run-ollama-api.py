from openai import OpenAI
import tiktoken
import sys
clientO = OpenAI(
       base_url='http://localhost:11434/v1/',
       api_key='ollama',
    )


def llm_ollama(prompt):
    response = clientO.chat.completions.create(
        model='gemma:2b',
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content

prompt = sys.argv[1]

response = llm_ollama(prompt)
encoding = tiktoken.encoding_for_model("gpt-4o")

print(f"Answer tokens: {len(encoding.encode(response))}")

print()
print()

print(response)
