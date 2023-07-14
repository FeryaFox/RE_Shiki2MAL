from pydantic import BaseModel, Field


class ARMResult(BaseModel):
    anidb: int | None
    anilist: int | None
    anime_planet: str | None = Field(alias="anime-planet")
    anisearch: int | None
    imdb: str | None
    kitsu: int | None
    livechart: int | None
    notify_moe: str | None = Field(alias="notify-moe")
    themoviedb: str | None
    thetvdb: int | None
    myanimelist: int | None
