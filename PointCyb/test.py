class Point:
    x = 0
    y = 0

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def pair(self):
        return (self.x, self.y)        

monPoint = Point(10, 10)
print("Voici mon point: ", monPoint)
print("Voici ses coordonnees: ", monPoint.pair())
monPoint.move(5, -2)
print("Voici mon point apres le move: ", monPoint)
print("Voici ses coordonnees apres le move: ", monPoint.pair())
