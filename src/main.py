from PyQt5.QtWidgets import QApplication
import BudgetAppUI


def main():
    app = QApplication([])
    app.setStyleSheet(BudgetAppUI.stylesheet)  # Apply the stylesheet to the application
    window = BudgetAppUI.BudgetApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
