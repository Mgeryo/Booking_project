import asyncio
from datetime import date, datetime, timedelta
from typing import List, Optional
from fastapi_cache.decorator import cache
from fastapi import APIRouter, Query


from app.exceptions import CannotBookHotelForLongPeriod, DateFromCannotBeAfterDateTo
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelInfo

router = APIRouter(
    prefix="/hotels", 
    tags=["Отели"]
    )


@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
) -> List[SHotelInfo]:
    # await asyncio.sleep(3)
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod 
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    return hotels