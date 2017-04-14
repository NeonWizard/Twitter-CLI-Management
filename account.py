from twython import Twython, TwythonError

class Account:
	def __init__(self, id):
		self.API = Twython("***REMOVED***", "***REMOVED***", "***REMOVED***", "***REMOVED***")
		self.id = id

		self.hasFollowed = []	# People that HAVE been followed by this account but aren't currently
		self.isFollowed = []	# People that ARE being followed by this account currently

		self.followers = []		# People following this account

	def followAllOf(target_id, amount=1000):
		amount = min(amount, 1000)
		count = 0
		for friend_id in twitter.get_followers_ids(user_id=target_id)["ids"]:
			if friend_id == self.id: continue # dat me
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