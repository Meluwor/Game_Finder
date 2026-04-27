from openai import OpenAI
import os
from dotenv import load_dotenv
import json



load_dotenv()

API_KEY = os.getenv("OPENAI_GTP_KEY")
client = OpenAI(api_key=API_KEY)

MODEL="gpt-4o-mini"
#MODEL = "gpt-5-mini"

RESPONSE_FORMAT = {"type": "json_object"} # erzwingt JSON-Ausgabe



def abc():
    prompt = "Geb mir mal eine Liste der 10 beliebtesten Srategiepiele deren rating, pries,,image-URL und publisher in form eines JSON"

    # TODO die image-URL wird hier frei erfunden
    # preise sind relativ zu sehen da sie veraltet sein können
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        #model="gpt-5-mini",
        input="geb mir mal eine liste der 10 beliebtesten strategiepielen und deren rating pries,image-URL und publisher in form eines python dict"
    )

    print(response)
    print(response.output_text)

    for key in response:
        print(key)
        pass

    """
    response = client.chat.completions.create(

        model=MODEL,
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher Assistent, der nur valides JSON ausgibt."},
            {"role": "user", "content": prompt}
        ],
        response_format = RESPONSE_FORMAT
    )
    content = response.choices[0].message.content
    # print(content)

    data = json.loads(content)
    print(data)
    print("datatype: ", type(data))




def main():
    print("start")
    abc()

if __name__ == "__main__":
    main()


def check_data(data):
    """
    This function shall ensure that the user will get game data not something else.
    """
    pass