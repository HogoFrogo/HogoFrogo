# add fly
flies = [0]
sample_object = Human(35) # object
sample_object = human(35) # function
sample_object = Human.karel()
print(Human.n_humans)
pavel = Human2("Pavel Hrášek")
# franta = Human2("František Palatka")

print(pavel.name)
pavel.health -=50
pavel.ublizSi(50)
pavel.prdniSi()

pavel.jump()
like = True
# 30 FPS -> 30x za vteřinu se provede tenhle cyklus

while True:
    pavel.x += 2
    view_image(pavel.image,pavel.x,pavel.y)
    check_collisions(pavel)


def check_collisions(human):
    if human.x >50:
        human.die()

# when I want to take a shit
class Human2():
    image = "person.jpg"
    x = 23
    y = 434
    name = ""
    health = 100
    def __init__(self, some_shitty_word):
        self.name = some_shitty_word
        print("Human was born")
    def die(self):
        print("Hoewjhfdjs")
    def jump(self):
        print("jump")
    def prdniSi(self):
        print(self.name + " si prdnul")

class Human():
    age
    height
    n_humans = 0
    def karel(self,age):
        self.age = age
        n_humans += 1
    def takeAShit():
        print("shit")



fly = Fly()
# move fly
# kill fly