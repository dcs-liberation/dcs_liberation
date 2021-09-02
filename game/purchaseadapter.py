from abc import abstractmethod
from typing import TypeVar, Generic, Any

from game import Game
from game.coalition import Coalition
from game.dcs.aircrafttype import AircraftType
from game.dcs.groundunittype import GroundUnitType
from game.dcs.unittype import UnitType
from game.squadrons import Squadron
from game.theater import ControlPoint

ItemType = TypeVar("ItemType")


class TransactionError(RuntimeError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class PurchaseAdapter(Generic[ItemType]):
    def __init__(self, coalition: Coalition) -> None:
        self.coalition = coalition

    def buy(self, item: ItemType, quantity: int) -> None:
        for _ in range(quantity):
            if self.has_pending_sales(item):
                self.do_cancel_sale(item)
            elif self.can_buy(item):
                self.do_purchase(item)
            else:
                raise TransactionError(f"Cannot buy more {item}")
            self.coalition.adjust_budget(-self.price_of(item))

    def sell(self, item: ItemType, quantity: int) -> None:
        for _ in range(quantity):
            if self.has_pending_orders(item):
                self.do_cancel_purchase(item)
            elif self.can_sell(item):
                self.do_sale(item)
            else:
                raise TransactionError(f"Cannot sell more {item}")
            self.coalition.adjust_budget(self.price_of(item))

    def has_pending_orders(self, item: ItemType) -> bool:
        return self.pending_delivery_quantity(item) > 0

    def has_pending_sales(self, item: ItemType) -> bool:
        return self.pending_delivery_quantity(item) < 0

    @abstractmethod
    def current_quantity_of(self, item: ItemType) -> int:
        ...

    @abstractmethod
    def pending_delivery_quantity(self, item: ItemType) -> int:
        ...

    def expected_quantity_next_turn(self, item: ItemType) -> int:
        return self.current_quantity_of(item) + self.pending_delivery_quantity(item)

    def can_buy(self, item: ItemType) -> bool:
        return self.coalition.budget >= self.price_of(item)

    def can_sell_or_cancel(self, item: ItemType) -> bool:
        return self.can_sell(item) or self.has_pending_orders(item)

    @abstractmethod
    def can_sell(self, item: ItemType) -> bool:
        ...

    @abstractmethod
    def do_purchase(self, item: ItemType) -> None:
        ...

    @abstractmethod
    def do_cancel_purchase(self, item: ItemType) -> None:
        ...

    @abstractmethod
    def do_sale(self, item: ItemType) -> None:
        ...

    @abstractmethod
    def do_cancel_sale(self, item: ItemType) -> None:
        ...

    @abstractmethod
    def price_of(self, item: ItemType) -> int:
        ...

    @abstractmethod
    def name_of(self, item: ItemType, multiline: bool = False) -> str:
        ...

    @abstractmethod
    def unit_type_of(self, item: ItemType) -> UnitType[Any]:
        ...


class AircraftPurchaseAdapter(PurchaseAdapter[Squadron]):
    def __init__(self, control_point: ControlPoint) -> None:
        super().__init__(control_point.coalition)
        self.control_point = control_point

    def pending_delivery_quantity(self, item: Squadron) -> int:
        return item.pending_deliveries

    def current_quantity_of(self, item: Squadron) -> int:
        return item.owned_aircraft

    def can_buy(self, item: Squadron) -> bool:
        return super().can_buy(item) and self.control_point.unclaimed_parking() > 0

    def can_sell(self, item: Squadron) -> bool:
        return item.untasked_aircraft > 0

    def do_purchase(self, item: Squadron) -> None:
        item.pending_deliveries += 1

    def do_cancel_purchase(self, item: Squadron) -> None:
        item.pending_deliveries -= 1

    def do_sale(self, item: Squadron) -> None:
        item.untasked_aircraft -= 1
        item.pending_deliveries -= 1

    def do_cancel_sale(self, item: Squadron) -> None:
        item.untasked_aircraft += 1
        item.pending_deliveries += 1

    def price_of(self, item: Squadron) -> int:
        return item.aircraft.price

    def name_of(self, item: Squadron, multiline: bool = False) -> str:
        if multiline:
            separator = "<br />"
        else:
            separator = " "
        return separator.join([item.aircraft.name, str(item)])

    def unit_type_of(self, item: Squadron) -> AircraftType:
        return item.aircraft


class GroundUnitPurchaseAdapter(PurchaseAdapter[GroundUnitType]):
    def __init__(
        self, control_point: ControlPoint, coalition: Coalition, game: Game
    ) -> None:
        super().__init__(coalition)
        self.control_point = control_point
        self.game = game

    def pending_delivery_quantity(self, item: GroundUnitType) -> int:
        return self.control_point.ground_unit_orders.pending_orders(item)

    def current_quantity_of(self, item: GroundUnitType) -> int:
        return self.control_point.base.total_units_of_type(item)

    def can_buy(self, item: GroundUnitType) -> bool:
        return super().can_buy(item) and self.control_point.has_ground_unit_source(
            self.game
        )

    def can_sell(self, item: GroundUnitType) -> bool:
        return False

    def do_purchase(self, item: GroundUnitType) -> None:
        self.control_point.ground_unit_orders.order({item: 1})

    def do_cancel_purchase(self, item: GroundUnitType) -> None:
        self.control_point.ground_unit_orders.sell({item: 1})

    def do_sale(self, item: GroundUnitType) -> None:
        raise TransactionError("Sale of ground units not allowed")

    def do_cancel_sale(self, item: GroundUnitType) -> None:
        raise TransactionError("Sale of ground units not allowed")

    def price_of(self, item: GroundUnitType) -> int:
        return item.price

    def name_of(self, item: GroundUnitType, multiline: bool = False) -> str:
        return f"{item}"

    def unit_type_of(self, item: GroundUnitType) -> GroundUnitType:
        return item
