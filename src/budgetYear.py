import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import ctypes
from PIL import Image
import pandas as pd
from sklearn.linear_model import LinearRegression

class BudgetYear:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    SPREADSHEET_ID = "1L4yjLKLaMQQokcvFhDzepPWEyGQhhnxnpq7VgPZB0bc"
    MONTH = [
        "January","February","March","April","May","June","July",
             "August","September","October","November","December"
     ]
#If you cant log in, get rid of the token not the credentials.
    def __init__(self):
        credentials = None
        # Path to the service account key file
        service_account_file = 'UniCreds.json'

        # Authenticate using the service account
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=self.SCOPES)

        self.service = service = build("sheets", "v4", credentials=credentials)
        self.sheet = self.service.spreadsheets()
        self.values_of_first_row = self.sheet.values().get(spreadsheetId= self.SPREADSHEET_ID, range="1:1"
                                                      ).execute().get('values', [])[0]
        self.columnInUse = chr(ord("A") + len(self.values_of_first_row) - 1)
        self.values_for_column_in_use = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID,
                                                range=f"{self.columnInUse}:{self.columnInUse}").execute().get('values',[])
        self.rowInColumnInUse = len(self.values_for_column_in_use) + 1
        self.cellInUse = f"{self.columnInUse}{self.rowInColumnInUse}"

    def getcolumn(self, dist_from_month_in_use):
        column = chr(ord("A") + len(self.values_of_first_row) - (1+dist_from_month_in_use))
        print(column)
        return self.get_values(f"{column}:{column}")

    def get_values(self, cell_range):
        """ This is a getter method used to grab data from the google sheets."""
        return self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, range=cell_range).execute().get("values", [])

    # This is a main loop for the program. It will allow you to enter or get info from the google sheets. You can also
    # the program with this as well.

    def send_value(self, amount):
        try:

            self.sheet.values().update(spreadsheetId=self.SPREADSHEET_ID, range="sheet1!" + f"{self.cellInUse}",
                                       valueInputOption="USER_ENTERED",
                                       body={"values": [[amount]]}).execute()
            self.values_for_column_in_use = \
                self.sheet.values().get(
                    spreadsheetId=self.SPREADSHEET_ID,
                    range=f"{self.columnInUse}:{self.columnInUse}").execute().get('values', [])
            self.rowInColumnInUse += 1
            self.cellInUse = f"{self.columnInUse}{self.rowInColumnInUse}"

        except HttpError as error:
            print(error)

    """This differs from the above method in that it can send a value to a specfied cell range rather than just getting
    the value that occupies cell in Use."""
    def send_value_to_range(self, amount, ranges):
        try:

            self.sheet.values().update(spreadsheetId=self.SPREADSHEET_ID, range="sheet1!" + f"{ranges}",
                                       valueInputOption="USER_ENTERED",
                                       body={"values": [[amount]]}).execute()
            """If the column range is farth to the left than the current column in use, we need to 
            set almost all of the class parameters again. If not we just need to update the column in use,
            row in column in use, and cell in use."""
            if ranges[0] > self.columnInUse:
                self.values_of_first_row = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, range="1:1"
                                                                   ).execute().get('values', [])[0]
                self.columnInUse = chr(ord("A") + len(self.values_of_first_row) - 1)
                self.values_for_column_in_use = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID,
                                                                        range=f"{self.columnInUse}:{self.columnInUse}").execute().get(
                    'values', [])
                self.rowInColumnInUse = len(self.values_for_column_in_use) + 1
                self.cellInUse = f"{self.columnInUse}{self.rowInColumnInUse}"
            else:
                self.values_for_column_in_use = \
                    self.sheet.values().get(
                        spreadsheetId=self.SPREADSHEET_ID,
                        range=f"{self.columnInUse}:{self.columnInUse}").execute().get('values', [])
                self.rowInColumnInUse += 1
                self.cellInUse = f"{self.columnInUse}{self.rowInColumnInUse}"

        except HttpError as error:
            print(error)

    """ We need to change the column in use after updated. To start we find the new month
     from the column in use array and our Month Static variable. We then need to use Row 
     in use and """
    def add_new_month(self):
        current_index= self.MONTH.index(self.values_for_column_in_use[0][0])
        if current_index >= (len(self.MONTH) - 1):
            new_month = self.MONTH[0]
        else:
            new_month = self.MONTH[current_index + 1]

        range = f"{chr(ord(self.columnInUse) + 1)}1"
        self.send_value_to_range(new_month, range)
        print(self.columnInUse , " ", self.cellInUse)


    """We have a method here to pull the whole sheet,turn it into a csv,panda
    df, clean it and then return the df"""
    def get_whole_sheet(self):
        values = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, range='Sheet1').execute().get(
            'values',[])

        if not values:
            print("No Data")
        else:
            with open("sheet1.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(values)
        df = pd.read_csv("sheet1.csv")
        for column in df.columns:
            df[column] = df[column].astype(str).str.replace(',', '').astype(float)
        return df

    def while_loop(self):
        """ You can enter or see data in from the google sheets with the range. You can exit the loop by typing exit"""
        while (choice := input("Type \"get\" or \"enter\" or \"exit\" to get info, enter info, or exit.")) != "exit":

            if choice == "get":
                input_range = input("Enter in cell that you want to see or cell range.")

                try:
                    result = self.get_values(input_range)
                    print("Printing result:\n", result)
                    values = result.get("values", [])

                    for row in values:
                        print(row)

                except HttpError as error:
                    print(error)

            if choice == "enter":
                try:

                    self.sheet.values().update(spreadsheetId=self.SPREADSHEET_ID, range="sheet1!" + f"{self.cellInUse}",
                                           valueInputOption="USER_ENTERED",
                                           body={"values": [[input("enter expense:")]]}).execute()
                    self.values_for_column_in_use = \
                        self.sheet.values().get(
                            spreadsheetId=self.SPREADSHEET_ID,
                            range=f"{self.columnInUse}:{self.columnInUse}").execute().get('values', [])
                    self.rowInColumnInUse += 1
                    self.cellInUse = f"{self.columnInUse}{self.rowInColumnInUse}"

                except HttpError as error:
                    print(error)

            if choice == "exit":
                self.screenshot()
                break

    def screenshot(self):
        """This method creates a graph from the given data in the google API, takes a picture of it, and then
        sets that picture as my background."""
        month = self.values_for_column_in_use[0][0]
        month_index = None
        for index, months in enumerate(BudgetYear.MONTH):
            if month == months:
                month_index = index
                break
        # Here we have this disaster of a code that gives me the last months expeneses and the current month's expenses
        last_month_expenses = np.cumsum([float(item[0]) for item in self.getcolumn(1)[1:]])[-1]

        list_of_expenses = [float(item[0]) for item in self.values_for_column_in_use[1:]]
        cumulative_sums = np.cumsum((list_of_expenses))
        cumulative_sums= np.insert(cumulative_sums, 0, 0)


        fig, ax = plt.subplots()
        ax.plot(range(len(cumulative_sums)), cumulative_sums, marker='o', linestyle='-', color="gray")
        fig.set_facecolor((0.06, 0.06, 0.06))
        ax.set_facecolor("black")
        ax.set_xlabel("Purchase Number", color="white")
        ax.set_ylabel("Amount Spent", color="white")
        ax.tick_params(axis="both", color="gray")
        for axis in [ax.xaxis, ax.yaxis]:
            for label in axis.get_ticklabels():
                label.set_color((0.50, 0.25, 0.25))

        for spine in ax.spines.values():
            spine.set_edgecolor("gray")

        final_spent = cumulative_sums[-1]  # Gets the last value of cumulative_sums
        ax.set_xlim([0, len(cumulative_sums)])  # Assuming your x-axis starts at 0
        ax.set_ylim([0, max(cumulative_sums) * 1.1])
        text_position_x = len(cumulative_sums)* .25   # This is saying based on the maximum x value, put the text at the position of the multiplier
        text_position_y = max(cumulative_sums) * 1.17  # This is saying based on the maximum y value, put the text at the position of the multiplier
        ax.text(text_position_x,
                text_position_y,
                f"You have spent ${final_spent:.2f} so far in {month} \n In {BudgetYear.MONTH[month_index-1]} you spent ${last_month_expenses:.2f}",
                 color="white")

        #Show the plot and save it as an image.
        plt.grid(True)
        plt.savefig("expenses_plot.png")
        plt.show()

        screen_width = 2540
        screen_height = 1440
        image_path = r"C:\Users\Timot\PycharmProjects\BudgetProject\expenses_plot.png"
        resize_image_to_fit_screen(image_path, screen_width, screen_height)

        screen_resolutions = [(2560, 1440),
                              (1920, 1080)]
        image_path = create_multi_monitor_wallpaper(r"C:\Users\Timot\PycharmProjects\BudgetProject\expenses_plot.png",
                                                    screen_resolutions)

        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)


