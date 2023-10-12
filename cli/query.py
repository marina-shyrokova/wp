"""Command line interface to query the stock.

To iterate the source data you can use the following structure:

for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names) in the list.
"""

from data import stock
from datetime import datetime as dt
from collections import Counter

def display_menu(menu):
    print ("Menu")
    for k, v in menu.items(): 
        print (f"{k}: {v}")

def get_item(input_item):
    lst_item = input_item.split(" ")

    if len(lst_item) == 3:
        category = " ".join([lst_item[0], lst_item[1]])
        state = lst_item[2]

    elif len (lst_item) ==2:
        category = lst_item[0]
        state = lst_item[1]
    else:
        raise ValueError("Input is not valid. Try again")

    return category.capitalize(), state.capitalize()

def search_item(item_input):
        try:
            item =" ".join(get_item(item_input))
            state, category = get_item(item_input)

            item_in_warehouse1= [i for i in warehouse1 if i["state"]==state and i["category"]==category]
            item_in_warehouse2= [i for i in warehouse2 if i["state"]==state and i["category"]==category]

            count_1 = len(item_in_warehouse1)
            count_2 = len(item_in_warehouse2)
            total = count_1 + count_2

            print(f"Amount available: {total}")
            print("Location:")
        
            today = dt.now().date()

            if count_1 or count_2:

                for i in item_in_warehouse1:
                    date_of_stock = dt.strptime(i["date_of_stock"].split()[0],'%Y-%m-%d').date()
                    days_in_stock = (today - date_of_stock).days 
                    print(f"- Warehouse 1 (in stock for {days_in_stock} days)")
                for j in item_in_warehouse2:
                    date_of_stock = dt.strptime(j["date_of_stock"].split()[0],'%Y-%m-%d').date()
                    days_in_stock = (today - date_of_stock).days 
                    print(f"- Warehouse 2 (in stock for {days_in_stock} days)")

                if count_1>count_2:
                    print(f"Maximum availability:{count_1} in Warehouse 1")
                elif count_1<count_2:
                    print(f"Maximum availability:{count_2} in Warehouse 2")
                else:
                    print(f"Maximum availability: equal in warehouse1 ({count_1}) and warehouse2 ({count_2})")
        
            else:
                print("Not in stock")

            order_item(item, total)

        except ValueError:
            print('Input valid. The item has to include state and category')


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
                    break
                elif quantity <0:
                    print("Quantity must be grather than zero")
                else:
                    print(f"There are not this many available. The maximum amount that can be ordered is {total}")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            print ("Your answer has to be y or n")

def sort_of_warehouse(stock):
    warehouse1 = [i for i in stock if i.get("warehouse") == 1]
    warehouse2 = [i for i in stock if i.get("warehouse") == 2]
    return warehouse1, warehouse2

warehouse1, warehouse2 = sort_of_warehouse(stock)

name = input("Please provide your name: ")
print("Hello", name)

menu = {"1": "List items by warehouse", "2": "Search an item and place an order","3": "Browse by category", "4": "Quit" }

display_menu(menu)

choice = input("Make your choice: ")

if choice == "1":

    print ("Warehouse1\n")
    for item in warehouse1:
            print(item['state'] +" "+ item["category"])
    print ("\nWarehouse2\n")
    for item in warehouse2:
            print(item['state'] +" "+ item["category"])

    print("\nTotal items in warehouse 1", len(warehouse1))
    print("Total items in warehouse 2:", len(warehouse2))

    
elif choice == "2":
    item_input = input("What is the name of the item? ")
    search_item(item_input)

    
elif choice == "3":
    categories = []
    for item in stock:
        categories.append(item["category"])

    count = Counter(categories)

    summary_of_categories = []

    i = 1
    for k, v in count.items():
        summary_of_categories.append((i, k, v))
        i+=1

    for i in summary_of_categories:
        print(f"{i[0]}. {i[1]} ({i[2]})")
              
    
    number_of_category = int(input("Type the number of the category to browse: "))

    selected_category = None

    for category_info in summary_of_categories:
        if number_of_category == category_info[0]:
            selected_category = category_info[1]
            break                           

    print("\nList of laptops available:")

    for i in stock:
        if i['category'] == selected_category:
            selected_state = i["state"]
            selected_warehouse = i["warehouse"]
            print(f"{selected_state} {selected_category.lower()}, Warehouse {selected_warehouse}")

elif choice == "4":
    pass
else:
    print("Invalid choice. Please select a valid option.")

print (f"\nThank you for your visit, {name}!")






    

    




