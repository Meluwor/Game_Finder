from pydantic import BaseModel, Field

class StructuredOutput(BaseModel):
    game_name: str = Field(description="Name das ermitttelten Gegenstandes")
    genre: str = Field(description="Ermitteltes Genre")
    release: str = Field(description="Erscheinungsjahr")
    rating: int = Field(description="Bewertung von 1 bis 10")
    background_image_url: str = Field(description="Eine background_image_url ")
    summary:str = Field(description="Eine kurze Zusammenfassung max: 950 Wörter")




