from kivy.uix.screenmanager import Screen
import csv
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

Builder.load_file('view/customer/viewCustomer.kv')

class ViewCustomersWindow(Screen):
    def on_enter(self):
        """Load and display customers when entering the screen."""
        self.customers_data = []  # Initialize the customers data
        self.load_customers()

    def load_customers(self):
        """Load customers from the CSV file and display them."""
        self.ids.customers_grid.clear_widgets()  # Clear existing widgets

        # Add headers
        headers = ["ID", "Name", "Email", "Phone", "Address", "Company", "Actions"]
        for header in headers:
            self.ids.customers_grid.add_widget(Label(text=header, bold=True, color=(0, 0, 0, 1)))

        try:
            with open('logic/data/data.csv', mode='r') as file:
                reader = csv.reader(file)
                self.customers_data = list(reader)  # Store all customer data
                for row in self.customers_data:
                    if row:
                        for item in row:
                            self.ids.customers_grid.add_widget(Label(text=item.strip(), color=(0, 0, 0, 1)))

                        # Create a BoxLayout for buttons
                        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
                        button_layout.add_widget(Label(text=''))  # Empty space for centering

                        # Edit Button
                        edit_button = Button(text='Edit', size_hint_x=None, width=80)
                        edit_button.bind(on_release=lambda instance, row=row: self.edit_customer(row))
                        button_layout.add_widget(edit_button)

                        # Delete Button
                        delete_button = Button(text='Delete', size_hint_x=None, width=80)
                        delete_button.bind(on_release=lambda instance, row=row: self.delete_customer(row))
                        button_layout.add_widget(delete_button)

                        button_layout.add_widget(Label(text=''))  # Empty space for centering

                        # Add the button layout to the grid
                        self.ids.customers_grid.add_widget(button_layout)

        except FileNotFoundError:
            self.ids.customers_grid.add_widget(Label(text="CSV file not found.", color=(1, 0, 0, 1)))

    def search_customers(self, search_text):
        """Search for customers based on input and display the results."""
        self.ids.customers_grid.clear_widgets()  # Clear existing widgets

        headers = ["ID", "Name", "Email", "Phone", "Address", "Company", "Actions"]
        for header in headers:
            self.ids.customers_grid.add_widget(Label(text=header, bold=True, color=(0, 0, 0, 1)))

        # Filter customers based on search input
        for customer in self.customers_data:
            if (search_text.lower() in customer[1].lower() or 
                search_text.lower() in customer[2].lower() or 
                search_text.lower() in customer[3].lower() or 
                search_text.lower() in customer[5].lower()):
                
                # Add customer data labels
                for item in customer:
                    self.ids.customers_grid.add_widget(Label(text=item.strip(), color=(0, 0, 0, 1)))

                # Create a BoxLayout for buttons
                button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
                button_layout.add_widget(Label(text=''))  # Empty space for centering

                # Edit Button
                edit_button = Button(text='Edit', size_hint_x=None, width=80, background_color=(.06, .45, .45, 1))
                edit_button.bind(on_release=lambda instance, row=customer: self.edit_customer(row))
                button_layout.add_widget(edit_button)

                # Delete Button
                delete_button = Button(text='Delete', size_hint_x=None, width=80, background_color=(.06, .45, .45, 1))
                delete_button.bind(on_release=lambda instance, row=customer: self.delete_customer(row))
                button_layout.add_widget(delete_button)

                button_layout.add_widget(Label(text=''))  # Empty space for centering

                # Add the button layout to the grid
                self.ids.customers_grid.add_widget(button_layout)

    def delete_customer(self, row):
        """Delete the selected customer row based on ID."""
        customer_id = row[0]  # Assuming the ID is the first item in the row
        print("Deleting customer with ID:", customer_id)

        # Load existing customers from the CSV
        updated_data = []
        try:
            with open('logic/data/data.csv', mode='r') as file:
                reader = csv.reader(file)
                for customer in reader:
                    if customer and customer[0] != customer_id:  # Keep rows that don't match the ID
                        updated_data.append(customer)

        except FileNotFoundError:
            print("CSV file not found. Cannot delete customer.")

        # Write the updated data back to the CSV
        with open('logic/data/data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(updated_data)

        self.load_customers()  # Reload to display updated data


    def edit_customer(self, row):
        """Open a dialog to edit the selected customer row."""
        popup_layout = BoxLayout(orientation='vertical', padding=10)

        # Create text inputs for each field
        name_input = TextInput(text=row[1], hint_text='Name')
        email_input = TextInput(text=row[2], hint_text='Email')
        phone_input = TextInput(text=row[3], hint_text='Phone')
        address_input = TextInput(text=row[4], hint_text='Address')
        company_input = TextInput(text=row[5], hint_text='Company')

        # Add inputs to the layout
        popup_layout.add_widget(name_input)
        popup_layout.add_widget(email_input)
        popup_layout.add_widget(phone_input)
        popup_layout.add_widget(address_input)
        popup_layout.add_widget(company_input)

        # Save button
        save_button = Button(text='Save')
        popup_layout.add_widget(save_button)

        # Create popup
        popup = Popup(title='Edit Customer', content=popup_layout, size_hint=(0.7, 0.7))

        # Save button functionality
        def save_changes(instance):
            # Update the row with new values
            updated_row = [row[0], name_input.text, email_input.text, phone_input.text, address_input.text, company_input.text]

            # Update the customers_data
            index = self.customers_data.index(row)
            self.customers_data[index] = updated_row

            # Save the updated data back to the CSV
            self.save_customers()

            # Close the popup
            popup.dismiss()

        save_button.bind(on_release=save_changes)

        # Open the popup
        popup.open()

    def save_customers(self):
        """Save the updated customers data back to the CSV file."""
        with open('logic/data/data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(self.customers_data)  # Write all updated rows

        self.load_customers()  # Reload to display updated data