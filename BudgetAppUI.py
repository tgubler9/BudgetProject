from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QLabel, QLineEdit
import budgetYear

class BudgetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget App")
        self.setGeometry(100, 100, 800, 600)  # Set window size

        self.label = QLabel("Enter Expense:", self)
        self.label.move(20, 20)


        """Here is our textbox for our expense input"""
        self.expense_input = QLineEdit(self)
        self.expense_input.move(120, 20)
        self.expense_input.resize(100, 30)

        """This button refreshes the background BudgetYear object incase the values need to be re-retrieved"""
        self.refresh_button = QPushButton("Refresh", self)
        self.refresh_button.move(500, 60)
        self.refresh_button.clicked.connect(self.refresh_budget_obj)

        """This button sends the value in the text box to the google sheets"""
        self.expense_button = QPushButton("Add Expense", self)
        self.expense_button.move(20, 60)
        self.expense_button.clicked.connect(self.add_expense)

        """This button changes the background of the computer based on the info in the google sheets"""
        self.background_change_button = QPushButton("Change background", self)
        self.background_change_button.move(50,550)
        self.background_change_button.resize(135,30)
        self.background_change_button.clicked.connect(self.change_background)

        # Add a text area for showing data
        self.text_area = QTextEdit(self)
        self.text_area.move(20, 100)
        self.text_area.resize(400, 200)

        """This is the budgetYear object which implements most of the background work"""
        self.budget_year_obj = budgetYear.BudgetYear()

    def add_expense(self):
        expense = self.expense_input.text()
        self.budget_year_obj.send_value(expense)
        self.text_area.append(expense)
    # Add your widgets here

    def change_background(self):
        self.budget_year_obj.screenshot()

    def refresh_budget_obj(self):
        self.budget_year_obj = budgetYear.BudgetYear()

if __name__ == "__main__":
    app = QApplication([])
    window = BudgetApp()
    window.show()
    app.exec_()