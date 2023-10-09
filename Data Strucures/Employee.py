class Employee:
    'Common base class for all employees'
    empCount = 0

    def __init__(self, name, salary):
        self.__name = name
        self.__salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print("Total Employee %d" % Employee.empCount)

    def displayEmployee(self):
        print("Name : ", self.__name, ", Salary: ", self.__salary)

# This would create the first object of the Employee class
emp1 = Employee("Zara", 2000)

# This would create the second object of the Employee class
emp2 = Employee("Manni", 5000)

emp1.displayEmployee()
emp2.displayEmployee()
print("Total Employee %d" % Employee.empCount)
