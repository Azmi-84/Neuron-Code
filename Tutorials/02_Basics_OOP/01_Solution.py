# Object-Oriented Programming (OOP) Basics in Python

# Class Definition
# Class names should start with a capital letter
class Car:
    totalCar = 0  # Class variable
    
    def __init__(self, userBrand, userModel):
        """
        The __init__() function is called automatically when a new object is created.
        The '__' prefix makes a variable private.
        """
        self.__brand = userBrand
        self.__model = userModel
        Car.totalCar += 1  # Increment class variable

    def fullName(self):
        return f"{self.__brand} {self.__model}"
    
    def get_brand(self):
        return self.__brand + "!"
    
    def fuel_type(self):
        return "Petrol or Diesel"
    
    def __str__(self):
        """
        Provides a meaningful string representation when using print().
        """
        return f"Car(Brand: {self.__brand}, Model: {self.__model})"
    
    @staticmethod
    def general_description():
        """
        A static method does not access 'self' and belongs to the class itself.
        """
        return "Car means transportation!!!"
    
    @property
    def model(self):
        return self.__model

# Inheritance - Subclass Example
class ElectricCar(Car):
    def __init__(self, brand, model, battery_size):
        super().__init__(brand, model)
        self.battery_size = battery_size
        
    def fuel_type(self):
        return "Electric Charge"

# Creating instances
firstCar = Car("Toyota", "Corolla")
print(firstCar)  # Prints meaningful info
print(firstCar.get_brand())  # Access private attribute using getter method
print(firstCar.model)  # Accessing model using @property
print(firstCar.fullName())

secondCar = Car("CLICK", "Plug")
print(secondCar.get_brand())

thirdCar = ElectricCar("Tesla", "Model S", "90kWH")
print(thirdCar.get_brand())
print(thirdCar.fullName())

print(firstCar.fuel_type())  # Calls parent class method
print(thirdCar.fuel_type())  # Overridden method in ElectricCar

# Checking total number of car instances
print(Car.totalCar)

# Another instance increases the count
ElectricCar("Huaw", "ERT", "945kWH")

print(firstCar.general_description())  # Calling static method

# Read-only property example
print(firstCar.model)

# Checking instance types
print(isinstance(thirdCar, Car))  # True
print(isinstance(thirdCar, ElectricCar))  # True

# Multiple Inheritance Example
class Battery:
    def battery_info(self):
        return "This is Battery!!!"

class Engine:
    def engine_info(self):
        return "This is Engine!!!"

class ElectricCarTwo(Battery, Engine, Car):
    pass

fourthCar = ElectricCarTwo("Tesla", "Q Model")

print(fourthCar.battery_info())  # Inherited from Battery
print(fourthCar.engine_info())  # Inherited from Engine
