from kivy.uix.screenmanager import Screen
from logic.customer.viewCustomer import ViewCustomersWindow

class DashboardWindow(Screen):
     def load_customers(self):
        # Clear the current content
        self.ids.content_area.clear_widgets()

        # Create an instance of the ViewCustomersWindow
        customer_view = ViewCustomersWindow()

        # Add the ViewCustomersWindow to the content_area
        self.ids.content_area.add_widget(customer_view)

        # Call on_enter to load customer data
        customer_view.on_enter()
