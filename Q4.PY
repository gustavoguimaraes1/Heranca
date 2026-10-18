from abc import ABC, abstractmethod


class TaxCalculator:
    _INSS_BRACKETS = (
        (1621.00, 0.075),
        (2902.84, 0.09),
        (4354.27, 0.12),
        (8475.55, 0.14),
    )

    _IRRF_BRACKETS = (
        (2428.80, 0.00, 0.00),
        (2826.65, 0.075, 169.44),
        (3751.05, 0.15, 381.44),
        (4664.68, 0.225, 662.77),
        (float("inf"), 0.275, 896.00),
    )

    def __new__(cls):
        raise TypeError("TaxCalculator não pode ser instanciada.")

    @staticmethod
    def calculate_inss(gross: float) -> float:
        discount = 0.0
        previous_limit = 0.0

        for limit, rate in TaxCalculator._INSS_BRACKETS:
            if gross > previous_limit:
                taxable_amount = min(gross, limit) - previous_limit
                discount += taxable_amount * rate

            if gross <= limit:
                break

            previous_limit = limit

        return discount

    @staticmethod
    def calculate_irrf(
        gross: float,
        inss_discount: float
    ) -> float:

        calculation_base = gross - inss_discount

        for limit, rate, deduction in TaxCalculator._IRRF_BRACKETS:
            if calculation_base <= limit:
                tax = calculation_base * rate - deduction
                return max(tax, 0.0)

        return 0.0

class Employee(ABC):
    MINIMUM_WAGE = 1621.00
    WEEKLY_WORKING_HOURS = 44

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def gross_salary(self) -> float:
        pass

    def net_salary(self) -> float:
        gross = self.gross_salary()

        inss = TaxCalculator.calculate_inss(gross)

        irrf = TaxCalculator.calculate_irrf(
            gross,
            inss
        )

        return gross - inss - irrf

class SalariedEmployee(Employee):
    def __init__(self, name: str, monthly_salary: float):
        super().__init__(name)
        self.monthly_salary = monthly_salary

    @property
    def monthly_salary(self) -> float:
        return self._monthly_salary

    @monthly_salary.setter
    def monthly_salary(self, monthly_salary: float):
        if monthly_salary < Employee.MINIMUM_WAGE:
            raise ValueError(
                "O salário mensal não pode ser menor que o salário mínimo."
            )

        self._monthly_salary = monthly_salary

    def gross_salary(self) -> float:
        return self.monthly_salary

class CommissionEmployee(Employee):
    def __init__(
        self,
        name: str,
        base: float,
        sales: float,
        commission_rate: float
    ):
        super().__init__(name)

        self.base = base
        self.sales = sales
        self.commission_rate = commission_rate

    @property
    def base(self) -> float:
        return self._base

    @base.setter
    def base(self, base: float):
        if base < 0:
            raise ValueError(
                "O salário base não pode ser negativo."
            )

        self._base = base

    @property
    def sales(self) -> float:
        return self._sales

    @sales.setter
    def sales(self, sales: float):
        if sales < 0:
            raise ValueError(
                "O valor de vendas não pode ser negativo."
            )

        self._sales = sales

    @property
    def commission_rate(self) -> float:
        return self._commission_rate

    @commission_rate.setter
    def commission_rate(self, commission_rate: float):
        if commission_rate < 0.0 or commission_rate > 1.0:
            raise ValueError(
                "A taxa de comissão deve estar entre 0.0 e 1.0."
            )

        self._commission_rate = commission_rate

    def commission(self) -> float:
        return self.sales * self.commission_rate

    def gross_salary(self) -> float:
        salary = self.base + self.commission()

        return max(
            salary,
            Employee.MINIMUM_WAGE
        )

class HourlyEmployee(Employee):
    def __init__(
        self,
        name: str,
        hours: float,
        hourly_rate: float
    ):
        super().__init__(name)

        self.hours = hours
        self.hourly_rate = hourly_rate

    @staticmethod
    def _minimum_hourly_rate() -> float:
        monthly_hours = Employee.WEEKLY_WORKING_HOURS * 5

        return Employee.MINIMUM_WAGE / monthly_hours

    @property
    def hours(self) -> float:
        return self._hours

    @hours.setter
    def hours(self, hours: float):
        if hours < 0:
            raise ValueError(
                "As horas trabalhadas não podem ser negativas."
            )

        self._hours = hours

    @property
    def hourly_rate(self) -> float:
        return self._hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, hourly_rate: float):
        minimum = self._minimum_hourly_rate()

        if hourly_rate < minimum:
            raise ValueError(
                "O valor da hora não pode resultar em salário "
                "mensal abaixo do salário mínimo."
            )

        self._hourly_rate = hourly_rate

    def gross_salary(self) -> float:
        return self.hours * self.hourly_rate