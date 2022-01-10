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
    cities = ['chicago', 'new york city', 'washington']
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city would you like to explore? Chicago, New York City, or Washington?\n')
    city = city.lower()
    #checks to make sure we have received valid input
    while city not in cities:
        print('Invalid input, please try again.\n')
        city = input('Which city would you like to explore? Chicago, New York City, or Washington?\n')
        city = city.lower()
        if city in cities:
            break

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Which month would you like to see data for? \nJanuary, February, March, April, May, June, or all?\n')
    month = month.lower()
    #checks to make sure we have received valid input
    while month not in months:
        print('Invalid input, please try again.\n')
        month = input('Which month would you like to see data for? \nJanuary, February, March, April, May, June, or all?\n')
        month = month.lower()
        if month in months:
            break
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day would you like to see data for? \nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?')
    day = day.lower()
    #checks to make sure we have received valid input
    while day not in days:
        print('Invalid input, please try again.\n')
        day = input('Which day would you like to see data for? \nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?')
        day = day.lower()
        if day in days:
            break


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
    # load data from the selected city
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        #capitalize day of the week to remain uniform
        day = day.title()
        #filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]


    return df


def time_stats(df):
    months = ['january', 'february', 'march', 'april', 'may', 'june']

    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_index = df['month'].mode()[0]
    common_month = months[month_index - 1].title()
    print('The most popular month was: ', common_month)


    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most popular day was: ', common_day)

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most popular hour was: ', common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most popular Start Station was: ', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most popular End Station was: ', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    combo_start, combo_end = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most frequent combination of Start and End Stations is: {} and {}'.format(combo_start, combo_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    print('The total travel time over this period was: {} minutes'.format(tot_travel_time))


    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average travel duration over this period was: {} minutes'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_count = df['User Type'].value_counts()
    print('The counts of different user types was:\n')
    for user, count in enumerate(user_count):
          print('{}: {}'.format(user_count.index[user], count))

    # TO DO: Display counts of gender
    print()
    #skip gender and birth analysis if washington has been selected as the city
    # because Washington is missing this data
    if city == 'washington':
        print('\nWashington did not collect gender and birth year data, we will skip this data and continue...\n')
    else:
        gender_count = df['Gender'].value_counts()
        print('The counts of different genders was:\n')
        for gender, count in enumerate(gender_count):
              print('{}: {}'.format(gender_count.index[gender], count))

        print()
        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth = int(df['Birth Year'].min())
        print('The earlist year of birth was: ', earliest_birth)

        latest_birth = int(df['Birth Year'].max())
        print('The most recent year of birth was: ', latest_birth)

        mode_birth = int(df['Birth Year'].mode()[0])
        print('The most common year of birth was: ', mode_birth)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data_viewer(df):
    """Gives the user the option to view 5 rows of data from the dataframe"""
    #we initialize by asking the user if they would like to view the data
    user_input = input('Would you like to see some of the raw data from the dataframe?\n yes or no?')
    user_input = user_input.lower()
    while user_input not in ['yes', 'no']:
        print('\nPlease answer yes or no')
        user_input = input('Would you like to see some of the raw data from the dataframe?\n yes or no?')
        user_input = user_input.lower()
        if user_input in ['yes', 'no']:
            break
    #initialize the counter at 0 so we can track when we have displayed 5 rows of data
    counter = 0
    boolean = True
    while boolean:
        #print the first 5 rows
        print(df.iloc[counter:counter + 5])
        #increase the count for the next 5 rows
        counter +=5
        #ask if they would like to see more
        more = input('Would you like to see five more? yes or no\n').lower()
        #checks to make sure we have received valid input
        while more not in ['yes', 'no']:
            more = input('Please answer yes or no\n')
            if more in ['yes', 'no']:
                break
        if more == 'no':
            boolean = False
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data_viewer(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
