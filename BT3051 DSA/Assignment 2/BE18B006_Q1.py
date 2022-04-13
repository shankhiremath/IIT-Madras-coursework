# Add library imports here
# Only datetime library is allowed.
from datetime import datetime, timedelta

class PersonalWorldClock():
    """
    The class should be able to convert time to and from the 
    home time zone and away time zone.

    For the example provided in q1_test.txt. The time zones considered are:
    - Home: IST
    - Away: Pheonix, Arizona, USA

    Explaination:
    The away time is 12:30 hours ahead of IST.
    So essentially, 12:30 in IST will be 00:00 in Pheonix.
                    12:00 in Pheonix will be 00:30 in IST (The next day)

    Example:
    For the given q1_test.txt, the output we expect to get when we run the code:
    PersonalWorldClock Converter:
    Home: UTC+05:30; Away: UTC-07:00
    ----------------------------------------
    Converting Away time to Home time
    Given Away Time: 08/09/21 16:30
    Home time: 09/09/21 05:00
    ----------------------------------------
    Converting Home time to Away time
    Given Home Time: 08/09/21 15:30
    Away time: 08/09/21 03:00
    """

    def __init__(self, away_time_zone, home_time_zone="+05:30"):
        """
        Initialize the variables.
        Note that the away time zone will be passed as a string
        """
        self.hometz = home_time_zone
        self.awaytz = away_time_zone

    def timezonetodelta(self, timezone):
        tz_sign = timezone[0]
        tz_hour = int(timezone[1:3])
        tz_minute = int(timezone[4:6])
        if tz_sign == '+':
            return timedelta(hours = tz_hour, minutes = tz_minute)
        if tz_sign == '-':
            return timedelta(hours = - tz_hour, minutes = - tz_minute)

    def convert_to_home(self, time_to_be_converted):
        """
        Inputs:
        - time_to_be_converted: of type str.
          Example: "08/09/21 16:30"

        Outputs:
        - Should return a string in the 
        same format as the input
        """
        timedt = datetime.strptime(time_to_be_converted, "%d/%m/%y %H:%M")
        homeoffset = self.timezonetodelta(self.hometz)
        awayoffset = self.timezonetodelta(self.awaytz)
        hometime = timedt + homeoffset - awayoffset
        return hometime.strftime("%d/%m/%y %H:%M")

    def convert_to_away(self, time_to_be_converted):
        """
        Inputs:
        - time_to_be_converted: of type str.
          Example: "08/09/21 16:30"

        Outputs:
        - Should return a string in the 
        same format as the input
        """
        timedt = datetime.strptime(time_to_be_converted, "%d/%m/%y %H:%M")
        homeoffset = self.timezonetodelta(self.hometz)
        awayoffset = self.timezonetodelta(self.awaytz)
        awaytime = timedt - homeoffset + awayoffset
        return awaytime.strftime("%d/%m/%y %H:%M")

    # You can add any additional function that you might need.

if __name__ == "__main__":
    ################################################
    # Don't change anything below this.
    ################################################

    fin = open("q1_test.txt")
    data = fin.read().split("\n")
    fin.close()

    away_time_zone = data[0]
    home_time_zone = data[1]
    given_away_time = data[2]
    given_home_time = data[3]

    time_converter = PersonalWorldClock(away_time_zone=away_time_zone, home_time_zone=home_time_zone)

    # Check time conversion - given away time convert to home time
    op_home_time = time_converter.convert_to_home(given_away_time)

    # Check time conversion - given home time convert to away time
    op_away_time = time_converter.convert_to_away(given_home_time)

    # Print and check
    print("PersonalWorldClock Converter:\nHome: UTC", home_time_zone, "; Away: UTC", away_time_zone, sep="")
    print("-"*40)
    print("Converting Away time to Home time")
    print("Given Away Time:", given_away_time)
    print("Home time:", op_home_time)
    print("-"*40)
    print("Converting Home time to Away time")
    print("Given Home Time:", given_home_time)
    print("Away time:", op_away_time)
