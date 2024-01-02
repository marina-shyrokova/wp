import psycopg2
import json

try:
    conn = psycopg2.connect(
        dbname="warehouse_project",
        user="postgres",
        password="11111",
        host="localhost",
        port="5432",
    )
except psycopg2.Error as e:
    print(e)

if conn:
    cursor = conn.cursor()

    query = "SELECT * FROM employee"

    cursor.execute(query)

    empoyees_data = cursor.fetchall()

    if not empoyees_data:
        data_to_load = []

        file_path = (
            "/home/marina/Student/Project/warehouse-project/cli/data/personnel.json"
        )
        with open(file_path) as json_file:
            data = json.load(json_file)

            def extract_data(data):
                for item in data:
                    user_name = item["user_name"]
                    password = item["password"]

                    data_to_load.append((user_name, password))
                    if "head_of" in item:
                        extract_data(item["head_of"])

            extract_data(data)

        cursor.executemany(
            "INSERT INTO employee (user_name, password) VALUES (%s, %s);", data_to_load
        )

        conn.commit()

    query = "SELECT * FROM item"

    cursor.execute(query)

    items_data = cursor.fetchall()

    if not items_data:
        file_path = "/home/marina/Student/Project/warehouse-project/cli/data/stock.json"
        with open(file_path) as json_file:
            data = json.load(json_file)

            query = "SELECT * FROM warehouse"

            cursor.execute(query)
            warehouses_data = cursor.fetchall()

            if not warehouses_data:
                warehouse_id = set()
                for item in data:
                    warehouse_id.add(item["warehouse"])

                warehouses_to_load = []

                for id in warehouse_id:
                    warehouses_to_load.append((id, f"Warehouse {id}"))

                cursor.executemany(
                    "INSERT INTO warehouse (id, name) VALUES (%s, %s);",
                    warehouses_to_load,
                )

                conn.commit()

            items_to_load = []

            for item in data:
                items_to_load.append(
                    (
                        item["state"],
                        item["category"],
                        item["warehouse"],
                        item["date_of_stock"],
                    )
                )
            cursor.executemany(
                "INSERT INTO item (state, category, warehouse, date_of_stock) VALUES (%s, %s, %s, %s);",
                items_to_load,
            )
            conn.commit()

    cursor.close()
    conn.close()
