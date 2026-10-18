from abc import ABC, abstractmethod

class InvalidMeasurementError(ValueError):
    def __init__(self, dimension_name: str, measurement: float):
        self.dimension_name = dimension_name
        self.measurement = measurement

        message = (
            f"{dimension_name} deve ser um valor positivo, recebido {measurement}"
        )

        super().__init__(message)

class Shape(ABC):

    @staticmethod
    def _check_positive(dimension_name: str, measurement: float):
        if measurement <= 0:
            raise InvalidMeasurementError(dimension_name, measurement)

    @property
    @abstractmethod
    def area(self) -> float:
        pass

class Shape2d(Shape):

    @property
    @abstractmethod
    def perimeter(self) -> float:
        pass

class Shape3d(Shape):

    @property
    @abstractmethod
    def volume(self) -> float:
        pass

class Rectangle(Shape2d):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, width: float):
        self._check_positive("largura", width)
        self._width = width

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, height: float):
        self._check_positive("altura", height)
        self._height = height

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    @property
    def is_square(self) -> bool:
        return self.width == self.height

class Circle(Shape2d):

    PI = 3.1415

    def __init__(self, radius: float):
        self.radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, radius: float):
        self._check_positive("raio", radius)
        self._radius = radius

    @property
    def area(self) -> float:
        return self.PI * self.radius ** 2

    @property
    def perimeter(self) -> float:
        return 2 * self.PI * self.radius

class Prism(Shape3d):
    def __init__(self, base: Shape2d, height: float):
        self.base = base
        self.height = height

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, height: float):
        self._check_positive("altura", height)
        self._height = height

    @property
    def area(self) -> float:
        return (
            2 * self.base.area
            + self.height * self.base.perimeter
        )

    @property
    def volume(self) -> float:
        return self.base.area * self.height

class Cone(Shape3d):
    def __init__(self, base_radius: float, height: float):
        self._base = Circle(base_radius)
        self.height = height

    @property
    def base_radius(self) -> float:
        return self._base.radius

    @base_radius.setter
    def base_radius(self, base_radius: float):
        self._base.radius = base_radius

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, height: float):
        self._check_positive("altura", height)
        self._height = height

    @property
    def slant_height(self) -> float:
        return (
            self.base_radius ** 2
            + self.height ** 2
        ) ** 0.5

    @property
    def area(self) -> float:
        return (
            self._base.area
            + Circle.PI
            * self.base_radius
            * self.slant_height
        )

    @property
    def volume(self) -> float:
        return self._base.area * self.height / 3