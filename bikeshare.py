import time
import calendar
import pprint
import pandas as pd
import numpy as np

CITY_DATA = ['chicago.csv', 'new_york_city.csv', 'washington.csv']

def check_input(msg, valid_choice):
    """
    checks if the user's input is a valid choice, and a number.

    Args:
        (str) msg - a message to be displayed for the user when asking for his input
        (list) valid_choice - a list of the valid choices for an input to be checked
    Returns:
        (int) user_input - after its been checked
    """
    while True:
        try:
            # ask for user input
            user_input = int(input(msg))

            # check if the input is valid
            if user_input in valid_choice:
                break

            print("\n-- Invalid choice, please enter a value from the given choices --\n")

        except ValueError:
            print('\n-- Invalid number, please enter numbers only --\n')

    return user_input


def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        (int) city - city number (0,1,2)
        (int) month - month number (1 to 6) or -1 (no filter)
        (int) day - day number (0 to 6) or -1 (no filter)
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    msg = 'Would you like to see data for Chicago, New York, or Washington?\n' \
    'Enter (0 for Chicago, 1 for New York, or 2 for Washington)\n'
    city = check_input(msg, [0, 1, 2])

    msg = '\nWould you like to filter the data by month, day, both, or not at all??\n' \
    'Enter (0 for month, 1 for day, 2 for both, or 3 for no filter)\n'
    user_filter = check_input(msg, [0, 1, 2, 3])

    # initial values in case the user didn't want to filter by them both or one of them
    month = -1
    day = -1

    # ask for month number
    # only if the user didn't chose to filter by day or no filter
    if user_filter not in (1, 3):
        msg = '\nWich month?\nEnter (1 for January, 2 for February,' \
        ' 3 for March\n4 for April, 5 for May, or 6 for June)\n'
        month = check_input(msg, [1, 2, 3, 4, 5, 6])

    # ask for day number
    # only if the user didn't chose to filter by month or no filter
    if user_filter not in (0, 3):
        msg = '\nWich day?\nEnter (0 for Monday, 1 for Tuesday,' \
        ' 2 for Wednesday\n3 for Thursday, 4 for Friday, 5 for Saturday, or 6 for Sunday)\n'
        day = check_input(msg, [0, 1, 2, 3, 4, 5, 6])

    print()
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city (and filters by month or day or both if applicable).

    Args:
        (int) city - city number (0,1,2)
        (int) month - month number (1 to 6) or -1 (no filter)
        (int) day - day number (0 to 6) or -1 (no filter)
    Returns:
        df - Pandas DataFrame containing city data (filtered by month or day or both if applicable)
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of the week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != -1:
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of the week if applicable
    if day != -1:
        # filter by day of the week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # extract hour from Start Time to create new column
    df['hour'] = df['Start Time'].dt.hour

    # find the most frequent month, only if the user chose to not filter by month
    if month == -1:
        popular_month = df['month'].mode()[0]
        count_month = df['month'].value_counts().max()
        month_name = calendar.month_abbr[popular_month]
        print('Most Frequent Month:\n{} - {} (Count: {})\n'.format(popular_month, month_name, count_month))

    # find the most frequent day, only if the user chose to not filter by day
    if day == -1:
        popular_day = df['day_of_week'].mode()[0]
        count_day = df['day_of_week'].value_counts().max()
        day_name = calendar.day_abbr[popular_day]
        print('Most Frequent Day of Week:\n{} - {} (Count: {})\n'.format(popular_day, day_name, count_day))

    # find the most frequent hour
    popular_hour = df['hour'].mode()[0]
    count_hour = df['hour'].value_counts().max()
    print('Most Frequent Start Hour:\n{} (Count: {})\n'.format(popular_hour, count_hour))

    print("\nThis took %s seconds." % (time.time() - start_time), '\n')
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # create a new column from the combination of start and end stations
    df['trip'] = df['Start Station'] + ' -- ' + df['End Station']

    # most common start station
    popular_start_station = df['Start Station'].mode()[0]
    count_start_station = df['Start Station'].value_counts().max()

    # most common end station
    popular_end_station = df['End Station'].mode()[0]
    count_end_station = df['End Station'].value_counts().max()

    # most common trip
    popular_trip = df['trip'].mode()[0]
    count_trip = df['trip'].value_counts().max()

    print('Most Common Start Station:\n{}'.format(popular_start_station))
    print('(Count: {})\n'.format(count_start_station))

    print('Most Common End Station:\n{}'.format(popular_end_station))
    print('(Count: {})\n'.format(count_end_station))

    print('Most Common Trip:\n{}'.format(popular_trip))
    print('(Count: {})\n'.format(count_trip))

    print("\nThis took %s seconds." % (time.time() - start_time), '\n')
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total Travel Time:\n{}\n'.format(df['Trip Duration'].sum()))
    print('Average Travel Time:\n{}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time), '\n')
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('Counts of each user type:\n{}\n\n'.format(df['User Type'].value_counts().to_string()))

    # counts of each gender and earliest, most recent, and most common year of birth
    # only if the city is Chicago 0, or NYC 1
    if city in (0, 1):
        print('Counts of each gender:\n{}'.format(df['Gender'].value_counts().to_string()))
        print('Not Specified     ', df['Gender'].isna().sum(), '\n\n')

        count_birth_year = df['Birth Year'].value_counts().max()
        print('Earliest Birth Year:\n{}\n'.format(int(df['Birth Year'].min())))
        print('Most recent Birth Year:\n{}\n'.format(int(df['Birth Year'].max())))
        print('Most Common Birth Year:\n{} (Count: {})\n'.format(int(df['Birth Year'].mode()[0]), count_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time), '\n')
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        msg = '\nWould you like to see the raw data?\n' \
        'Enter (1 for yes, or 0 for no)\n'
        user_input_raw_data = check_input(msg, [0, 1])

        if user_input_raw_data == 1 :
            # start and end counters for slicing df
            s_counter = 0
            e_counter = 5
            while True:
                # convert df sliced records to a dictionary and print it
                pprint.pprint(df[s_counter:e_counter].to_dict('records'))
                print('-'*40)
                s_counter = e_counter
                e_counter += 5

                msg = '\nWould you like to see more of the raw data?\n' \
                'Enter (1 for yes, or 0 for no)\n'
                user_input_raw_data = check_input(msg, [0, 1])

                if user_input_raw_data == 0:
                    break

        msg = '\nWould you like to restart?\n' \
        'Enter (1 for yes, or 0 for no)\n'
        restart = check_input(msg, [0, 1])
        if restart == 0:
            break


if __name__ == "__main__":
    main()
