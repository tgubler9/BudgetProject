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



def main():

    objectj = budgetYear.BudgetYear()

    print(objectj.values_of_first_row)
    
    objectj.screenshot()





if __name__ == "__main__":
    main()

# We want this to be in a while loop
# I want to display the current month and its expenses but only during the first iteration of the while loop, and then
# after I want it to ask you.
