import webbrowser

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

from models.employee import Employee
from models.department import Department # noqa
from models.position import Position # noqa

from app_config.db_config import initialize_database
from operations.employee_operations import (
    add_employee, promote_employee, list_all_employees,
    delete_employee, get_team_leaders, get_experienced_women
)


# Helper function for showing popups
def show_popup(title, message):
    popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
    popup.open()


class PromoteEmployeeForm(BoxLayout):
    employee_name = ObjectProperty(None)
    new_position = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.add_widget(Label(text="Employee Name"))
        self.employee_name = TextInput(multiline=False)
        self.add_widget(self.employee_name)

        self.add_widget(Label(text="New Position"))
        self.new_position = TextInput(multiline=False)
        self.add_widget(self.new_position)

        self.add_widget(Button(text="Promote", on_press=self.submit_form))

    def submit_form(self, instance):
        try:
            employee_name = self.employee_name.text
            new_position = self.new_position.text
            promote_employee(employee_name, new_position)
            show_popup("Success", f"Employee {employee_name} promoted to {new_position}!")
        except Exception as e:
            show_popup("Error", f"An error occurred: {e}")


class EmployeeForm(BoxLayout):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    position_name = ObjectProperty(None)
    department_name = ObjectProperty(None)
    hire_date = ObjectProperty(None)
    manager_name = ObjectProperty(None)
    gender = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # self.employee_id = TextInput(multiline=False)
        self.first_name = TextInput(multiline=False)
        self.last_name = TextInput(multiline=False)
        self.position_name = TextInput(multiline=False)
        self.department_name = TextInput(multiline=False)
        self.hire_date = TextInput(multiline=False)
        self.manager_name = TextInput(multiline=False)
        self.gender = TextInput(multiline=False)

        # self.add_widget(Label(text="EmployeeID"))
        # self.add_widget(self.employee_id)

        self.add_widget(Label(text="First Name"))
        self.add_widget(self.first_name)
        self.add_widget(Label(text="Last Name"))
        self.add_widget(self.last_name)
        self.add_widget(Label(text="Position"))
        self.add_widget(self.position_name)
        self.add_widget(Label(text="Department"))
        self.add_widget(self.department_name)
        self.add_widget(Label(text="Hire date"))
        self.add_widget(self.hire_date)
        self.add_widget(Label(text="Manager name"))
        self.add_widget(self.manager_name)
        self.add_widget(Label(text="gender"))
        self.add_widget(self.gender)

        self.add_widget(Button(text="Submit", on_press=self.submit_form))

    def submit_form(self, instance):
        try:
            # Create an Employee object with the data from the input fields
            employee = Employee(
                first_name=self.first_name.text,
                last_name=self.last_name.text,
                position_name=self.position_name.text,
                department_name=self.department_name.text,
                hire_date=self.hire_date.text,
                manager_name=self.manager_name.text,
                gender=self.gender.text
            )

            # Save the employee to the database using the save method
            employee.save()

            # Show success popup
            show_popup("Success", "Employee added successfully!")

        except ValueError:
            # Show error popup if the input values are not valid
            show_popup("Error", "Please enter valid values for the fields.")

        except Exception as e:
            # Show error popup for any other exception
            show_popup("Error", f"An error occurred: {e}")


class DeleteEmployeeForm(BoxLayout):
    employee_name = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.add_widget(Label(text="Employee Name"))
        self.employee_name = TextInput(multiline=False)
        self.add_widget(self.employee_name)

        self.add_widget(Button(text="Delete", on_press=self.submit_form))

    def submit_form(self, instance):
        try:
            employee_name = self.employee_name.text
            delete_employee(employee_name)
            show_popup("Success", "Employee deleted successfully!")
        except Exception as e:
            show_popup("Error", f"An error occurred: {e}")


