from openapi import OpenAI
client = OpenAI()
def generate_random_sentence():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Please generate a random sentence"}],
        temperature = 0.8
    )
    sentence = response.choices[0].message.content
    return sentence