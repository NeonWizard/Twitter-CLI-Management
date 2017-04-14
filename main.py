from twython import Twython, TwythonError
import time

twitter = Twython("U8NXVVgoLFmCINZqMiE7Fhi9G", "27sx2V6j2FSIW2kMpDu6OrEe1NfhRYbbUXmVMWRlAMErJR1jWD", "850089475128438784-k1JMEgPaTaIyTrE1hpQwyJraXWQVWLw", "8wZNArpbRHcyHHGziYSJxYYfPOMdcUrKCcZPMpXXVfX2O")

myFollows = twitter.get_friends_ids()["ids"]

def updateFollowed():
	pass

def writeFollowed():
	pass

def followAllOfTelepathics(amount=1000):
	amount = min(1000, amount)
	count = 0
	for friend_id in twitter.get_followers_ids(user_id=2432753774)["ids"]:
		if friend_id == 850089475128438784: continue # dat me
		if friend_id in myFollows: continue # already following :0

		# Create friendship
		try:
			twitter.create_friendship(user_id=friend_id)
			print("Added friend {}".format(friend_id))
			myFollows.append(friend_id)
		except TwythonError:
			# This is mostly just for users I've already requested to follow but haven't accepted yet
			continue

		# Make a tiny bit of a delay so it doesn't flood the Twitter servers
		time.sleep(0.1)

		# Keep count so we can break once we follow [amount] users
		count += 1
		if count >= amount:
			break

def unfollowNonFollowers():
	myFollowers = twitter.get_followers_ids()["ids"]

	for followed_id in myFollows:
		if followed_id not in myFollowers:
			twitter.destroy_friendship(user_id=followed_id)
			print("Unfollowed {} cuz he/she wasn't following me back >:c".format(user_id))

def followBackAll():
	myFollowers = twitter.get_followers_ids()["ids"]

	for follower_id in myFollowers:
		if follower_id not in myFollows:
			try:
				twitter.create_friendship(user_id=follower_id)
				print("Followed back {}!".format(follower_id))
			except TwythonError:
				continue
