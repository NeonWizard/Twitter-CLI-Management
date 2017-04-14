from account import Account

def main():
	acc = Account(id=int(input("Please enter your Twitter ID: ")))
	print("Hello @{}!".format(acc.screenName))

	looping = True
	while looping:
		print()
		print("What would you like to do?")
		print()
		print("1 - Follow back all followers.")
		print("2 - Follow [x] of [target]'s followers.")
		print("3 - Unfollow everyone who doesn't follow you.")
		print("4 - Exit.")
		print()
		option = int(input("> "))
		if option == 1:
			acc.followBackAll()
		elif option == 2:
			print("WIP")
		elif option == 3:
			acc.unfollowNonFollowers()
		elif option == 4:
			looping = False
		else:
			print("Invalid option.")

main()
