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
    city = ""    
    city_list = ["chicago", "new york city", "washington"]    
    while city not in city_list:   
        city = input("Enter the city name you wish to explore: \nYou can either pick from chicago, new york city, washington").lower()    
        if city in city_list:    
            print("The city picked is", city)    
        else:
            print('Please! kindly select between chicago, new york city and washington')    
            continue

    # get user input for month (all, january, february, ... , june)
    month = ""    
    month_list = ("all", "january", "february", "march", "april", "may", "june")    
    while month not in month_list:   
        month = input("Enter the month you wish to explore: \nYou can either pick: 'all', 'january', 'february', 'march', 'april', 'may', 'june'").lower()
        if month in month_list:    
            print('The month picked is', month)    
        else:
            print("Please! kindly select between: 'all', 'january', 'february', 'march', 'april', 'may', 'june'")    
            continue


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""    
    day_list = ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")    
    while day not in day_list:   
        day = input("Enter the day you wish to explore: \nYou can either pick: 'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'").lower()
        if day in day_list:    
            print('The day picked is', day)    
        else:
            print("Please! kindly select between: 'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'")    
            continue


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
    df = pd.read_csv(f'{CITY_DATA[city]}', parse_dates=['Start Time', 'End Time'])

        # Drop first column
    df = df.iloc[:,1:]

        # Create month column
    months_dict = {'01': 'january', '02': 'february', '03': 'march', '04':'april', '05': 'may', '06': 'june'}

    df['month'] = df['Start Time'].dt.strftime('%m')
    df['month'] = df['month'].map(months_dict)

        # Create day of week (dow) column
    day_of_week_dict ={0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday', 5: 'saturday', 6: 'sunday'}

    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['day_of_week'] = df['day_of_week'].map(day_of_week_dict)
         # Create an hour column
    df['hour_of_day'] = df['Start Time'].dt.hour
    df['hour_of_day'] = df['hour_of_day'].apply(lambda x: str(x) + ':00')  


        # Filter data
    if month != 'all':
        df = df[df['month'] == month]

        if day != 'all':
            df = df[df['day_of_week'] == day]
    count = 5    
    while True:    
        try:    
            view_data = input('Do you want to view 5 lines of raw data? Enter yes or no. - ')    
            if view_data != 'yes':    
                break    
            else:    
             if count % 5 == 0:    
                 data = int(input('enter \n1 for the first 5 rows \n2 for the first 10 rows \n3 for the first 15 rows e.t.c :'))    
                 data *= count    
                 print(df.iloc[(count -5) : (data)])    
        except ValueError:    
            print('input must be a number of either 1,2,3,4,5,6,...')    
        except KeyboardInterrupt:    
            print("\nNo input taken")    
            break
        except KeyError as e :
            print('an error occured {}'.format(e))

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['month'].value_counts().index[0]
    print()
    print('-----The most common month is-----')
    print(month)


    # display the most common day of week
    day_of_week = df['day_of_week'].value_counts().index[0]
    print()
    print('-----The most common day of the week is-----')
    print(day_of_week)


    # display the most common start hour
    hour_of_day = df['hour_of_day'].value_counts().index[0]
    print()
    print('-----The most common start hour is-----')
    print(hour_of_day)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print()
    print('-----Most used Start Station-----')
    print(f'\'{df["Start Station"].value_counts().index[0]}\'')


    # display most commonly used end station
    print()
    print('-----Most used End Station-----')
    print(f'\'{df["End Station"].value_counts().index[0]}\'')


    # display most frequent combination of start station and end station trip
    print('-----Most Frequent Route-----')

    df['Routes'] = df['Start Station'] + ' - ' + df['End Station']
    most_freq_route = df['Routes'].value_counts().index[0]

    print(f'Start station: {most_freq_route.split("-")[0].strip()}')
    print()
    print(f'End station: {most_freq_route.split("-")[1].strip()}')
    print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('-----Total travel time-----')
    print(f'{np.sum(df["Trip Duration"])}')


    # display mean travel time
    print()
    print('-----Mean Travel Time-----')
    print(f'{np.mean(df["Trip Duration"])}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # Display counts of user types
        print('-----User types-----')
        for index, val in zip(df['User Type'].value_counts().index, df['User Type'].value_counts()):
                print(index +  ": " + str(val))
    # Display counts of gender
        print("-----Gender count-----")
        for index, val in zip(df['Gender'].value_counts().index, df['Gender'].value_counts()):
                print(index +  ": " + str(val))

    # Display earliest, most recent, and most common year of birth
        year_list = df['Birth Year'].value_counts().index
        year_list = list(year_list)
        year_list = sorted(year_list)

        print('-----Earliest year of birth-----')
        print(int(year_list[0]))

        print('-----Most recent year of birth-----')
        print(int(year_list[-1]))

        print('-----Most common year of birth-----')
        print(int(df["Birth Year"].value_counts().index[0]))
    except Exception as e:
        print('An error occurred. %s column doesn\'t exist for this dataset' % (e))

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
