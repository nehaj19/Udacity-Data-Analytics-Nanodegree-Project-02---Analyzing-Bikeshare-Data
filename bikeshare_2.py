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
        city = input('Would you like to see data for Chicago , New York or Washington ?\n')
        if city.lower() not in ('chicago', 'new york', 'washington'):
            print("Not an appropriate choice.")
        else:
            break

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        filter = input('Would you like to filter by month , day , both or none?\n')
        if filter.lower() not in ('month', 'day', 'both', 'none'):
            print("Not an appropriate choice.")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    if filter == 'month' or filter == 'both' :
        while True:
            month = input('Which month : January , February , March, April, May , June?\n')
            day = ''
            if month.lower() not in ('january' , 'february' , 'march', 'april', 'may' , 'june' ):
                print("Not an appropriate choice.")
            else:
                break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter == 'day' or filter == 'both' :
        while True:
            day = input('Which day : Monday , Tuesday ,Wednesday, Thursday, Friday?\n')
            month = ''
            if day.lower() not in ('monday' , 'tuesday' , 'wednesday', 'thursday', 'friday'):
                print("Not an appropriate choice.")
            else:
                break

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

    df1['Start Time'] = pd.to_datetime(df1['Start Time'])

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

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Start_Used_Station = df['Start Station'].value_counts().idxmax()
    Count = df['Start Station'].value_counts().max()

    # display most commonly used end station
    End_Used_Station= df['End Station'].value_counts().idxmax()
    Count1 = df['End Station'].value_counts().max()

    # display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station'] + '  and  ' +  df['End Station']
    Combinations = df['Combination'].value_counts().idxmax()
    Count2 = df['Combination'].value_counts().max()

    print('Common used start station : {}, Count : {}\nCommon used end station : {}, Count : {}'.format(Start_Used_Station,Count,End_Used_Station,Count1))
    print('Most frequent combination of start station and end station trip : {}, Count : {}'.format(Combinations,Count2))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

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

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    User = df['User Type'].value_counts()
    print('User types : \n{}'.format(User))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats1(df):
    print('\nCalculating User Birth Stats...\n')
    start_time = time.time()
    # Display earliest, most recent, and most common year of birth
    df = df[np.isfinite(df['Birth Year'])]
    df = df.astype({"Birth Year":int}, copy=False)
    Earliest = df['Birth Year'].min()
    Recent = df['Birth Year'].max()
    common = df['Birth Year'].value_counts().idxmax()
    print('Earliest year of birth : {} \nRecent year of birth : {}\nMost common year of birth : {}'.format(Earliest,Recent,common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # Washington city do not have birth year data,so using a different function for only Chicago and New York
        if city.lower() in ('chicago', 'new york'):
            user_stats1(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
