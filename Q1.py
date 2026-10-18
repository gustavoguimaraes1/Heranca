class Employee:

    MINIMUM_WAGE: float = 1621.00

    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, salary):
        if salary < self.MINIMUM_WAGE:
            raise ValueError("O salário não pode estar abaixo do mínimo")

        self._salary = salary

    def get_salary(self):
        return self._salary

    def set_salary(self, salary):
        self.salary = salary

    def __str__(self) -> str:
        return f'Name: {self.name}, Salary: R$ {self._salary:.1f}'

class Manager(Employee):

    def __init__(self, name: str, salary: float, bonus: float):
        super().__init__(name, salary)
        self.bonus = bonus

    @property
    def bonus(self):
        return self._bonus

    @bonus.setter
    def bonus(self, bonus):
        if bonus < 0:
            raise ValueError("O bônus não pode ser negativo")

        self._bonus = bonus

    def get_bonus(self):
        return self._bonus

    def set_bonus(self, bonus):
        self.bonus = bonus

    def __str__(self) -> str:
        return (
            f'Name: {self.name}, '
            f'Salary: R$ {self._salary:.1f}, '
            f'Bonus: R$ {self._bonus:.1f}'
        )