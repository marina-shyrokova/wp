"""Command line interface to query the stock.

To iterate the source data you can use the following structure:

for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names) in the list.
"""

from data import warehouse1, warehouse2

def display_menu(menu):
    print ("Menu")
    for k, v in menu.items(): 
        print (f"{k}: {v}")

def order_item(item, total):
    if total == 0:
        return
    
    while True: 
        order = input("Would you like to order this item?(y/n): ").lower()
        if order== "n":
            break
        elif order == "y":
            try: 
                quantity = int(input("How many would you like? "))
                if quantity <= total:
                    print (f"{quantity} {item} have been placed")
                elif quantity <0:
                    print("Quantity must be grather than zero")
                else:
                    print(f"There are not this many available. The maximum amount that can be ordered is {total}")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            print ("Your answer has to be y or n")

name = input("Please provide your name: ")
print("Hello", name)

menu = {"1": "List items by warehouse", "2": "Search an item and place an order","3": "Quit" }

display_menu(menu)

choice = input("Make your choice: ").lower()

if choice == "1":
    print ("Warehouse1")
    for item_1 in warehouse1:
        print (item_1)
    print ("Warehouse2")
    for item_2 in warehouse2:
        print(item_2)

elif choice == "2":
    item = input("Write the item: ")

    count_1 = warehouse1.count(item)
    count_2 = warehouse2.count(item)
    total = count_1 + count_2

    print(f"Amount available: {total}")

    if item in warehouse1 and item in warehouse2:
        print(f"Location: Both warehouses")
        if count_1>count_2:
            print(f"Maximum availability:{count_1} in Warehouse 1")
        elif count_1<count_2:
            print(f"Maximum availability:{count_2} in Warehouse 2")
        else:
            print(f"Amount of {item} is equal in warehouse1 ({count_1}) and warehouse2 ({count_2})")
            
    elif item in warehouse1:
        print(f"The location of {item} in Warehouse1")

    elif item in warehouse2:
        print(f"The location of {item} in Warehouse2")    
    else:
        print("Not in stock")

    order_item(item, total)

elif choice == "3":
    pass
else:
    print("Invalid choice. Please select a valid option.")

print (f"Thank you for your visit, {name}!")







    

    




