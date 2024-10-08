import fileinput
import Homework

def main():
    double = [True, True, True, True, True,True,True]  
    single = [True, True, True, True, True,True]
    no_spicy = []  
    no_vegetables = []

    double_price = Homework.price_hamburger(*double) # Why I have to use * ?
    print(double_price)

main()