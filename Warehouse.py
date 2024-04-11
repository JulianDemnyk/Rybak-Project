import re
from datetime import datetime


class Product:
    def __init__(self, name, quantity, price, arrival_date, supplier):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.arrival_date = arrival_date
        self.supplier = supplier

    def validate_data(self):
        if not isinstance(self.name, str) or len(self.name) == 0:
            raise ValueError("Product name must have a name.")
        if not isinstance(self.quantity, int) or self.quantity < 0:
            raise ValueError("Quantity must be at least 1.")
        if not isinstance(self.price, (int, float)) or self.price <= 0:
            raise ValueError("Price can not go below zero.")
        if not isinstance(self.arrival_date, datetime):
            raise ValueError("Arrival date must be a datetime object.")
        if not isinstance(self.supplier, Supplier):
            raise ValueError("Product must have a supplier.")


class Supplier:
    def __init__(self, company_name, contact_info_email, contact_info_phone):
        self.company_name = company_name
        self.contact_info_email = contact_info_email
        self.contact_info_phone = contact_info_phone

    def validate_data(self):
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        phone_pattern = r"\d{3}-\d{3}-\d{4}"
        if not isinstance(self.company_name, str) or len(self.company_name) == 0:
            raise ValueError("Company name must be a non-empty string.")
        if not isinstance(self.contact_info_email, str):
            raise ValueError("Contact info must be a string for email address.")
        if not isinstance(self.contact_info_phone, str):
            raise ValueError("Contact info must be a string for phone number.")
        if not re.match(email_pattern, self.contact_info_email) or not re.match(phone_pattern,
                                                                                self.contact_info_phone):
            raise ValueError("Contact info must be a valid email address or phone number.")


class Transaction:
    def __init__(self, date, operation_type, quantity, product_name, supplier_name):
        self.date = date
        self.operation_type = operation_type
        self.quantity = quantity
        self.product_name = product_name
        self.supplier_name = supplier_name

    def notify_new_product(self):
        print(
            f"!!!Received new product: {self.product_name} from supplier {self.supplier_name}.!!!\nQuantity: {self.quantity}\nDate of arrival: {self.date.strftime('%Y-%m-%d')}")

    def notify_update_product(self):
        print(f"!!!Product: {self.product_name} was updated!!!")

    def notify_sell_products(self):
        print(f"!!!Product: {self.product_name}, was sold.\nQuantity: {self.quantity}!!!")


class Warehouse:
    def __init__(self):
        self.products = []
        self.suppliers = []

    def add_product(self, product, supplier):
        if not isinstance(product, Product):
            raise ValueError("Only Product objects can be added to the warehouse.")
        if not isinstance(supplier, Supplier):
            raise ValueError("Only Supplier objects can be added to the warehouse.")
        product.supplier = supplier
        product.validate_data()
        self.products.append(product)

    def add_supplier(self, supplier):
        if not isinstance(supplier, Supplier):
            raise ValueError("Only Supplier objects can be added to the warehouse.")
        supplier.validate_data()
        self.suppliers.append(supplier)

    def remove_product(self, product):
        if product in self.products:
            self.products.remove(product)

    def update_product_info(self, product, **kwargs):
        if product in self.products:
            for key, value in kwargs.items():
                setattr(product, key, value)

    def sell_product(self, product_name, quantity_to_sell):
        for product in self.products:
            if product.name == product_name:
                if product.quantity >= quantity_to_sell:
                    product.quantity -= quantity_to_sell
                    print(f"Successfully sold {quantity_to_sell} units of {product_name}.")
                    return True
                else:
                    print(f"Not enough stock for {product_name}. Only {product.quantity} units available.")
                    return False
        print(f"Product {product_name} not found.")
        return False

    def list_products(self, sort_by=None):
        if sort_by:
            self.products.sort(key=lambda x: getattr(x, sort_by))
        for product in self.products:
            print(
                f"Name: {product.name}, Quantity: {product.quantity}, Price: {product.price}, Arrival Date: {product.arrival_date}, Supplier: {product.supplier.company_name}")

    def list_suppliers(self):
        for supplier in self.suppliers:
            print(f"Company Name: {supplier.company_name}, Contact Info:")
            print(f"  Email address: {supplier.contact_info_email}")
            print(f"  Phone number: {supplier.contact_info_phone}")
            print(f"  Products supplied:")
            supplied_products = [product for product in self.products if product.supplier == supplier]
            if supplied_products:
                for product in supplied_products:
                    print(
                        f"    Name: {product.name}, Quantity: {product.quantity}, Price: {product.price}, Arrival Date: {product.arrival_date}")
            else:
                print("    No products supplied by this supplier.\n")


