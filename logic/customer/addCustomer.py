from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import csv
import re

# Load the KV file for Add Customer screen
Builder.load_file('view/customer/addCustomer.kv')

class AddCustomerWindow(Screen):
    def add_customer(self):
        """Add a new customer to the CSV file after validating the input data."""
        # Retrieve the data from the input fields
        customer_id = self.ids.customer_id.text
        customer_name = self.ids.customer_name.text
        customer_email = self.ids.customer_email.text
        customer_phone = self.ids.customer_phone.text
        customer_address = self.ids.customer_address.text
        customer_company = self.ids.customer_company.text

        # Validate input fields
        if not self.validate_inputs(customer_id, customer_name, customer_email, customer_phone, customer_address, customer_company):
            return  # Stop if validation fails

        # Create a new record
        new_record = [customer_id, customer_name, customer_email, customer_phone, customer_address, customer_company]

        # Write the record to the CSV file
        with open('logic/data/data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_record)

        self.ids.message_label.text = "Customer added successfully!"
        self.ids.message_label.color = (0, 1, 0, 1)  # Green for success message

        # Clear input fields after adding
        self.clear_inputs()
        
        # Navigate back to the dashboard
        self.manager.current = 'dashboard'

    def validate_inputs(self, customer_id, customer_name, customer_email, customer_phone, customer_address, customer_company):
        """Validate input data before saving."""
        # Clear previous messages
        self.ids.message_label.text = ""

        # Check if any field is empty
        if not (customer_id and customer_name and customer_email and customer_phone and customer_address and customer_company):
            self.ids.message_label.text = "Error: All fields must be filled."
            return False

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", customer_email):
            self.ids.message_label.text = "Error: Invalid email format."
            return False

        # Validate phone number (only digits and length of 10)
        if not (customer_phone.isdigit() and len(customer_phone) == 10):
            self.ids.message_label.text = "Error: Phone number must be 10 digits."
            return False

        # Check if customer_id is unique (optional)
        if not self.is_unique_id(customer_id):
            self.ids.message_label.text = f"Error: Customer ID '{customer_id}' already exists."
            return False

        return True

    def is_unique_id(self, customer_id):
        """Check if customer_id is unique by reading the CSV file."""
        try:
            with open('logic/data/data.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == customer_id:  # Compare customer_id (first column)
                        return False
            return True
        except FileNotFoundError:
            # If the file doesn't exist, assume all IDs are unique (first customer)
            return True

    def clear_inputs(self):
        """Clear the input fields after adding a customer."""
        self.ids.customer_id.text = ''
        self.ids.customer_name.text = ''
        self.ids.customer_email.text = ''
        self.ids.customer_phone.text = ''
        self.ids.customer_address.text = ''
        self.ids.customer_company.text = ''
        self.ids.message_label.text = ""  