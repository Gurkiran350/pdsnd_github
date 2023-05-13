import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
    city_name = ['chicago', 'new york city', 'washington']
    while True:
        city = input('Which city would you like to see data for (e.g. chicago, new york city or washington)\n').lower()
        if city in city_name:
            break
        else:
            print('Please enter a valid city name(chicago, new york city or washington). \n')

        # get user input for month (all, january, february, ... , june)

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('Which month would you like to see data for (e.g. all, january, february, march, april, may, june)\n').lower()
        if month in months:
            break
        else:
            print('Please enter a valid city month./')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('Which day would you like to see data for (e.g. all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)\n').lower()
        if day in day_of_week:
            break
        else:
            print('Please enter a valid city day')

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

     # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month of travel:', common_month)

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('Most common day of week:', common_day_of_week)


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('Most common start hour of the day:', common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_counts = df['Start Station'].value_counts()
    common_start_station = start_station_counts.idxmax()
    count_common_start_station = start_station_counts.max()
    print('Most commonly used start station is:', common_start_station)
    print('Count:', count_common_start_station)


    # display most commonly used end station
    end_station_counts = df['End Station'].value_counts()
    common_end_station = end_station_counts.idxmax()
    count_common_end_station = end_station_counts.max()
    print('Most commonly used start station is:', common_end_station)
    print('Count:', count_common_end_station)


    # display most frequent combination of start station and end station trip
    trip_counts = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    popular_station = trip_counts.loc[trip_counts['count'].idxmax()]
    print('The most common trip from start to end is from {} to {}, with a count of {}.'.format(popular_station['Start Station'], popular_station['End Station'], popular_station['count']))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Compute total and mean travel time
    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    # Display results
    print(f'Total duration of this trip is: {total_travel_time}')
    print(f'The mean travel time of this trip is: {mean_travel_time}')
    print(f'\nThis took {time.time() - start_time:.2f} seconds.')
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The user types are:', user_types)

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('The gender of people travelling are:', gender_count)
    
    except:
        print('The gender count data is not available')

    # Display earliest, most recent, and most common year of birth
    try:
        most_earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('The most earliest passenger birth year is:', most_earliest_birth_year)
        print('The most recent passenger birth year is:', most_recent_birth_year)
        print('The most common passenger birth year is:', most_common_birth_year)
    except:
        print('The birth year data is not available')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data to the customer"""

    raw_data = input('Would you like to view raw data? Enter yes or no?').lower()
    start_location = 0
    while True:
        if raw_data == 'no':
            break
        if raw_data == 'yes':
            pd.set_option('display.max_columns',200)
            print(df[start_location:start_location+5])
            raw_data = input('Would you like to view 5 more rows of data? Enter yes or no?').lower()
            start_location += 5
        else:
            raw_data = input('Your input is invalid. Please enter only yes or no').lower()
        
    return df


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