if __name__ == "__main__":
    warehouse = Warehouse()

    while True:
        print("\nChoose an option:")
        print("1. Add a product")
        print("2. Remove a product")
        print("3. List products in the warehouse")
        print("4. Add a supplier")
        print("5. List suppliers")
        print("6. Update product information")
        print("7. Sell product")
        print("8. Exit")
        option = input("Enter your choice: ")

        if option == "1":
            name = input("Enter product name: ")
            quantity = int(input("Enter product quantity: "))
            price = float(input("Enter product price: "))
            arrival_date = input("Enter arrival date (YYYY-MM-DD): ")
            supplier_name = input("Enter product supplier: ")
            arrival_date = datetime.strptime(arrival_date, "%Y-%m-%d")

            supplier = next((s for s in warehouse.suppliers if s.company_name == supplier_name), None)
            if supplier is None:
                print(f"Supplier '{supplier_name}' not found.")
            else:
                product = Product(name, quantity, price, arrival_date, supplier)
                warehouse.add_product(product, supplier)
                print("Product added successfully.")
                transaction = Transaction(datetime.now(), "receive", quantity, name, supplier_name)
                transaction.notify_new_product()
        elif option == "2":
            name = input("Enter product name to remove: ")
            for product in warehouse.products:
                if product.name == name:
                    warehouse.remove_product(product)
                    print(f"{name} removed successfully.")
                    break
            else:
                print(f"Product with name {name} not found.")
        elif option == "3":
            print("\nList of products in the warehouse:")
            print("1. Sort by name")
            print("2. Sort by quantity")
            print("3. Sort by price")
            sort_option = input("Choose sorting option: ")

            if sort_option == "1":
                warehouse.list_products(sort_by="name")
            elif sort_option == "2":
                warehouse.list_products(sort_by="quantity")
            elif sort_option == "3":
                warehouse.list_products(sort_by="price")
            else:
                print("Invalid sorting option or warehouse is empty.")
        elif option == "4":
            company_name = input("Enter supplier's company name: ")
            email = input("Enter supplier's email(example@gmail.com): ")
            phone = input("Enter supplier's phone(xxx-xxx-xxxx): ")
            supplier = Supplier(company_name, email, phone)
            warehouse.add_supplier(supplier)
            print("Supplier added successfully.")
        elif option == "5":
            print("\nList of suppliers:")
            warehouse.list_suppliers()
        elif option == "6":
            name = input("Enter product name to update: ")
            for product in warehouse.products:
                if product.name == name:
                    print("Select what you want to update:")
                    print("1. Quantity")
                    print("2. Price")
                    print("3. Arrival Date")
                    update_option = input("Enter your choice: ")
                    if update_option == "1":
                        new_quantity = int(input("Enter new quantity: "))
                        warehouse.update_product_info(product, quantity=new_quantity)
                    elif update_option == "2":
                        new_price = float(input("Enter new price: "))
                        warehouse.update_product_info(product, price=new_price)
                    elif update_option == "3":
                        new_arrival_date = input("Enter new arrival date (YYYY-MM-DD): ")
                        new_arrival_date = datetime.strptime(new_arrival_date, "%Y-%m-%d")
                        warehouse.update_product_info(product, arrival_date=new_arrival_date)
                    else:
                        print("Invalid option.")

                    transaction = Transaction(datetime.now(), "update", 0, name, "")
                    transaction.notify_update_product()
                    break
            else:
                print(f"Product with name {name} not found.")
        elif option == "7":
            product_name = input("Enter product name to sell: ")
            quantity_to_sell = int(input("Enter quantity to sell: "))
            warehouse.sell_product(product_name, quantity_to_sell)
        elif option == "8":
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please choose again.")
