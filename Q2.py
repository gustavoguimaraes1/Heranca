from abc import ABC, abstractmethod

class Customer(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def discount(self, amount: float) -> float:
        pass

    def final_price(self, amount: float) -> float:
        return amount - self.discount(amount)

class Sale:
    def __init__(self, customer: Customer, amount: float):
        self.customer = customer
        self.amount = amount

    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, customer):
        self._customer = customer

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, amount: float):
        if amount <= 0:
            raise ValueError("O valor da compra deve ser maior que zero.")

        self._amount = amount

    @property
    def discount(self) -> float:
        return self.customer.discount(self.amount)

    @property
    def final_price(self) -> float:
        return self.customer.final_price(self.amount)

class RegularCustomer(Customer):
    def discount(self, amount: float) -> float:
        return 0.0


class SilverMember(Customer):
    DISCOUNT_RATE: float = 0.05

    def discount(self, amount: float) -> float:
        return amount * self.DISCOUNT_RATE


class GoldMember(Customer):
    DISCOUNT_RATE: float = 0.10
    MINIMUM_PURCHASE: float = 100.00

    def discount(self, amount: float) -> float:
        if amount >= self.MINIMUM_PURCHASE:
            return amount * self.DISCOUNT_RATE

        return 0.0

class VipMember(Customer):
    DISCOUNT_RATE: float = 0.15
    MAX_DISCOUNT: float = 500.00

    def discount(self, amount: float) -> float:
        discount = amount * self.DISCOUNT_RATE

        if discount > self.MAX_DISCOUNT:
            return self.MAX_DISCOUNT

        return discount