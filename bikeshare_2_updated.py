import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago,New York or Washington?\n')
        if city.lower() not in ('chicago','new york','washington'):
            print("Not an appropriate choice.")
        else:
            break

    # get user input if the data to be filtered by month,day,by both and no filter
    while True:
        filter = input('Would you like to filter by month,day,both or none?\n')
        if filter.lower() not in ('month','day','both','none'):
            print("Not an appropriate choice.")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    if filter == 'month' or filter == 'both' :
        while True:
            month = input('Which month : January,February,March,April,May,June?\n')
            day = ''
            if month.lower() not in ('january','february','march','april','may','june'):
                print("Not an appropriate choice.")
            else:
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter == 'day' or filter == 'both' :
        while True:
            day = input('Which day: Monday,Tuesday,Wednesday,Thursday,Friday,Saturday or Sunday?\n')
            month = ''
            if day.lower() not in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
                print("Not an appropriate choice.")
            else:
                break

    # if user do not filtered the data by month or by a day then setting month and day variables as blank
    if filter == 'none':
        day = ''
        month = ''

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
    """
    city = city.lower()
    df1 = pd.read_csv(CITY_DATA[city])
    # convert column 'Start Time' to datetime to filter the data
    df1['Start Time'] = pd.to_datetime(df1['Start Time'])

    # filtering and loading the data based on user input
    if filter == 'both':
        df = df1[(df['Start Time'].dt.month == month) &  (df['Start Time'].dt.weekday_name == day)]
    elif filter == 'month':
        df = df1[(df['Start Time'].dt.month == month)]
    elif filter == 'day':
        df = df1[(df['Start Time'].dt.weekday_name == day)]
    else:
        df = df1

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    '''
    Args:
    df - Pandas DataFrame containing city data filtered by month and day

    Returns:
        displays statistics on most popular month,week and hour for start time
    '''

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start month'] = df['Start Time'].dt.month
    common_month = df['Start month'].mode()[0]

    # display the most common day of week
    df['Start day'] = df['Start Time'].dt.weekday_name
    common_day = df['Start day'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]

    print('Common month : {} \nCommon day : {} \nCommon start hour : {}'.format(common_month,common_day,common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    '''
    Args:
    df - Pandas DataFrame containing city data filtered by month and day

    Returns:
        displays statistics on most popular start station, end station and trip
    '''

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Start_Used_Station = df['Start Station'].value_counts().idxmax()
    Count = df['Start Station'].value_counts().max()

    # display most commonly used end station
    End_Used_Station= df['End Station'].value_counts().idxmax()
    Count1 = df['End Station'].value_counts().max()

    # display most frequent combination of start station and end station trip
    # combining both columns 'Start Station' and 'End Station'
    df['Combination'] = df['Start Station'] + '  and  ' +  df['End Station']
    Combinations = df['Combination'].value_counts().idxmax()
    Count2 = df['Combination'].value_counts().max()

    print('Common used start station : {}, Count : {}\nCommon used end station : {}, Count : {}'.format(Start_Used_Station,Count,End_Used_Station,Count1))
    print('Most frequent combination of start station and end station trip : {}, Count : {}'.format(Combinations,Count2))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    '''
    Args:
    df - Pandas DataFrame containing city data filtered by month and day

    Returns:
        displays statistics on total and average trip duration
    '''

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Total_time = df['Trip Duration'].sum()

    # display mean travel time
    Average_time = df['Trip Duration'].mean()

    print('Total travel time : {} \nAverage travel time : {}'.format(Total_time,Average_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    '''
    Args:
    df - Pandas DataFrame containing city data filtered by month and day

    Returns:
        displays statistics on counts of each user type
    '''

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    User = df['User Type'].value_counts()

    print('User types : \n{}'.format(User))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats1(df):
    '''Chicago and New York city have birth year data only.Displays statistics on bikeshare users for Chicago and New York cities'''
    '''
    Args:
    df - Pandas DataFrame containing city data filtered by month and day

    Returns:
        displays statistics on earliest, most recent, and most common year of birth
    '''

    print('\nCalculating User Birth Stats...\n')
    start_time = time.time()
    # Display earliest, most recent, and most common year of birth

    # Replacing missing values with zeros
    df = df[np.isfinite(df['Birth Year'])]
    # Converting data type float to integer
    df = df.astype({"Birth Year":int}, copy=False)
    # Display statistics
    Earliest = df['Birth Year'].min()
    Recent = df['Birth Year'].max()
    common = df['Birth Year'].value_counts().idxmax()

    print('Earliest year of birth : {} \nRecent year of birth : {}\nMost common year of birth : {}'.format(Earliest,Recent,common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Asks user to see the rows of data before computing statistics.

    Args:
    df - Pandas DataFrame containing city data filtered by month and day

    Returns:
        df - some rows of Pandas DataFrame containing city data filtered by month and day
    """
    # get user input for displaying the data used for computing the stats
    while True:
        display = input('Would you like to see the rows of data used to compute the stats?' 'Type \'yes\' or \'no\'.\n')
        if display.lower() not in ('yes','no'):
            print("Not an appropriate choice.")
        else:
            break

    # display the data if user input is 'yes'
    if display.lower() == 'yes':
        print(df.head())

    # get user input again for displaying the data used for computing the stats
    if display.lower() == 'yes':
        while True:
            dis = input('Would you like to see more rows of data used to compute the stats?' 'Type \'yes\' or \'no\'.\n')
            if dis.lower() not in ('yes','no'):
                print("Not an appropriate choice.")
            else:
                break
    else :
        dis = 'no'

    # display the data if user input is 'yes'
    if dis.lower() == 'yes':
        print(df[6:11])


def main():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns: descriptive statistics about a city and time period specified by the user via raw input
    '''
    # Filter by city (Chicago, New York, Washington) and by time period (month, day, none)
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        print('Calculating the first statistic...')
        # What is the most popular month,week and hour for start time?
        time_stats(df)
        # What is the most popular start station, end station  and trip?
        station_stats(df)
        # What is the total trip duration and average trip duration?
        trip_duration_stats(df)
        # What are the counts of each user type?
        user_stats(df)
        # What are the earliest (i.e. oldest user), most recent (i.e. youngest user), and most popular birth years?
        # Washington city do not have birth year data,so using a different function for only Chicago and New York
        if city.lower() in ('chicago','new york'):
            user_stats1(df)
        # Display five lines of data at a time if user specifies that they would like to
        display_data(df)

        # Restart?
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
