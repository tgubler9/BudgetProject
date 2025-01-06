import csv
import budgetYear
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sklearn.linear_model

def main():
    #obj = budgetYear.BudgetYear()
    #df = obj.get_whole_sheet()

    df = pd.read_csv("sheet1.csv")
    for column in df.columns:
        df[column] = df[column].astype(str).str.replace(',', '').astype(float)




    month_mapping = {
        "January": 1, "February": 2, "March": 3,
        "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9,
        "October": 10, "November": 11, "December": 12
    }
    new_data = {
        'Month_Number': [],
        'Total_Spending': [],
        'Number_of_Items': []
    }
    for month_name, values in df.items():
        total_spending = sum(values.dropna())
        number_of_items = values.count()

        month_number = month_mapping[month_name]
        new_data['Month_Number'].append(month_number)
        new_data['Total_Spending'].append(total_spending)
        new_data['Number_of_Items'].append(number_of_items)



    print(df.dtypes)
    newdf = pd.DataFrame(new_data)

    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111,projection='3d')
    ax.scatter(newdf['Month_Number'], newdf['Number_of_Items'], newdf['Total_Spending'], c='r', marker='o')

    ax.set_xlabel('Month Number')
    ax.set_ylabel('Number of Items')
    ax.set_zlabel('Total Spending')
    print('hi')
    plt.title('3D Scatter Plot of Spending Data')
    ax.view_init(elev=0, azim=90)
    plt.show()

    X = newdf[['Month_Number', 'Number_of_Items']]
    Y = newdf['Total_Spending'].values

    model = sklearn.linear_model.LinearRegression()
    model.fit(X,Y)
    prediction_input = pd.DataFrame([[1, 35]], columns=['Month_Number', 'Number_of_Items'])
    prediction = model.predict(prediction_input)
    print(prediction)


if __name__ == "__main__":
    main()
