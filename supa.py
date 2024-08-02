from typing import List
from supabase import create_client, Client
from os import getenv

supabase: Client = create_client(getenv("SUPABASE_URL"), getenv("SUPABASE_KEY"))


def supabase_upload_v1(
    year: int,
    month: int,
    day: int,
    url: str,
    hdurl: str,
    type: str,
    width: int,
    height: int,
    ratio: float,
    colors: List[str],
) -> None:
    try:
        (
            supabase.table("apods_v1")
            .insert(
                {
                    "year": year,
                    "month": month,
                    "day": day,
                    "url": url,
                    "hdurl": hdurl,
                    "type": type,
                    "width": width,
                    "height": height,
                    "ratio": ratio,
                    "colors": colors,
                }
            )
            .execute()
        )

    except Exception as exception:
        print(exception)
