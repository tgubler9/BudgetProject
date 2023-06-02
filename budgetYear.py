import calendar


class BudgetYear:
    # We want each BudgetYear object to have parameters like yearly sum of spending. And each BudgetYear object will
    # have 12 BudgetMonth objects in a list. One for each month of the year and those objects will have parameters of sums,
    # and then we can override the BudgetYear methods with sum from the beginning of the year to the end of that month,
    # and the average will also be the beginning of the year to the end of that month.
    SPREADSHEET_ID = "1L4yjLKLaMQQokcvFhDzepPWEyGQhhnxnpq7VgPZB0bc"
    def __init__(self, year):
        self.sum = 0
        self.year = year
        self.months = [BudgetMonth(month_name) for month_name in calendar.month_name[1:13]]

    def get_sum(self):
        for month in self.months:
            self.sum = month.get_sum()
        return self.sum



class BudgetMonth:
    SPREADSHEET_ID = "1L4yjLKLaMQQokcvFhDzepPWEyGQhhnxnpq7VgPZB0bc"
    def __init__(self, month):
        self.month = month
        self.sum = sum(self.expense)
        self.expense = []

    def get_sum(self):
        return self.sum

    def get_month(self):
        return self.month

    def print_expenses(self):
        nextline = 0
        for i in self.expense:
            print(i + " ")
            nextline += 1
            if nextline % 3 == 0:
                print("\n")

    def add_expense(self, expense):
        self.expense.append(expense)
        self.sum = sum(self.expense)

        # We want a data field to be a sum value, we want there to be expenses assigned to the month. Later we want each
        # month to its own column in a Google sheets which I believe can be referred with the Google api and some array
        # or list.
