import config
from openai import OpenAI

client = OpenAI(api_key=config.API_KEY)

def get_gpt_explanation(prompt):
    query = [{"role": "system", "content": "Eres Einnova AI, el asistente de IA del equipo de Einnova. Hablas en primera persona del plural y te diriges directamente al usuario."},
             {"role": "user", "content": prompt}]
    result = client.chat.completions.create(
        model="gpt-4o",
        messages=query,
        temperature=0.3
    )
    return result.choices[0].message.content
