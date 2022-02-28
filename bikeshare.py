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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #Three while loops below to handle each of the inputs. They will 'break' the loop once the user entered prompt meets the condition
    #input() prompts user input
    #the user input is converted to suit the required formats in each list per the practice examples in the course -
    #e.g. .lower coverts user input to lowercase and .title to Tile Case
    while True:
        cities= ['chicago','new york city','washington']
        city= input('\n Please type the city would you like to analyse.\n Choose from Chicago, New York City, or Washington.\n').lower()
        if city in cities:
            break
        else:
            print("\nPlease enter a valid city name (Chicago, New York City, or Washington)")

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        months= ['January','February','March','April','May','June','All']
        month = input("\n Which month would you like to analyse? \n Choose from January, February, March, April, May, June, or type 'All' for no month filter.\n").title()
        if month in months:
            break
        else:
            print("\n Please enter a valid month from the list")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']
        day= input("\n Which day of the week would you like to analyse?'\n Choose from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. Type 'All' for no day filter \n").title()
        if day in days:
            break
        else:
            print("\n Please enter a valid day from the list")

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name #dt.weekday_name in the practice file
    #I had an error using weekday_name (DatetimeProperties' object has no attribute 'weekday_name) in my desktop version

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1


    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    """Note: If a particular month has been selected by the user, then this will be the mode"""
    months = ['January','February','March','April','May','June','All' ]
    common_month= df['month'].mode()[0]
    common_month= months[common_month-1]
    print("The most common month is",common_month)

    # TO DO: display the most common day of week
    """Note: If a particular day has been selected by the user, then this will be the mode"""
    common_day= df['day_of_week'].mode()[0]
    print("The most common day of the week is",common_day)

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['StartHour'] = df['Start Time'].dt.hour
    common_hour  = df['StartHour'].mode()[0]
    print('The most common start hour is {}:00'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mostused_start_stn= df['Start Station'].mode()[0]
    print("The most commonly used Start Station is {}".format(mostused_start_stn))

    # TO DO: display most commonly used end station
    mostused_end_stn= df['End Station'].mode()[0]
    print("The most commonly used End Station is {}".format(mostused_end_stn))

    # TO DO: display most frequent combination of start station and end station trip
    mostused_combo_stns = (df['Start Station']+' to '+df['End Station']).mode()[0]
    print("The most frequent combination of start station and end station is {}".format(mostused_combo_stns).split("||"))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration=df['Trip Duration'].sum()
    #manually calculate, and use divmod to split the quotient to a tuple
    minute,second=divmod(total_duration,60)
    hour,minute=divmod(minute,60)
    print("The total trip duration: {}hour(s){}minute(s) {}second(s))".format(hour, minute, second))

    # TO DO: display mean travel time
    mean_duration=df['Trip Duration'].mean()
    minute,second=divmod(mean_duration,60)
    hour,minute=divmod(minute,60)

    print("The average trip duration: {} hour(s){} minute(s) {} second(s))".format(hour, minute, second))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count= df['User Type'].value_counts()
    print("The User Types are:\n",user_type_count)


    # TO DO: Display counts of gender
    #Gender key element does not exist for the Washington file
    try:
        gender_counts= df['Gender'].value_counts()
        print("\nThe count of each gender category are:\n",gender_counts)
    except:
        print("\nThere is no gender category available for your selected city")

    # TO DO: Display earliest, most recent, and most common year of birth
    #year of birth also does not exist for the Washington file
    #use try to 'try' to make calculations and if it will fail over to except (print exception) where data doesn't exist.
    try:
        earliest= int(df['Birth Year'].min())
        print("\nThe oldest user was born in ",earliest)
        recent= int(df['Birth Year'].max())
        print("\nThe youngest user was born in ",recent)
        common_birthyear= int(df['Birth Year'].mode()[0])
        print("\nThe most common birth year is",common_birthyear)
    except:
        print("\nThere is no birth year data available for your selected city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #TO DO Your script should prompt the user if they want to see 5 lines of raw data
def show_raw_data(df):
    """Displays raw data 5 rows at a time iteratively."""
    """The first loop will just get the first 5 rows using head() which defaults to 5. This saves 3 lines of syntax for the first iteration"""
    """The second loop will then start from the row location and get the next iteration(s)"""

    #using another while true loop
    start=0
    end=5
    while True:
        rawdata_options= ['y','n']
        rawdata_prompt= input("\n Would you like to see five lines of data?\n Type 'Y' for yes or 'N' for no.\n").lower()
        if rawdata_prompt in rawdata_options:
            if rawdata_prompt == 'y':
                print (df.head())
            break
        else:
            print("\nPlease enter a valid response: Y or N ")
    if rawdata_prompt=='y':
            while True:
                more_rawdata_prompt= input("Would you like to view five more lines of data? Type 'Y' for yes or 'N' for no.\n").lower()
                if more_rawdata_prompt in rawdata_options:
                    if more_rawdata_prompt=='y':
                        start+=5
                        end+=5
                        rawdata = df.iloc[start:end]
                        print(rawdata)
                    else:
                        break
                else:
                    print("Please enter a valid response: Y or N ")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)
        #I changed this as any other entry other than yes breaks it, so accidently entering y instead of yes will break
        restart = input("\nWould you like to restart? Type 'Y' for yes or 'N' for no.\n")
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
