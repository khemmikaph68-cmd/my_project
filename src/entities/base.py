import pygame

class Entity:
    """Base class สำหรับวัตถุในเกม (โชว์ Inheritance และ Encapsulation)"""
    def __init__(self, x, y):
        # Encapsulation: ซ่อนตัวแปรไว้ภายใน (Protected/Private)
        self._x = x  
        self._y = y

    # ใช้ Property เป็น Getter/Setter 
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def update(self, dt, *args, **kwargs):
        """Method ว่างเปล่า เพื่อให้ Subclass นำไป Override (โชว์ Polymorphism)"""
        pass

    def draw(self, surface):
        """Method ว่างเปล่า เพื่อให้ Subclass นำไป Override (โชว์ Polymorphism)"""
        pass