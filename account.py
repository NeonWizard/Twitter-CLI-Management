from twython import Twython, TwythonError, TwythonRateLimitError
import random
import time

class Account:
	def __init__(self, id, keys):
		self.API = Twython(**keys)
		self.screenName = self.API.verify_credentials()["screen_name"]
		self.id = id

		self.followedFile = open("hasfollowed.txt", 'r+')

		self.loadFollowed()											# The followed set includes people that have been followed OR are currently being followed
		self.isFollowed = set(self.API.get_friends_ids()["ids"])	# The isFollowed set ONLY includes people currently being followed
		self.followers = set(self.API.get_followers_ids()["ids"])	# People following this account

	# def dumpFollowed(self):
	# 	print("Dumping followed... ", end="")
	# 	with open("hasfollowed.txt", 'w') as openFile:
	# 		for ID in self.followed:
	# 			openFile.write(str(ID) + "\n")
	# 	print("done.")

	def writeFollowed(self, ID):
		self.followedFile.write(str(ID) + "\n")

	def loadFollowed(self):
		self.followed = set()

		print("Loading followed... ", end="")
		for line in self.followedFile:
			line = line.rstrip("\n")
			self.followed.add(int(line))
		print("done.")

	def follow(self, ID):
		try:
			toFollow = self.API.show_user(user_id=ID)
			self.API.create_friendship(user_id=ID)

			if toFollow["protected"]:
				print("Sent a follow request to \033[93m{}\033[0m!".format(ID))
			else:
				print("Followed \033[92m{}\033[0m!".format(ID))

			self.followed.add(ID)
			self.writeFollowed(ID)

			return True
		except TwythonError as e:
			print(e)
			# This is mostly just for users I've already requested to follow but haven't accepted yet
			if isinstance(e, TwythonRateLimitError):
				raise TwythonRateLimitError
			elif "already requested" in str(e) or "blocked" in str(e):
				self.followed.add(ID)
				self.writeFollowed(ID)
			return False

	def followAllOf(self, target_id, amount=1000):
		amount = min(amount, 1000)
		count = 0
		for friend_id in self.API.get_followers_ids(user_id=target_id)["ids"]:
			if friend_id == self.id: 		continue	# dat me
			if friend_id in self.followed: 	continue 	# already followed/following

			# Create friendship
			if not self.follow(friend_id):
				# Couldn't add them >:y
				continue

			# Make a tiny bit of a delay so it doesn't flood the Twitter servers
			time.sleep(random.randrange(1, 6) / 10.0)

			# Keep count so we can break once we follow [amount] users
			count += 1
			if count >= amount:
				break

	def unfollowNonFollowers(self):
		unfollowed = set()
		for followed_id in self.isFollowed:
			if followed_id not in self.followers:
				self.API.destroy_friendship(user_id=followed_id)
				unfollowed.add(followed_id)
				print("Unfollowed {} cuz he/she wasn't following me back >:c".format(followed_id))
				break

		self.isFollowed = self.isFollowed - unfollowed

	def followBackAll(self):
		for follower_id in self.followers:
			if follower_id not in self.isFollowed:
				self.follow(follower_id)


def main():
	spooky = Account(id=850089475128438784, keys={
		"app_key": "***REMOVED***",
		"app_secret": "***REMOVED***",
		"oauth_token": "***REMOVED***",
		"oauth_token_secret": "***REMOVED***"
	})

	spooky.followAllOf(target_id=2432753774, amount=2)	# Follow a few of Telepathics' followers
	spooky.followBackAll()
	# spooky.unfollowNonFollowers()

if __name__ == "__main__":
	main()
