from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit,QHBoxLayout, QPushButton, QLabel, QLineEdit
import budgetYear

stylesheet = """
    QMainWindow {
        background-color: #333;
    }

    QLabel, QPushButton, QLineEdit, QTextEdit {
        font-family: 'Arial';
        font-size: 14px;
        color: white;
    }

    QLineEdit {
        border: 2px solid #555;
        border-radius: 10px;
        padding: 5px;
        background-color: #222;
        color = black;
    }

    QPushButton {
        border: 2px solid #555;
        border-radius: 10px;
        padding: 5px;
        background-color: #555;
    }

    QPushButton:hover {
        background-color: #777;
    }

    QTextEdit {
        background-color: white;
        border: none;
        padding: 5px;
        border-radius: 10px;
        color: red; 
    }
"""

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Add your custom title and buttons here
        self.title = QLabel("Budget App")
        self.title.setStyleSheet("color: white;")

        self.minimizeButton = QPushButton("Minimize")
        self.minimizeButton.resize(50, 50)

        self.closeButton = QPushButton("Close")
        self.closeButton.resize(50, 50)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.minimizeButton)
        self.layout.addWidget(self.closeButton)

        self.minimizeButton.clicked.connect(parent.showMinimized)
        self.closeButton.clicked.connect(parent.close)

        self.setStyleSheet("""
            background-color: #2c3e50;
            padding: 5px;
        """)

    def mousePressEvent(self, event):
        self.startPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.startPos
        self.parent().move(self.parent().pos() + delta)
        self.startPos = event.globalPos()

class BudgetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget App")
        self.setGeometry(100, 100, 1000, 800)  # Set window size

        self.label = QLabel("Enter Expense:", self)
        self.label.move(20, 50)

        # Hide the title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Create and set the custom title bar
        self.customTitleBar = CustomTitleBar(self)
        self.setMenuWidget(self.customTitleBar)

        """Here is our textbox for our expense input"""
        self.expense_input = QLineEdit(self)
        self.expense_input.move(150, 50)
        self.expense_input.resize(100, 30)

        """This button refreshes the background BudgetYear object incase the values need to be re-retrieved"""
        self.refresh_button = QPushButton("Refresh", self)
        self.refresh_button.move(150, 85)
        self.refresh_button.clicked.connect(self.refresh_budget_obj)

        """This button sends the value in the text box to the google sheets"""
        self.expense_button = QPushButton("Add Expense", self)
        self.expense_button.move(20, 85)
        self.expense_button.clicked.connect(self.add_expense)

        """This button changes the background of the computer based on the info in the google sheets"""
        self.background_change_button = QPushButton("Change background", self)
        self.background_change_button.move(550, 100)
        self.background_change_button.resize(160,30)
        self.background_change_button.clicked.connect(self.change_background)

        self.add_month_button = QPushButton("Add New Month", self)
        self.add_month_button.move(725, 100)
        self.add_month_button.resize(135,30)
        self.add_month_button.clicked.connect(self.add_month)

        # Add a text area for showing data
        self.text_area = QTextEdit(self)
        self.text_area.move(20, 150)
        self.text_area.resize(250, 500)

        """This is the budgetYear object which implements most of the background work"""
        self.budget_year_obj = budgetYear.BudgetYear()

    def add_expense(self):
        expense = self.expense_input.text()
        self.budget_year_obj.send_value(expense)
        self.text_area.append(expense)
    # Add your widgets here

    def change_background(self):
        self.budget_year_obj.screenshot()

    def add_month(self):
        self.budget_year_obj.add_new_month()

    def refresh_budget_obj(self):
        self.budget_year_obj = budgetYear.BudgetYear()

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(stylesheet)  # Apply the stylesheet to the application
    window = BudgetApp()
    window.show()
    app.exec_()