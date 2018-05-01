import os
from account import Account

def promptUserAuth():
	ID = int(input("Please enter your Twitter ID: "))
	
	keys = {
		"app_key": os.environ["TWITTER_API_KEY"] if "TWITTER_API_KEY" in os.environ else input("Please enter your app key: "),
		"app_secret": os.environ["TWITTER_API_SECRET"] if "TWITTER_API_SECRET" in os.environ else input("Please enter your app secret: "),
		"oauth_token": os.environ["TWITTER_TOKEN"] if "TWITTER_TOKEN" in os.environ else input("Please enter your oauth token: "),
		"oauth_token_secret": os.environ["TWITTER_TOKEN_SECRET"] if "TWITTER_TOKEN_SECRET" in os.environ else input("Please enter your oauth token secret: ")
	}

	return ID, keys

def main():
	ID, keys = promptUserAuth()
	acc = Account(id=ID, keys=keys)

	print("Hello @{}!".format(acc.screenName))

	print("\n" * 50)
	looping = True
	while looping:
		print(chr(27) + "[2J")
		print("==================================")
		print("    \033[1mWhat would you like to do?\033[0m")
		print("==================================")
		print()
		print("\033[93m1\033[0m - Follow back all followers.")
		print("\033[93m2\033[0m - Follow [x] of [target]'s followers.")
		print("\033[93m3\033[0m - Unfollow everyone who doesn't follow you.")
		print("\033[93m4\033[0m - Exit.")
		print()
		option = int(input("> "))
		if option == 1:
			acc.followBackAll()
		elif option == 2:
			print()
			print(chr(27) + "[2J")
			ID = int(input("Enter target account's ID: "))
			amount = int(input("Enter amount to follow: "))
			print()
			acc.followAllOf(ID, amount)
		elif option == 3:
			acc.unfollowNonFollowers()
		elif option == 4:
			looping = False
		else:
			print("Invalid option.")

main()
