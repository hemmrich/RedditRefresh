import praw #python reddit api wrapper
import getpass #to get password from command line
import time #for sleep


user_agent = ("Script that migrates reddit subscriptions to new account"
              "by /u/MJHdev")

if __name__ == '__main__':
   
   reddit = praw.Reddit(user_agent = user_agent)
   username = raw_input('>> Enter your old account\'s username: ')
   password = getpass.getpass('>> Enter your old account\'s password: ')
   print 'Logging in to old account...'
   try:
      reddit.login(username = username, password = password)
   except:
      print 'Error logging in. Exiting.'
      exit()

   oldReddits = reddit.get_my_subreddits(limit = None)

   needAccount = False
   while True:
      yn = raw_input('>> Have you already made a new account? (Y/N): ')
      if yn.lower() == 'y':
         new_name = raw_input('>> Enter your new account\'s username: ')
         new_password = getpass.getpass('>> Enter your new account\'s password: ')
         break
      elif yn.lower() == 'n':
         needAccount = True
         break
      else:
         continue

   accountMade = False
   if needAccount:
      while not accountMade:
         new_name = raw_input('>> Enter your desired new username: ')
         if reddit.is_username_available(new_name):
            print 'Desired name ' + new_name + ' is available.'

            while True:
               new_password = getpass.getpass('>> Enter your desired new password: ')
               new_password2 = getpass.getpass('>> Verify password: ')

               if new_password.lower() == new_password2.lower():
                  print 'Passwords matched.'
                  email = raw_input('>> Enter your email address (can leave blank): ')
                  print 'Creating account now...'
                  reddit.create_redditor(user_name = new_name, password = new_password, email = email, captcha = None)
                  accountMade = True
                  print 'Account made.'

               else:
                  'Passwords do not match. Try again.'
         else:
            print 'Account name already taken. Try again.'

   
   # Login to new account
   print 'Logging in to new account...'
   try:
      reddit = praw.Reddit(user_agent = user_agent)
      reddit.login(username = new_name, password = new_password)
      newReddits = reddit.get_my_subreddits(limit = None) # to reduce number of API calls below
   except:
      print 'Error logging in. Exiting.'
      exit()
   print 'Done.'
   print 'Adding subscriptions to new account.'

   # Add subscribtions in new account
   for subreddit in oldReddits:
      if subreddit not in newReddits:
         print 'Subscribing to r/' + subreddit.display_name
         reddit.subscribe(subreddit = subreddit, unsubscribe = False)
      else:
         print 'Already subscribed to r/' + subreddit.display_name
   print ''
   




























   



