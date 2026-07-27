from core.models import CarListing


def matches(car: CarListing) -> bool:

    if car.price > 20000:
        return False

    if car.year < 2019:
        return False

    if car.mileage > 120000:
        return False

    fuel = car.fuel.lower()

    if "hybrid" not in fuel and "hybridi" not in fuel:
        return False

    subtitle = car.subtitle.lower()

    if "330e" not in subtitle:
        return False

    return True