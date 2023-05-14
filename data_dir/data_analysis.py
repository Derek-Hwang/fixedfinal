#pip install pandas matplotlib streamlit openpyxl

#to open the web browser:
#streamlit run data_analysis.py --server.enableCORS false --server.enableXsrfProtection false

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

@st.cache_data()
def load_data(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path, usecols=['date', ' Per 1000 Population'], header=1)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df['date'] = df['date'].dt.year # extract year from date column
    df = df.rename(columns={'date': 'Year'}) # rename column to 'Year'
    df.set_index('Year', inplace=True)
    return df

def main():
    # Define the file path
    file_path = 'taiwan-population-2023-04-16 (3).csv'

    # Load the data using the cached function
    df = load_data(file_path)

    # Select rows 53-76 from the dataframe
    df_selected = df.iloc[51:74]
    
    # Multiply each value in the 'Per 1000 Population' column by 20
    df_selected[' Per 1000 Population'] = df_selected[' Per 1000 Population'] * 800

    # Read the Excel sheet and select only the 'Year' and 'Enterprises (Units)' columns
    df_boba = pd.read_excel('OD6250 Bubble Tea Shops in the US Industry Report (3).xlsx', usecols=['Year', 'Enterprises (Units)'], header=0)

    # Create a new DataFrame with the missing years and 0 values
    missing_years = pd.DataFrame({'Year': [2001, 2002, 2003, 2004], 'Enterprises (Units)': [0, 0, 0, 0]})

    # Reset the index of df_selected
    df_selected = df_selected.reset_index()

    # Concatenate the original DataFrame and the missing years DataFrame
    df_boba = pd.concat([missing_years, df_boba], ignore_index=True)

    # Sort the DataFrame by year in ascending order
    df_boba = df_boba.sort_values(by=['Year'])

    # Reset the index
    df_boba = df_boba.reset_index(drop=True)

    # Slice the dataframe to only include the first 20 rows
    df_boba = df_boba.iloc[:23]

    # Create a new DataFrame with both datasets
    df_combined = pd.concat([df_boba, df_selected], axis=1)

     # Add the title to your Streamlit app
    st.title("The Effect of Taiwanese Immigration on the Spread of Boba in the United States")

    # Write analysis
    st.write('The correlation coefficient between the number of bubble tea enterprises and the net migration rate is -0.483, which indicates a mild negative correlation between the two sets of data. This tells us that as Taiwanese net migration rate increased, the number of boba enterprises in the United States decreased. The only reasonable conclusion that we can make with this data is that the original null hypothesis that an increase in Taiwanese net migration rate would increase the number of boba establishments in the United States, is rejected. Instead, we can make some rudimentary assumptions from this result. The first is that there are many confounding variables in this study. For example, a large amount of Taiwanese immigration to the United States already ocurred in the 1980s and 1990s, before the birth of boba. Thus, there were already established Taiwanese communities in the United States such as in Flushing and the San Gabriel Valley. Another question this mild negative correlation raises is whether the boba movement was actually rooted in the United States as an Asian American trend rather than a Taiwanese or Hong Kong invention.')

    # Write Lessons Learned section
    st.write("By creating this project, I learned a lot of things about data analysis, visualization, and boba! First of all, I don't come from a strong coding or statistics background. Over time though, I've become really comfortable of the general coding process and template. I've come to realize that although specific programs and tech stacks may have different functions or tools, the logic behind these different tech stacks are more or less the same. Additionally, these tech stacks are meant to be user-friendly and online documentation provide all the instructions to use the provided tools. Thank you Dr. Tang! Also, this is making me seriously reconsider my national pride in boba.")

    # Add a header for the side by side graphs
    st.header("Bubble Tea Enterprises and Net Migration Rate (Separate)")

    # Create two columns for side by side graphs
    col1, col2 = st.columns(2)

    # Plot Bubble Tea Enterprises on the left column
    fig1, ax1 = plt.subplots()
    ax1.plot(df_boba['Year'], df_boba['Enterprises (Units)'], label='Bubble Tea Enterprises')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Enterprises (Units)')
    ax1.set_title('Bubble Tea Enterprises')
    ax1.legend()
    col1.pyplot(fig1)

    # Plot Net Migration Rate on the right column
    fig2, ax2 = plt.subplots()
    ax2.plot(df_boba['Year'], df_selected[' Per 1000 Population'], label='Net Migration Rate', color='orange')
    ax2.set_xlabel('Year')
    ax2.set_ylabel(' Per 1000 Population')
    ax2.set_title('Net Migration Rate (x800 for scale)')
    ax2.legend()
    col2.pyplot(fig2)

    #Add description of net migration rate
    st.write('Note: The net migration rate per 1000 population (right) is a measure of the number of people who have moved to or from a particular place (such as a country or region) in a given year, relative to the size of the population. It is calculated by subtracting the number of people who have left the place from the number of people who have moved to the place, and then dividing this difference by the size of the population and multiplying it by 1000. This rate can be used to understand the demographic changes in a place, and to compare migration patterns across different places.')

    # Add a header for the main graph
    st.header("Regression Analysis")

    # Plot the two variables together using Matplotlib
    fig, ax = plt.subplots()
    ax.plot(df_boba['Year'], df_boba['Enterprises (Units)'], label='Bubble Tea Enterprises')
    ax.plot(df_boba['Year'], df_selected[' Per 1000 Population'], label='Net Migration Rate')
    ax.set_xlabel('Year')
    ax.set_ylabel('Value')
    ax.set_title('Bubble Tea Enterprises vs Net Migration Rate')
    ax.legend()

    # # Set the x-axis limits
    # ax.set_xlim(2000, 2024)

    # Display the chart using Streamlit
    st.pyplot(fig)
    
    print(df_combined.to_string())

    # Calculate the correlation coefficient between the two variables
    correlation = df_combined['Enterprises (Units)'].corr(df_selected[' Per 1000 Population'])

    # Display the correlation coefficient
    st.write('Correlation Coefficient:', correlation)

    
if __name__ == '__main__':
    main()



