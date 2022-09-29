#Calls python files
from booking.booking import Booking

#Create object: Implement context managers
try:
    with Booking(teardown=True) as bot:
        bot.land_first_page()
        bot.change_currency(currency="USD")
        bot.select_place_to_go("Amsterdam")
        bot.select_date(check_in_date="2022-09-28", check_out_date="2022-10-03")
        bot.select_adults(2)
        bot.select_children(2)
        bot.select_rooms(2)
        bot.click_search()
        # bot.dismiss_sign_in()
        bot.apply_filtrations()
        # bot.refresh() # Gives a chance for the website to reorder the boxes correctly.
        bot.report_results()

# If the Chromedriver is not in PATH, you will get an error message.
# This exception handler provides instructions to deal with this potential issue.
except Exception as e:
    if "in Path" in str(e):
        print(
            "You are trying to run the bot from your command line. \n"
            "Please add the Selenium Drivers to your PATH. \n"
            "Windows: \n"
            "   set PATH=%PATH%;C:folder-path \n"
            "Linux: \n"
            "PATH=$PATH:/path/toyour/folder/ \n"

            )
    else:
        raise


# If teardown=True: Once code has finished running, the __exit__ method will run automatically.


