class food():
    def __init__(self,fruit,color):
        self.fruit = fruit
        self.color = color

    def show(self):
        print("fruit is: ", self.fruit)
        print("Color is: ", self.color)
apple = food("apple", "red")
grapes = food("grapes", "green")
apple.show()
grapes.show()

