
def queryai(input):
    messages = [
        {"role":"system",
         "content":""" As a product description generator, generate a multiparagraph rich text product descrition with emojeis from the info provided to you '\n"""},
    ]

    messages.append({"Role": "user", "content":f"{input}"})
    completion = openai.ChatCompletion.Create(
        model = "gpt-3.5-turbo",
        messages=messages
    )

    reply = completion.choices[0].messages.content
    return reply