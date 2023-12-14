"""
Name:       Nicholas Lewis
CS230:      Section 2
Data:       Parking Meters
URL:

Description:
This program is designed to run using streamlit/pandas, appear in a browser, and show data about the Boston parking
meters file

Histogram code for vendors was gathered from ChatGPT. See section 1 for further explanation.
Histogram code for streets was gathered from ChatGPT. See section 2 for further explanation.
Pie Chart code was gathered from ChatGPT. See section 3 for further explanation.
"""

# Import packages for data analysis/maps/charts
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# constant for parking meter data file
FILE = "Parking_Meters.csv"


# dataframe for parking meter data
def dataframe(FILE, column):
    # create dataframe from file
    df = pd.read_csv(FILE)
    # clean up rows with missing info from desired column
    dfClean = df.dropna(subset=[column])
    return dfClean


# make page 1 for Queries
def page1():
    # give the page a title
    st.title("Queries:")

    # call the dataframe cleaning function
    dfClean = dataframe(FILE, "STREET")
    # get desired street from drop-down
    des_street = st.selectbox('How Many Parking Meters Are On ___ (Street)?:', dfClean['STREET'].unique())
    # call the street function
    street(dfClean, des_street)
    # insert a line
    st.write("-"*50)

    # call the dataframe cleaning function
    dfClean = dataframe(FILE, "VENDOR")
    # get desired vendor from drop-down
    des_vendor = st.selectbox(f'How Many Parking Meters on {des_street} Were Produced by ___ (Vendor)?:',
                              dfClean['VENDOR'].unique())
    # call the vendor function and give it the street from earlier
    vendor(dfClean, des_vendor, des_street)
    # insert a line
    st.write("-" * 50)

    # call the dataframe cleaning function
    dfClean = dataframe(FILE, "BASE_RATE")
    # call cheap function for cheapest
    price, meter_id, streetN = cheap(dfClean)
    # print results
    st.header(f"The Cheapest Meter is Meter ID: {meter_id} with a Base Rate of ${price} on {streetN}")

    # call the dataframe cleaning function
    dfClean = dataframe(FILE, "BASE_RATE")
    # call expensive function for most expensive
    price, meter_id, streetN = expensive(dfClean)
    st.header(f"The Most Expensive Meter is Meter ID: {meter_id} with a Base Rate of ${price}0 on {streetN}")


# make page 2 for Graphs
def page2():
    # give the page a title
    st.title("Graphs:")

    # header for the 2 histograms
    st.header("Histograms:")

    # call the dataframe cleaning function
    dfClean = dataframe(FILE, "VENDOR")
    # call the vendor histogram function
    histogramV(dfClean)

    # call the dataframe cleaning function
    dfClean = dataframe(FILE, "STREET")
    # call the street histogram function
    histogramS(dfClean)

    # header for the pie chart
    st.header("Pie Chart:")

    # call the dataframe cleaning function
    dfClean = dataframe(FILE, "STREET")
    # get the user input for top # of streets for pie chart using slider
    topX = st.slider("Select To See Top 1-9 + Others:", min_value=1, max_value=9, value=1)
    # call the street pie chart function
    pieS(dfClean, topX)


# make page 3 for the map
def page3():
    # give the page a title
    st.title("Maps:")

    # header for the basic map
    st.header("Basic Map:")

    # call the dataframe cleaning function
    dfClean = dataframe(FILE, "LATITUDE")
    # call the map function
    map(dfClean)

    # header for the filtered map
    st.header("Filtered Map:")

    # call the dataframe cleaning function
    dfClean = dataframe(FILE, "LATITUDE")
    # get desired street from drop-down
    des_street = st.selectbox('Select a Street to Filter the Map By:', dfClean['STREET'].unique())
    # call the filtered map function
    mapF(dfClean, des_street)


# query to find how many parking meters are on street
def street(df, street):
    # counts the values for the different streets and returns a series counting unique values
    total = df["STREET"].value_counts()
    st.write(f'The Total Number of Meters on {street} is:')
    # prints the total amount of meters on the selected street by taking that row from the series
    st.header(f"{total[street]}")

