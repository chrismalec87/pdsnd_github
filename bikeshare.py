import os
import time
import pandas as pd
from datetime import timedelta as td

"""Current directory"""

path = os.getcwd()

""" dictionary describing data file locations """

city_data = { 'chicago': path + '\chicago.csv',
              'new york city': path + '\new_york_city.csv',
              'washington': path + '\washington.csv' }

""" sets of acceptable month / day user responses """

months = ("january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december", "all")

days = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all")



def get_filters():
    """ get_flters fuction asks the user for the city, month and day filters and returns those values in lower case """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    valid_city = valid_month = valid_day = False
    
    while not valid_city:
        city = input("Which city's data would you like to explore? Please select Chicago, New York City or Washington.\n").lower()
        if city in city_data:
            valid_city = True
        else:
            print("You have not selected a valid city, please try again.")

    while not valid_month:
        month = input("Which month would you like to examine? Please select a month or 'All' if you would like to look at all months.\n").lower()
        if month in months:
            valid_month = True
        else:
            print("You have not selected a valid month, please try again.")

    while not valid_day:
        day = input("Which day would you like to examine? Please select a day or 'All' if you would like to look at all days.\n").lower()
        if day in days:
            valid_day = True
        else:
            print("You have not selected a valid city, please try again.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
        df_unfiltered = Pandas DataFrame containing city data without any filtering
    """
    
    month = month.capitalize()
    day = day.capitalize()
    
    df = pd.read_csv(city_data[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    df['Start Time'] = pd.to_datetime(df['End Time'], format='%Y-%m-%d %H:%M:%S')
    
    df = df.astype({'Trip Duration':float})
    
    df['Start Day'] = df['Start Time'].dt.day_name()
    df['Start Month'] = df['Start Time'].dt.month_name()
    df['Start Hour'] = df['Start Time'].dt.hour
    
    df['Trip Station Pair'] = list(zip(df['Start Station'], df['End Station']))
    
    df_unfiltered = df
    
    if month != 'All':
        df = df[df['Start Month'] == month]
        
    if day != 'All':
        df = df[df['Start Day'] == day]
     

    return df, df_unfiltered


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['Start Month'].mode()[0]
    most_common_day = df['Start Day'].mode()[0]
    most_common_hour = df['Start Hour'].mode()[0]
    
    print('The most common month was:\n{}\n'.format(most_common_month))
    print('The most common day was:\n{}\n'.format(most_common_day))
    print('The most common start hour was:\n{}:00\n'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start = df['Start Station'].mode()[0]
    most_common_end = df['End Station'].mode()[0]
    most_common_trip = df['Trip Station Pair'].mode()[0]

    print('The most common start station was:\n{}\n'.format(most_common_start))
    print('The most common end station was:\n{}\n'.format(most_common_end))
    print('The most common trip was:\n{}\tto\t{}\n'.format(most_common_trip[0],most_common_trip[1]))
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = str(td(seconds=df['Trip Duration'].sum()))
    mean_travel_time = str(td(seconds=df['Trip Duration'].mean()))

    print('The total travel time was:\n{}\n'.format(total_travel_time))
    print('The mean travel time was:\n{}\n'.format(mean_travel_time))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_breakdown = df.groupby(['User Type'])['User Type'].count()
    
    print('The user breakdown for passengers is:\n{}\n'.format(user_breakdown))
    
    if city == 'new york city':
        gender_breakdown = df.groupby(['Gender'])['Gender'].count()
        min_birth_year = int(df['Birth Year'].min())
        max_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        
        print('The gender breakdown for passengers is:\n{}\n'.format(gender_breakdown))
        print('The earliest birth year is:\n{}\n'.format(min_birth_year))
        print('The most recent birth year is:\n{}\n'.format(max_birth_year))
        print('The most common birth year is:\n{}\n'.format(most_common_birth_year))
    else:
        print('No gender or birth year data available for the selected city.')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """Displays raw (unfiltered) data to user in 5 row blocks."""
    
    row_limit = df.shape[0]
    first_row = 0
    last_row = 4
    
    show_data = input('\nWould you like to view the raw data? Enter yes or no.\n').lower()
    
    while show_data == 'yes' or show_data == 'y':
        
        if last_row >= row_limit:
            last_row = row_limit
            print(df.loc[first_row:last_row,:])
            print('END OF DATA')
            break
            
        print(df.loc[first_row:last_row,:])
        show_data = input('\nWould you like to view the next 5 rows of raw data? Enter yes or no.\n').lower()
        first_row += 5
        last_row += 5
        
    
def main():
    while True:
        city, month, day = get_filters()
        df, df_unfiltered = load_data(city, month, day)
        print("slected {},{},{}".format(city, month, day))
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        show_raw_data(df_unfiltered)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
