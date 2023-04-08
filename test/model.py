'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
from no_sql_db import database

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

#-----------------------------------------------------------------------------
# Add a new route to serve the chat page

def chat(user):
    '''
        chat
        Returns the view for the chat page
    '''
    # Get the user's friend list from database
    friends = get_friends(user)
    # Get the user's username from the cookie
    return page_view("chat",name=user, friend=friends)


# Add friend to user's friend list in database
def add_friend(username, friend):
    '''
        add_friend
        Adds a friend to the user's friend list

        :: username :: The username
        :: friend :: The friend to add
    '''
    user = database.search_table('users', 'username', username)
    friend_search = database.search_table('users', 'username', friend)
    if user and friend_search:
        #if user[3] do not exist friend, append friend to user[3]
        if friend_search[1] not in user[3]:
            user[3].append(friend_search[1])
        if user[1] not in friend_search[3]:
            friend_search[3].append(user[1])
    return


# Get user's friend list from database
def get_friends(username):
    '''
        get_friends
        Gets the user's friend list

        :: username :: The username

        Returns a list of friends
    '''
    friends = None
    #get the friends from the database
    user = database.search_table('users', 'username', username)
    if user:
        #list out the friends from user[3] one by one
        for friend in user[3]:
            #if friends is not empty, append the friend to friends
            if friends:
                friends = friends + "," + friend
            else:
                friends = friend
    return friends
    
# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    users = database.search_table('users', 'username', username)
    if users:
        if users[2] == password:
            
            return page_view("valid", name=username)
        
        else:
            return page_view("invalid")
    else:
        return page_view("invalid")


#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())

def register_user(username, password):
    # Check if the username already exists
    if database.search_table('users', 'username', username):
        return page_view("register", error="Username already exists")

    # If not, add the new user to the database
    database.create_table_entry('users', [None, username, password, []])

    # Redirect the user to the login page with a success message
    return page_view("login", message="Registration successful. Please log in.")


def register_form():
    '''
        register_form
        Returns the view for the registration form
    '''
    return page_view("register")
def get_user(username):
    user = database.get_user('users', username)
    return user



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)