class Sidebar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (0.2, 1)
        self.add_widget(
            Button(text="Add Employee", on_press=self.show_employee_form, font_size=30, background_color=(3, 3, 3, 3),
                   color=(0, 0, 0, 1)))
        self.add_widget(Button(text="List of Employees", on_press=self.show_employee_list, font_size=30,
                               background_color=(3, 3, 3, 3),
                               color=(0, 0, 0, 1)))
        self.add_widget(
            Button(text="Team Leaders", on_press=self.show_team_leaders, font_size=30, background_color=(0, 1, 0, 1),
                   color=(0, 0, 0, 1)))
        self.add_widget(Button(text="Find Experienced Women", on_press=self.find_experienced_women, font_size=30,
                               background_color=(0, 1, 0, 1),
                               color=(0, 0, 0, 1)))
        self.add_widget(Button(text="Promote Employee", on_press=self.show_promote_employee_form, font_size=30,
                               background_color=(0, 1, 0, 1),
                               color=(0, 0, 0, 1)))
        self.add_widget(Button(text="Delete Employee", on_press=self.show_delete_employee_form, font_size=30,
                               background_color=(3, 0, 0, 8),
                               color=(0, 0, 0, 1)))
        self.add_widget(Button(text="About", on_press=self.show_about, font_size=30, background_color=(3, 0, 0, 8),
                               color=(0, 0, 0, 1)))

    def show_employee_form(self, instance):
        employee_form = EmployeeForm()
        popup = Popup(title="Add Employee", content=employee_form, size_hint=(0.9, 0.9))
        popup.open()

    def show_employee_list(self, instance):
        employees = list_all_employees()  # Fetch the latest list of employees
        content = BoxLayout(orientation='vertical')
        for emp in employees:
            content.add_widget(Label(text=f"{emp[0]} {emp[1]} - {emp[2]}"))
        popup = Popup(title="List of Employees", content=content, size_hint=(0.9, 0.9))
        popup.open()

    def show_team_leaders(self, instance):
        leaders = get_team_leaders()
        content = BoxLayout(orientation='vertical')
        for leader in leaders:
            content.add_widget(Label(text=f"{leader[0]} {leader[1]} - {leader[2]}"))
        popup = Popup(title="Team Leaders", content=content, size_hint=(0.9, 0.9))
        popup.open()

    def update_team_leaders(self):
        leaders = get_team_leaders()

        if leaders:
            leaders_text = "\n".join([f"{first} {last} - {position}" for first, last, position in leaders])
            self.team_leader_list.text = leaders_text
        else:
            self.team_leader_list.text = "No team leaders found."

    def find_experienced_women(self, instance):
        # Get the list of experienced women (between 10-15 years of experience)
        women = get_experienced_women()

        content = BoxLayout(orientation='vertical')
        if not women:
            content.add_widget(Label(text="No experienced women found."))
        else:
            for woman in women:
                content.add_widget(Label(text=f"{woman[0]} {woman[1]} - {woman[2]} years"))

        # Display the results in a popup
        popup = Popup(title="Experienced Women", content=content, size_hint=(0.9, 0.9))
        popup.open()

    def show_promote_employee_form(self, instance):
        promote_form = PromoteEmployeeForm()
        popup = Popup(title="Promote Employee", content=promote_form, size_hint=(0.9, 0.9))
        popup.open()

    def show_delete_employee_form(self, instance):
        delete_form = DeleteEmployeeForm()
        popup = Popup(title="Delete Employee", content=delete_form, size_hint=(0.9, 0.9))
        popup.open()

    def open_url(self, url):
        """Open the URL in the web browser."""
        webbrowser.open(url)

    def show_about(self, instance):
        about_layout = BoxLayout(orientation='vertical')

        # GitHub link button
        github_button = Button(text="Visit GitHub Repository",
                               on_press=lambda x: self.open_url("https://github.com/Lyuben13"))
        about_layout.add_widget(github_button)

        # Pastebin link button
        pastebin_button = Button(text="Visit Pastebin Link",
                                 on_press=lambda x: self.open_url("https://pastebin.com/u/Lyuben_Andreev"))
        about_layout.add_widget(pastebin_button)

        # Popup to show the links
        popup = Popup(
            title="About",
            content=about_layout,
            size_hint=(0.6, 0.4)
        )
        popup.open()


class CompanyManagementApp(App):
    def build(self):
        initialize_database()  # Initialize the database
        layout = BoxLayout(orientation='horizontal')
        layout.add_widget(Sidebar())
        return layout


if __name__ == "__main__":
    CompanyManagementApp().run()
