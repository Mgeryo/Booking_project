from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("location, date_from, date_to, status_code", [
    ("Алтай", "2024-05-10", "2024-05-25", 200),
    ("Алтай", "2024-05-25", "2024-05-10", 400),
    ("Алтай", "2024-05-25", "2024-06-30", 400),

])
async def test_get_hotels_by_location_and_time(location, date_from, date_to, status_code, ac: AsyncClient):
    response = await ac.get(f"/hotels/{location}", params={
        "date_from": date_from,
        "date_to": date_to,
    })
    # print(ac.)
    assert response.status_code == status_code