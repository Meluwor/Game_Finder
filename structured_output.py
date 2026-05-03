from typing import List
from pydantic import BaseModel, Field

class ItemInfo(BaseModel):
    item_name: str = Field(description="Name das ermitttelten Gegenstandes")
    genre: List[str] = Field(description="Ermittelte Genre['genre_name','genre_name']")
    release: str = Field(description="Erscheinungsjahr")
    rating: float = Field(description="Bewertung von 1 bis 10")
    background_image_url: str = Field(description="Eine background_image_url")
    summary:str = Field(description="Eine kurze Zusammenfassung über diesen Gegenstand max: 950 Wörter")
    source:str = Field(description="Woher hast du diese Daten")
    rawg_game_id:str = Field(description="Wenn RAWG-API benutzt wurde")


class ItemList(BaseModel):
    items: List[ItemInfo] = Field(description="Eine Liste der empfohlenen oder gefundenen Gegenstände")
    reason: str = Field(description="Eine kurze Beschreibung wie du zu diesem Ergebniss gekommen bist")
