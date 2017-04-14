from twython import Twython, TwythonError
import random
import time

class Account:
	def __init__(self, id):
		self.API = Twython("***REMOVED***", "***REMOVED***", "***REMOVED***", "***REMOVED***")
		self.id = id

		self.hasFollowed = set()									# People that HAVE been followed by this account but aren't currently
		self.isFollowed = set(self.API.get_friends_ids()["ids"])	# People that ARE being followed by this account currently

		self.followers = set(self.API.get_followers_ids()["ids"])	# People following this account

	def dumpHasFollowed(self):
		print("Dumping hasFollowed... ", end="")
		with open("hasfollowed.txt", 'w') as openFile:
			for ID in self.hasFollowed:
				openFile.write(str(ID) + "\n")
		print("done.")

	def loadHasFollowed(self):
		print("Loading hasFollowed... ", end="")
		with open("hasfollowed.txt", 'r') as openFile:
			for line in openFile:
				line = line.rstrip("\n")
				self.hasFollowed.add(int(line))
		print("done.")

	def updateFollowers(self):
		self.followers = self.API.get_followers_ids()["ids"]

	def followAllOf(self, target_id, amount=1000):
		amount = min(amount, 1000)
		count = 0
		for friend_id in self.API.get_followers_ids(user_id=target_id)["ids"]:
			if friend_id == self.id: 			continue	# dat me
			if friend_id in self.isFollowed: 	continue 	# already following :0
			if friend_id in self.hasFollowed: 	continue	# already followed but no follow back :< 

			# Create friendship
			try:
				self.API.create_friendship(user_id=friend_id)
				print("Added friend {}!".format(friend_id))
				self.isFollowed.append(friend_id)
			except TwythonError:
				# This is mostly just for users I've already requested to follow but haven't accepted yet
				continue

			# Make a tiny bit of a delay so it doesn't flood the Twitter servers
			time.sleep(random.randrange(1, 6) / 10.0)

			# Keep count so we can break once we follow [amount] users
			count += 1
			if count >= amount:
				break

	def unfollowNonFollowers(self):
		tmp = set()
		for followed_id in self.isFollowed:
			if followed_id not in self.followers:
				self.API.destroy_friendship(user_id=followed_id)
				tmp.add(followed_id)
				self.hasFollowed.add(followed_id)
				print("Unfollowed {} cuz he/she wasn't following me back >:c".format(user_id))
				break

		self.isFollowed = self.isFollowed - tmp

	def followBackAll(self):
		for follower_id in self.followers:
			if follower_id not in self.isFollowed:
				try:
					self.API.create_friendship(user_id=follower_id)
					print("Followed back {}!".format(follower_id))
				except TwythonError:
					continue


def main():
	spooky = Account(id=850089475128438784)

	spooky.loadHasFollowed()

	# spooky.followAllOf(target_id=2432753774, amount=2)	# Follow a few of Telepathic's followers
	# spooky.followBackAll()
	spooky.unfollowNonFollowers()

	spooky.dumpHasFollowed()

if __name__ == "__main__":
	main()
