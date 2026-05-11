from typing import List, Optional
from pydantic import BaseModel, Field


class ItemInfo(BaseModel):
    item_name: str = Field(description="Name das ermitttelten Gegenstandes")
    genres: Optional[List[str]] = Field(default=None,
                                        description="Ermittelte Genre['genre_name','genre_name']")
    release: Optional[str] = Field(default=None,
                                   description="Erscheinungsjahr")
    rating: Optional[float] = Field(default=None,
                                    description="Bewertung von 1 bis 5")
    background_image_url: Optional[str] = Field(default=None,
                                                description="Eine background_image_url zu diesem Gegenstand")
    source: Optional[str] = Field(default=None,
                                  description="Woher stammen diese Daten")
    rawg_game_id: Optional[str] = Field(
        default=None,
        description="Die echte RAWG-ID falls vorhanden, ansonsten leer lassen (None)."
    )
    summary: str = Field(description="Eine kurze Zusammenfassung über diesen Gegenstand max: 300 Zeichen")


class ItemList(BaseModel):
    answer_to_user: str = Field(description="Kurze Antwort für den User")
    new_items: List[ItemInfo] = Field(description="Eine Liste der neu gefundenen Gegenstände")
    user_want_this: bool = Field(default=False,
                                 description="True, wenn der User im Chat signalisiert, dass er an einen der vorgeschlagenen Gegenstände interessiert ist.")
    wanted_items: List[ItemInfo] = Field(
        default=[],
        description="Liste der konkreten Gegenstände, die der Nutzer haben oder seinem Inventar hinzufügen möchte."
    )
