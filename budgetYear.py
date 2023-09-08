import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class BudgetYear:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    SPREADSHEET_ID = "1L4yjLKLaMQQokcvFhDzepPWEyGQhhnxnpq7VgPZB0bc"

    def __init__(self):
        credentials = None
        if os.path.exists("token.json"):
            credentials = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                credentials = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(credentials.to_json())

        self.service = service = build("sheets", "v4", credentials=credentials)
        self.sheet = self.service.spreadsheets()
        self.values_of_first_row = self.sheet.values().get(spreadsheetId= self.SPREADSHEET_ID, range="1:1"
                                                      ).execute().get('values', [])
        self.columnInUse = chr(ord("A") + len(self.values_of_first_row[0]) - 2)
        self.values_for_column_in_use = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID,
                                                range=f"{self.columnInUse}:{self.columnInUse}").execute().get('values',
                                                                                                              [])
        self.rowInColumnInUse = len(self.values_for_column_in_use) + 1
        self.cellInUse = f"{self.columnInUse}{self.rowInColumnInUse}"


    def get_values(self, cell_range):
        return self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, range=cell_range
                                         ).execute().get("values", [])

    def while_Loop(self):
        while (choice := input("Type \"get\" or \"enter\" or \"exit\" to get info, enter info, or exit.")) != "exit":

            if choice == "get":
                inputrange = input("Enter in cell that you want to see or cell range.")

                try:
                    result = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, range=inputrange).execute()
                    print("Printing result", result)
                    values = result.get("values", [])

                    for row in values:
                        print(row)

                except HttpError as error:
                    print(error)

            if choice == "enter":
                try:

                    self.sheet.values().update(spreadsheetId=self.SPREADSHEET_ID, range="sheet1!" + f"{self.cellInUse}",
                                           valueInputOption="USER_ENTERED",
                                           body={"values": [[input("enter expense")]]}).execute()

                except HttpError as error:
                    print(error)


object1 = BudgetYear()
object1.while_Loop()