def create_multi_monitor_wallpaper(center_image_path, screen_resolutions):
    """
    Creates a multi-monitor wallpaper.

    center_image_path: The path to the image you want on the center monitor.
    screen_resolutions: A list of (width, height) tuples for each monitor, in order.
    """

    total_width = sum([res[0] for res in screen_resolutions])
    max_height = max([res[1] for res in screen_resolutions])

    # Create a blank image with the combined resolution
    combined_img = Image.new("RGB", (total_width, max_height), color="black")

    # Open the center image
    center_img = Image.open(center_image_path)

    # Calculate starting position for the center image
    left_width = screen_resolutions[0][0]
    start_x =  10
    start_y = 0

    # Paste the center image onto the blank image
    combined_img.paste(center_img, (start_x, start_y))

    # Save the combined image
    combined_img.save("combined_wallpaper.png")

    return r"C:\Users\Timot\PycharmProjects\BudgetProject\combined_wallpaper.png"


def resize_image_to_fit_screen(image_path, screen_width, screen_height):
    """Resizes the Png file in the screenshot method to fit my screen."""
    with Image.open(image_path) as img:
        # Calculate aspect ratios
        screen_aspect_ratio = screen_width / screen_height
        image_aspect_ratio = img.width / img.height

        # Resize based on width or height


        # Resize the image
        img_resized = img.resize((screen_width, screen_height), Image.LANCZOS)

        # Save the resized image
        img_resized.save(image_path)
