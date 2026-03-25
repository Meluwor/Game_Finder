from openai import OpenAI
import os
from dotenv import load_dotenv



load_dotenv()

API_KEY = os.getenv("OPENAI_GTP_KEY")


client = OpenAI(api_key=API_KEY)



response = client.responses.create(
    #TODO testen von 5mini etc
    model="gpt-4o-mini",
    input="geb mir mal eine liste der 10 beliebtesten strategiepielen und deren rating pries und publisher in form eines python dict"
)

print(response)
print(response.output_text)
"""
for key in response:
    print(key)
    pass

"""





def main():
    print("start")

if "__name__" == "_main_":
    main()
