#TO DO 

/login
#User enters username stored in database with correct password 
    #Redirects to /newpost page 
    #Username stored in a session
User enters username stored in database with incorrect password
    Error message for invalid password
    ***DO ERROR NOT FLASH**
User enters username not in database
    Redirects to login with error message
#User doesn't have account, clicks "Create Account"
    #Redirects to '/signup'

/signup
#User enters new(valid) username and (valid) password
    #Verifies correctly 
    #Redirects to '/newpost' page
    #Username stored in a session
#Error message for leaving fields blank
#Error message if username already exists
#Error message for non-matching passwords
#Error message for password/user less than 3char
#Redirect to '/login' if not logged in (username not in session)
    #Allowed routes: 'login', '/blog', 'index', 'signup'
#After valid new post while logged in, redirect to page featuring that single_post
#'/blog' shows list of all entries by all users
    #Click on entry, redirect to single_post page showing just that entry
Logout redirects to '/blog' 
    #'/newpost' redirects to '/login'
#Create page to dynamically display posts of each individual user
    #Written with 'userid' with hyperlink to 'blog?user=userid'
#User on '/', clicks on author's username in list and lands on that user's page
#User on '/blog', clicks on author's username in tagline and lands on that user's page
#User on single_post page, clicks on author's username in tagline and lands on that user's page

Bonus
Paginate 5 blogs per page
Add Hashing

Lucas Recommendations
Add CSS & Bootstrap
Use bootstrap on navbar and div separation
Hide "new post" and "logout" if not logged in
Add 'Blog has been posted' success banner when applicable
Add Edit/Remove button to user ONLY FOR THEIR BLOGS



#TODO!!!!!
Not getting blank body error on Add New Post