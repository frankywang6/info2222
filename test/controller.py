'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''

from bottle import route, get, post, error, request, static_file, redirect


import model

#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------
curr_user = None
# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

#-----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')

#-----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------

# Redirect to login
@get('/')
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()

#-----------------------------------------------------------------------------

# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    return model.login_form()

#-----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    global curr_user
    curr_user = username
    # Call the appropriate method
    return model.login_check(username, password)



#-----------------------------------------------------------------------------

@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()
#-----------------------------------------------------------------------------
@get('/chat')
def get_chat():
    '''
        get_chat
        
        Serves the chat page
    '''
    #update the friends list
    
    return model.chat(curr_user)


@post('/chat')
def add_friend_controller():
    '''
        add_friend_controller
        
        Handles adding friends
        Expects a form containing 'friend' field
    '''
    

    friend = request.forms.get('friend')

    model.add_friend(curr_user, friend)
    #print the friends list
    # friends = model.get_friends(curr_user)

    return redirect('/chat')


@get('/register')
def get_register():
    '''
        get_register
        Serves the registration page
    '''
    return model.register_form()  # change this line

@post('/register')
def register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    model.register_user(username, password)

    user = model.get_user(username)
    if user:
        print(f"User {username} has been successfully registered!")
    else:
        print(f"User registration failed for {username}!")

    return redirect('/login')


# Help with debugging
@post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)

#-----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@error(404)
def error(error): 
    return model.handle_errors(error)


