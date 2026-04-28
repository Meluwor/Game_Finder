from openai import OpenAI
import os
from dotenv import load_dotenv
import json



load_dotenv()

API_KEY = os.getenv("OPENAI_GTP_KEY")
client = OpenAI(api_key=API_KEY)

#MODEL="gpt-4o-mini"
"""
möglicher ouutput:
{'strategies': [{'title': 'Civilization VI', 'rating': 89, 'price': 59.99, 'image_url': 'https://example.com/civilization_vi.jpg', 'publisher': '2K Games'}, {'title': 'StarCraft II', 'rating': 95, 'price': 39.99, 'image_url': 'https://example.com/starcraft_ii.jpg', 'publisher': 'Blizzard Entertainment'}, {'title': 'Total War: Three Kingdoms', 'rating': 84, 'price': 59.99, 'image_url': 'https://example.com/total_war_three_kingdoms.jpg', 'publisher': 'SEGA'}, {'title': 'Age of Empires IV', 'rating': 86, 'price': 59.99, 'image_url': 'https://example.com/age_of_empires_iv.jpg', 'publisher': 'Xbox Game Studios'}, {'title': 'XCOM 2', 'rating': 88, 'price': 39.99, 'image_url': 'https://example.com/xcom_2.jpg', 'publisher': '2K Games'}, {'title': 'Company of Heroes 2', 'rating': 82, 'price': 29.99, 'image_url': 'https://example.com/company_of_heroes_2.jpg', 'publisher': 'Sega'}, {'title': 'Wargroove', 'rating': 80, 'price': 19.99, 'image_url': 'https://example.com/wargroove.jpg', 'publisher': 'Chucklefish'}, {'title': 'Command & Conquer Remastered', 'rating': 85, 'price': 19.99, 'image_url': 'https://example.com/command_conquer_remastered.jpg', 'publisher': 'Electronic Arts'}, {'title': 'Anno 1800', 'rating': 87, 'price': 59.99, 'image_url': 'https://example.com/anno_1800.jpg', 'publisher': 'Ubisoft'}, {'title': 'Factorio', 'rating': 93, 'price': 29.99, 'image_url': 'https://example.com/factorio.jpg', 'publisher': 'Wube Software'}]}
datatype:  <class 'dict'>
"""
MODEL = "gpt-5-mini"
"""
möglicher ouutput:
{'bewertungsskala': '0-100', 'spiele': [{'titel': "Sid Meier's Civilization VI", 'bewertung': 88, 'preis': '59,99 €', 'image_url': 'https://example.com/images/civilization_vi.jpg', 'publisher': '2K'}, {'titel': 'Age of Empires II: Definitive Edition', 'bewertung': 84, 'preis': '19,99 €', 'image_url': 'https://example.com/images/age_of_empires_2_de.jpg', 'publisher': 'Xbox Game Studios'}, {'titel': 'StarCraft II', 'bewertung': 93, 'preis': 'Free-to-play', 'image_url': 'https://example.com/images/starcraft_ii.jpg', 'publisher': 'Blizzard Entertainment'}, {'titel': 'XCOM 2', 'bewertung': 88, 'preis': '39,99 €', 'image_url': 'https://example.com/images/xcom_2.jpg', 'publisher': '2K'}, {'titel': 'Total War: WARHAMMER II', 'bewertung': 86, 'preis': '59,99 €', 'image_url': 'https://example.com/images/total_war_warhammer_2.jpg', 'publisher': 'SEGA / Creative Assembly'}, {'titel': 'Crusader Kings III', 'bewertung': 88, 'preis': '49,99 €', 'image_url': 'https://example.com/images/crusader_kings_3.jpg', 'publisher': 'Paradox Interactive'}, {'titel': 'Stellaris', 'bewertung': 79, 'preis': '39,99 €', 'image_url': 'https://example.com/images/stellaris.jpg', 'publisher': 'Paradox Interactive'}, {'titel': 'Europa Universalis IV', 'bewertung': 88, 'preis': '39,99 €', 'image_url': 'https://example.com/images/europa_universalis_iv.jpg', 'publisher': 'Paradox Interactive'}, {'titel': 'Company of Heroes 2', 'bewertung': 78, 'preis': '19,99 €', 'image_url': 'https://example.com/images/company_of_heroes_2.jpg', 'publisher': 'SEGA / Relic Entertainment'}, {'titel': 'Command & Conquer Remastered Collection', 'bewertung': 82, 'preis': '19,99 €', 'image_url': 'https://example.com/images/command_and_conquer_remastered.jpg', 'publisher': 'Electronic Arts'}]}
datatype:  <class 'dict'>
"""

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