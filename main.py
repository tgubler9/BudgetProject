import os
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import budgetYear
import pyautogui
import numpy as np
import matplotlib.pyplot as plt

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1L4yjLKLaMQQokcvFhDzepPWEyGQhhnxnpq7VgPZB0bc"


def main():
    budget_obj = budgetYear.BudgetYear()
    budget_obj.get_values("A5")



    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    # This will find the column or month that is currently in use by finding the second to last row with values in it.
    service = build("sheets", "v4", credentials=credentials)
    sheets = service.spreadsheets()
    resultsForFirstRow = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="1:1").execute()
    print(resultsForFirstRow)
    valuesForFirstRow = resultsForFirstRow.get('values', [])
    columnInUse = chr(ord("A") + len(valuesForFirstRow[0]) - 2)

    # This will use the columnInUse variable to find the first row in that column that is empty.
    resultsForColumnInUse = sheets.values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=f"{columnInUse}:{columnInUse}").execute()
    values_for_column_in_use = resultsForColumnInUse.get('values', [])
    rowInColumnInUse = len(values_for_column_in_use) + 1

    # Here we will print the current month, its expenses and its sum.
    print("The month is {0} and its expenses are: \n{1}".format(
        values_for_column_in_use[0][0], f"\n".join(str(values_for_column_in_use[i][0]) for i in range(1,
        len(values_for_column_in_use)))
    ))

     # This will combine the two variables we found into a string for the cell we need.
    cellInUse = f"{columnInUse}{rowInColumnInUse}"
    print(cellInUse)

    """while (choice := input("Type \"get\" or \"enter\" or \"exit\" to get info, enter info, or exit.")) != "exit":
        
        if choice == "get":
            inputrange = input("Enter in cell that you want to see or cell range.")

            try:
                result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=inputrange).execute()
                print("Printing result", result)
                values = result.get("values", [])

                for row in values:
                    print(row)

            except HttpError as error:
                print(error)

        if choice == "enter":
            try:

                sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="sheet1!" + f"{cellInUse}",
                                       valueInputOption="USER_ENTERED",
                                       body={"values": [[input("enter expense")]]}).execute()

            except HttpError as error:
                print(error)"""

    objectj = budgetYear.BudgetYear()

    """month = objectj.values_for_column_in_use.pop(0)
    list_of_expenses = [float(item[0]) for item in objectj.values_for_column_in_use]

    cumulative_sums = np.cumsum(list_of_expenses)

    fig,ax = plt.subplots()
    ax.plot(range(len(cumulative_sums)), cumulative_sums, marker='o', linestyle='-', color="gray")

    # Plot the cumulative sums

    fig.set_facecolor("gray")
    ax.set_facecolor("black")
    ax.set_xlabel("Purchase Number", color="white")
    ax.set_ylabel("Total Amount Spent", color="white")
    ax.set_title("Running Total of Purchases")
    ax.tick_params(color="gray")

    for spine in ax.spines.values():
        spine.set_edgecolor("gray")

    final_spent = cumulative_sums[-1]  # Gets the last value of cumulative_sums
    text_position_x = len(cumulative_sums) * 0.15  # Adjust this as needed to place the text at desired x-coordinate
    text_position_y = max(cumulative_sums) * 1.15  # Adjust this as needed to place the text at desired y-coordinate
    ax.text(text_position_x, text_position_y, f"You have spent ${final_spent} so far this month", color="white")

    plt.grid(True)
    plt.savefig("expenses_plot.png")
    plt.show()"""
    objectj.screenshot()




if __name__ == "__main__":
    main()

# We want this to be in a while loop
# I want to display the current month and its expenses but only during the first iteration of the while loop, and then
# after I want it to ask you.