# query to find how many parking meters on a street are of desired vendor
def vendor(df, vendor, street1):
    # creates series based on how vendor count grouped by street then counts each with .size()
    total = df[df['VENDOR'] == vendor].groupby('STREET').size()
    # if statement to see if desired street is in that series, if not prints value of 0
    if street1 in total:
        st.write(f'The Total Number of Meters on {street1} Produced by {vendor} is:')
        st.header(f"{total[street1]}")
    else:
        st.header("0")


# pre-formed query about cheapest meter price
def cheap(df):
    # writes pre-formed query
    st.write("What is the Cheapest Meter Price in Boston?")
    # sorts dataframe by base rate in ascending order
    df = df.sort_values("BASE_RATE", ascending=True)
    # sets the price, meter ID, and street equal to the values of the first row
    price = df["BASE_RATE"].iloc[0]
    meter_id = int(df["METER_ID"].iloc[0])
    streetN = df["STREET"].iloc[0]
    # returns the 3 values to be printed
    return price, meter_id, streetN


# pre-formed query about most expensive meter price
def expensive(df):
    # writes pre-formed query
    st.write("What is the Most Expensive Meter Price in Boston?")
    # sorts dataframe by base rate in descending order
    df = df.sort_values("BASE_RATE", ascending=False)
    # sets the price, meter ID, and street equal to the values of the first row
    price = df["BASE_RATE"].iloc[0]
    meter_id = int(df["METER_ID"].iloc[0])
    streetN = df["STREET"].iloc[0]
    # returns the 3 values to be printed
    return price, meter_id, streetN


# create a histogram of the vendor data
def histogramV(df):
    # create histogram fom VENDOR column with color red
    sns.histplot(df['VENDOR'], color="red")
    # give the histogram a title
    plt.title("Meters by Vendor")
    # give the x-axis a title
    plt.xlabel("Vendor")
    # give the y-axis a title
    plt.ylabel("Frequency")
    # add gridlines
    plt.grid(axis="y", alpha=0.5)
    # Hide out-dated warning message
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # write histogram to page
    st.pyplot()


# create a histogram of the street data
def histogramS(df):
    # get the top 7 most populated streets
    top7 = df['STREET'].value_counts().nlargest(7)
    # make the graph width 8, height 6
    plt.figure(figsize=(8, 6))
    # create histogram using just the top 7 streets, make the color blue
    sns.histplot(df[df['STREET'].isin(top7.index)]['STREET'], color="blue")
    # give the histogram a title
    plt.title("Meters by Street (Top 7)")
    # change the size of the category fonts
    plt.xticks(fontsize=5.5)
    # give the x-axis a title
    plt.xlabel("Street")
    # give the y-axis a title
    plt.ylabel("Frequency")
    # add gridlines
    plt.grid(axis="y", alpha=0.5)
    # hide out-dated warning message
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # write histogram to page
    st.pyplot()


# Create a pie chart for the street data with a slider to show top 1-9 + others
def pieS(df, threshold=5):
    # from ChatGPT
    value_counts = df['STREET'].value_counts()
    included_values = value_counts.index[:threshold].tolist()
    df['STREET'] = df['STREET'].apply(lambda x: x if x in included_values else 'Other')
    value_counts = df['STREET'].value_counts()
    # create pie chart using values, street names as labels, and percent
    plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%')
    # add a legend in the top right
    plt.legend(loc="upper right")
    # give the pie chart a title
    plt.title('Pie Chart for Street')
    # write pie chart to page
    st.pyplot()


# create a map
def map(df):
    # creates and writes map
    st.map(df)


# created a map filtered by street
def mapF(df,street):
    filter = df[df['STREET'] == street]
    st.map(filter)


# main function to set up the sidebar
def main():
    # give the same title to each page
    st.title("BOSTON PARKING METERS")
    # create a title for the sidebar navigation tool
    st.sidebar.title("Page Navigation")
    # create a dictionary for the pages
    pages = {'Page 1': page1, 'Page 2': page2, 'Page 3': page3}
    # allows user to select which page using the pages dictionary keys
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    # calls the function based on user selection
    pages[selection]()


# Calls main function
main()
