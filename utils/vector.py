import math

class Vector2:
    def __init__(self, x: int, y: int):
        self.X = x
        self.Y = y

    def __sub__(self, another):
        if isinstance(another, Vector2):
            return Vector2(self.X - another.X, self.Y - another.Y)
        return NotImplemented

    def __add__(self, another):
        if isinstance(another, Vector2):
            return Vector2(self.X + another.X, self.Y + another.Y)
        return NotImplemented

    def __mul__(self, another):
        if isinstance(another, Vector2):
            return self.X * another.X + self.Y * another.Y
        elif not isinstance(another, Vector2):
            return Vector2(self.X * another, self.Y * another)
        else:
            return NotImplemented

    def __truediv__(self, value):
        return Vector2(self.X / value, self.Y / value)

    def __pow__(self, value):
        return Vector2(self.X / value, self.Y / value)

    def __floordiv__(self, value):
        return Vector2(self.X // value, self.Y // value)

    def __mod__(self, value):
        return Vector2(self.X % value, self.Y % value)

    def __repr__(self) -> str:
        return f"[{self.X}, {self.Y}]"    
    
    # Métodos
    @property
    def Magnitude(self):
        return math.sqrt(self.X ** 2 + self.Y ** 2)
