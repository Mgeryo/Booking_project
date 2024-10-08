from fastapi import APIRouter, Depends
from pydantic import TypeAdapter
from app.bookings.dao import BookingDAO
from app.bookings.shemas import SBooking, SNewBooking
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exceptions import RoomCannotBeBooked

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user))-> list[SBooking]:
    return await BookingDAO.find_all(user_id = user.id)
    
@router.post("")
async def add_booking(
    booking: SNewBooking,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )
    if not booking:
        raise RoomCannotBeBooked
    booking = TypeAdapter(SNewBooking).validate_python(booking).model_dump()
    
    return booking


@router.delete("/{booking_id}")
async def remove_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user),
):
    await BookingDAO.delete(id=booking_id, user_id=current_user.id)