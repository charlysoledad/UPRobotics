class Robot:
    name = ""
    speed = 0
    pollution = 0

    def __init__(self, name="War Machine", speed=8.5):
        self.speed = speed
        self.name = name
        self.distance = 0

    def walk(self,time):
        """ Multiply the speed with the time to obtain the distace and pollution """

        self.distance = self.speed * time
        Robot.pollution += (self.distance * 0.3)
        print("{} walked {} metros".format(self.name, self.distance))
        return Robot.pollution

    def __add__(self, instance):
        if isinstance(instance, Robot): 
            self.speed += instance.speed
            print("{} se comió a {}".format(self.name, instance.name))
        else:
            self.speed += instance

        return self

    def __radd__(self, instance):
        if isinstance(instance, Robot):
            self.speed += instance.speed
            print("{} se comió a {}".format(self.name, instance.name))
        else:
            self.speed += instance
        return self

    def __str__(self) -> str:
        name = 'A robot called {} with speed {}'.format(self.name,self.speed)
        return name

if __name__ == '__main__':
    # Test 1
    """ 
    botA = Robot()
    botB = Robot('Ixnamiki', 5.5)
    print(botA)
    print(botB)
    print("Pollution is: {}".format(Robot.pollution))
    botA.walk(3)
    print("Pollution is: {}".format(Robot.pollution))
    botB.walk(5)
    print("Pollution is: {}".format(Robot.pollution))
    botA = botA + botB
    print(botA) 
    """
    # Test 2
    
    botA = Robot()
    botB = Robot('Ixnamiki', 5.5)
    botB = botB + 5.5
    botB += 0.5
    print(botB)
    botB = 3 + botB
    print(botB)
    botA = 1 + botA + 1
    print(botA)
    botB = botA + botB
    print(botA)
