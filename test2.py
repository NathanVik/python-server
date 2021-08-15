

class Student:

    def __init__(self, name, age): #Class constructor with init method
        self.name = name
        self.age = age

    def say_hello(self):
        print("Hello there, my name is " + self.name)



print('********test 2**********')

student1 = Student('Nathan', 32)
student2 = Student('Sergio',35)
# print(student1)

student1.say_hello()
student2.say_hello()

print(student1.name)

student1.name = "New Name!"

print(student1.name)