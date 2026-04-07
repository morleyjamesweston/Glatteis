from ollama import generate

for _ in range(10):
    response = generate(
        model="gemma3:1b",
        prompt="please just repeat the word 'interrogation', but misspelled slightly Do not add anything else.",
        keep_alive=10.0,
    )
    print(response.response)
