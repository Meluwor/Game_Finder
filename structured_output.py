from typing import List
from pydantic import BaseModel, Field

class ItemInfo(BaseModel):
    item_name: str = Field(description="Name das ermitttelten Gegenstandes")
    genre: List[str] = Field(description="Ermittelte Genre['genre_name','genre_name']")
    release: str = Field(description="Erscheinungsjahr in format: yyyy-mm-dd")
    rating: float = Field(description="Bewertung von 1 bis 10")
    background_image_url: str = Field(description="Eine background_image_url")
    source:str = Field(description="Woher hast du diese Daten")
    rawg_game_id:str = Field(description="Wenn RAWG-API benutzt wurde default: leer")
    summary:str = Field(description="Eine kurze Zusammenfassung über diesen Gegenstand max: 950 Zeichen")



class ItemList(BaseModel):
    answer_to_user: str = Field(description="Freundliche Antwort im Stil das Game-Finder-Agenten")
    items: List[ItemInfo] = Field(description="Eine Liste der empfohlenen oder gefundenen Gegenstände")
    user_want_this: bool =Field(description="Der User hat sich dazu entschieden etwas vorgeschlagenes haben zu wollen")
    user_want_to_add:bool =Field(description="Der User hat sich dazu entschieden einen Gegenstand zu seinem Inventar zuzufügen")
    wanted_items:List[ItemInfo] = Field(description="Eine Liste der Gegenstände die der User seinem Inventar zufügen möchte")


