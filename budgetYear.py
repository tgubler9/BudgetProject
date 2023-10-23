import os
import matplotlib.pyplot as plt
import numpy as np
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import ctypes
from PIL import Image


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
                                                      ).execute().get('values', [])[0]
        self.columnInUse = chr(ord("A") + len(self.values_of_first_row) - 1)
        self.values_for_column_in_use = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID,
                                                range=f"{self.columnInUse}:{self.columnInUse}").execute().get('values',[])
        self.rowInColumnInUse = len(self.values_for_column_in_use) + 1
        self.cellInUse = f"{self.columnInUse}{self.rowInColumnInUse}"





    def get_values(self, cell_range):
        """ This is a getter method used to grab data from the google sheets."""
        self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, range=cell_range).execute().get("values", [])

    #This is a main loop for the program. It will allow you to enter or get info from the google sheets. You can also
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

    def while_loop(self):
        """ You can enter or see data in from the google sheets with the range. You can exit the loop by typing exit"""
        while (choice := input("Type \"get\" or \"enter\" or \"exit\" to get info, enter info, or exit.")) != "exit":

            if choice == "get":
                inputrange = input("Enter in cell that you want to see or cell range.")

                try:
                    result = self.get_values(inputrange)
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
                break

    def screenshot(self):
        """This method creates a graph from the given data in the google API, takes a picture of it, and then
        sets that picture as my background."""
        month = self.values_for_column_in_use[0][0]
        list_of_expenses = [float(item[0]) for item in self.values_for_column_in_use[1:]]
        cumulative_sums = np.cumsum((list_of_expenses))


        fig, ax = plt.subplots()
        ax.plot(range(len(cumulative_sums)), cumulative_sums, marker='o', linestyle='-', color="gray")
        fig.set_facecolor((0.06, 0.06, 0.06))
        ax.set_facecolor("black")
        ax.set_xlabel("Purchase Number", color="white")
        ax.set_ylabel("Total Amount Spent", color="white")
        ax.set_title("Running Total of Purchases")
        ax.tick_params(axis="both", color="gray")
        for axis in [ax.xaxis, ax.yaxis]:
            for label in axis.get_ticklabels():
                label.set_color((0.50, 0.25, 0.25))

        for spine in ax.spines.values():
            spine.set_edgecolor("gray")

        final_spent = cumulative_sums[-1]  # Gets the last value of cumulative_sums
        text_position_x = len(cumulative_sums) * 0.15  # Adjust this as needed to place the text at desired x-coordinate
        text_position_y = max(cumulative_sums) * 1.15  # Adjust this as needed to place the text at desired y-coordinate
        ax.text(text_position_x, text_position_y, f"You have spent ${final_spent:.2f} so far in {month} and you spent", color="white")

        #Show the plot and save it as an image.
        plt.grid(True)
        plt.savefig("expenses_plot.png")
        plt.show()

        screen_width = 2540
        screen_height = 1440
        image_path = r"C:\Users\Timot\PycharmProjects\BudgetProject\expenses_plot.png"
        resize_image_to_fit_screen(image_path, screen_width, screen_height)

        screen_resolutions = [(1920, 1080), (2560, 1440),
                              (1920, 1080)]  # Adjust these values to your monitors' resolutions
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
    start_x = left_width + 10
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
