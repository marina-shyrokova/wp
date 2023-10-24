from data import personnel
from loader import Loader
from datetime import datetime as dt
from collections import Counter
from classes import User, Warehouse, Item, Employee

stock = Loader(model="stock")

def display_menu(menu):
    print ("Menu")
    for k, v in menu.items(): 
        print (f"{k}: {v}")

def get_selected_operation():
        selected_operation = input("Make your choice: ")
        return selected_operation
 
def list_items_by_warehouse():
    count_of_items = {}
    
    for warehouse in stock:
        item_count = len(warehouse.stock)
        count_of_items[f'warehouse {warehouse.warehouse_id}'] = item_count
        print(f"Warehouse ID: {warehouse.warehouse_id}\n")
        for item in warehouse.stock:
                print (item.state, item.category)

    for warehouse in stock:
        print(f"Total items in Warehouse {warehouse.warehouse_id}: {warehouse.occupancy}")

    return f"Listed {sum(count_of_items.values())} items."

def search_and_order_item():

    try:
        item_input = input("What is the name of the item? ")

        if item_input.isdigit():
            print("The name of the item doesn't include numbers")
        
        selected_item = item_input.capitalize()
        today = dt.now().date()

        info_of_item = []
        count = {}

        for warehouse in stock:
            temp = 0
            for item in warehouse.stock:     
                if item.__str__().lower() == item_input.lower():
                    temp += 1
                    count[f'Warehouse {warehouse.warehouse_id}'] = temp
                    date_of_stock = dt.strptime(item.date_of_stock.split()[0],'%Y-%m-%d').date()
                    days_in_stock = (today - date_of_stock).days 
                    info_of_item.append({f"- Warehouse {warehouse.warehouse_id}" : f"(in stock for {days_in_stock} days)"})

        total = len(info_of_item)

        print(f"Amount available: {total}")

        print("Location:")

        if total > 0:

            for item in info_of_item:
                for k,v in item.items():
                    print(k, v)

            maximum_in_warehouse = [(k, v) for k,v in count.items() if v == max(v for v in count.values())]

            max_wrh, max_item = maximum_in_warehouse[0]
        
            print (f"\nMaximum availability: {max_item} in {max_wrh}")

            order = input("Would you like to order this item?(y/n): ").lower()
            if order== "n":
                return f"Search a {selected_item}"
            
            elif order == "y":

                return order_item(selected_item, total)
            
            else:
                print( "Your answer has to be y or n")
                working_continiue()

        else:
            print("Not in stock")
            return f"Search a {selected_item}"
    
    except ValueError:
        print('Input is not valid. Try again.')
        search_and_order_item()

def check_user_validation(func):

    def wrapper(*args, **kwargs):
        global user

        user_validation = user.is_authenticated

        if user_validation:
            return func(*args, **kwargs)
        
        while not user_validation:
            if isinstance(user, User):
                answer = input('Sorry, but you are not employee. Would you like to change the name?y/n ').lower()
                if answer == 'y':
                    user = get_name()
                elif answer == 'n':
                    working_continiue()
                    break
                else:
                    print("Yoir answer has to be y or n")
                    working_continiue()
        
            if isinstance(user, Employee):
                password = input("Please input your password:")
                user_validation = user.authenticate(password)
                if user.is_authenticated:
                    return func(*args, **kwargs)
                else: 
                    answer = input ("User_name or password is not valid. Do you want to try again?y/n").lower()
                    if answer =="y":
                        user = get_name()
                    elif answer == "n":
                        working_continiue()
                        break
                    else:
                        print("Yoir answer has to be y or n")
                        working_continiue()
            else: 
                answer = input ("User_name or password is not valid. Do you want to try again?y/n").lower()
                if answer =="y":
                    user = get_name()
                elif answer == "n":
                    working_continiue()
                    break
                else:
                    print("Yoir answer has to be y or n")
                    working_continiue()                         
    return wrapper

@check_user_validation
def order_item(selected_item, total):
    while True:
            try: 
                amount = int(input("How many would you like? "))
                if amount >= total:
                    user.order(selected_item, amount)
                elif amount < total:
                    print( f"{amount} {selected_item} have been placed")
                    break
            except ValueError:
                print('Input valid')
    return f"Search and ordered the {selected_item}"  
            
def browse_by_category():

    categories = []

    for warehouse in stock:
        for item in warehouse.stock:
            categories.append(item.category)

    count = Counter(categories)

    summary_of_categories = []

    i = 1
    for k, v in count.items():
        summary_of_categories.append((i, k, v))
        i+=1

    for i in summary_of_categories:
        print(f"{i[0]}. {i[1]} ({i[2]})")
              
    try :
        number_of_category = int(input("Type the number of the category to browse: "))

        selected_category = None

        for category_info in summary_of_categories:
            if number_of_category == category_info[0]:
                selected_category = category_info[1]
                break  

        print(f"\nList of {selected_category} available:")

        for warehouse in stock:
            for item in warehouse.search(selected_category):
                print(f"{item}, Warehouse {warehouse.warehouse_id}")

        return f"Browsed the category {selected_category}"     
    except ValueError:
        print (f'Invalid input. Try again.')
    except TypeError:
        print("It has to be a number of category")
    finally:
        working_continiue()
                

def session_operation():
   
    menu = {"1": "List items by warehouse", "2": "Search an item and place an order","3": "Browse by category", "4": "Quit" }
    display_menu(menu) 

    operation = get_selected_operation()

    if operation == "4":
        user.bye()
        return
    elif operation == "1":
            action = list_items_by_warehouse()
            session_actions.append(action)
            working_continiue()        
    elif operation == "2":
            action = search_and_order_item()
            session_actions.append(action)
            working_continiue()         
    elif operation == "3":
        action = browse_by_category()
        session_actions.append(action)
        working_continiue()
    else:
        print("*" * 50)
        print(operation, "is not a valid operation.")
        print("*" * 50)
        working_continiue()

def working_continiue():
    try: 
        working_continue = input("Would you like to continue to work with program?(y/n) ").lower()
        if working_continue == "y":
            session_operation()
        elif working_continue != "n":
            pass
        else:
            print("Invalid input. Try again")
    except ValueError:
        print("Invalid input. Try again")
    except TypeError:
        print("Invalid input. Try again")

def get_name():
    user = None
    user_name = input("Please provide your name: ")
    for i in personnel:
        if user_name == i['user_name']:
            user = Employee(i['user_name'], i['password'])
            return user
        for j in i.get('head_of', []):
            if user_name == j['user_name']:
                user = Employee (j['user_name'], j['password'])
                return user
    user = User(user_name)
    return user

session_actions = []
user = get_name()
print(user.greet())
session_operation()
print(user.bye())
if session_actions:
            print("In this session you have:")
            for i, action in enumerate(session_actions, start=1):
                print(f"""    {i}. {action}""")



    

    




