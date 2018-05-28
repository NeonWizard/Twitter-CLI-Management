from twython import Twython, TwythonError, TwythonRateLimitError
from boto.s3.connection import S3Connection

import random
import time

class Account:
	def __init__(self, id, twitter_keys, aws_keys):
		self.TWAPI = Twython(**twitter_keys)
		self.S3API = S3Connection(aws_keys['key'], aws_keys['secret_key'])

		self.screenName = self.TWAPI.verify_credentials()["screen_name"]
		self.id = id

		# self.followedFile = open("hasfollowed.txt", 'r+')
		self.followedS3File = self.S3API.get_bucket("wespooky-getfollowers").get_key("hasfollowed.txt")

		self.loadFollowed()											# The followed set includes people that have been followed OR are currently being followed
		self.isFollowed = set(self.TWAPI.get_friends_ids()["ids"])	# The isFollowed set ONLY includes people currently being followed
		self.followers = set(self.TWAPI.get_followers_ids()["ids"])	# People following this account
		self.followCount = 0

	def dumpFollowed(self):
		print("Dumping followed... ", end="")
		self.followedS3File.set_contents_from_string(
			"\n".join(["{}:{}".format(*followed) for followed in self.followedE])
		)
		print("done.")

	def triggerDump(self, force=False):
		if (force and self.followCount > 0) or self.followCount == 10:
			self.dumpFollowed()
			self.followCount = 0

	# def writeFollowed(self, ID):
		# self.followedFile.write(str(ID) + "\n")

	def loadFollowed(self):
		self.followed = set()
		self.followedE = []

		print("Loading followed... ", end="")
		raw = self.followedS3File.get_contents_as_string().decode().split("\n")
		for line in raw:
			if not line: continue
			line = line.rstrip("\n").split(":")

			self.followed.add(int(line[0]))
			self.followedE.append((int(line[0]), int(line[1])))

		print("done.")

	def addFollowed(self, ID):
		self.followed.add(int(ID))
		self.followedE.append((int(ID), int(time.time())))

	def follow(self, ID):
		self.followCount += 1
		try:
			toFollow = self.TWAPI.show_user(user_id=ID)
			self.TWAPI.create_friendship(user_id=ID)

			if toFollow["protected"]:
				print("Sent a follow request to \033[93m{}\033[0m!".format(ID))
			else:
				print("Followed \033[92m{}\033[0m!".format(ID))

			self.addFollowed(ID)

			# self.writeFollowed(ID)
			self.triggerDump()

			return True
		except TwythonError as e:
			print(e)
			# This is mostly just for users I've already requested to follow but haven't accepted yet
			if isinstance(e, TwythonRateLimitError):
				raise TwythonRateLimitError
			elif "already requested" in str(e) or "blocked" in str(e):
				self.addFollowed(ID)

				# self.writeFollowed(ID)
				self.triggerDump()

			return False

	# Follows [amount] followers of [target_id]'s account
	def followAllOf(self, target_id, amount=1000):
		amount = min(amount, 1000)
		count = 0
		for friend_id in self.TWAPI.get_followers_ids(user_id=target_id)["ids"]:
			if friend_id == self.id: 		continue	# dat me
			if friend_id in self.followed: 	continue 	# already followed/following

			# Create friendship
			if not self.follow(friend_id):
				# Couldn't add them >:y
				continue

			# Make a tiny bit of a delay so it doesn't flood the Twitter servers
			time.sleep(random.randrange(1, 4) * 2)

			# Keep count so we can break once we follow [amount] users
			count += 1
			if count >= amount:
				break

	# Unfollows anyone that isn't following the account
	def unfollowNonFollowers(self):
		unfollowed = set()
		for followed_id in self.isFollowed:
			if followed_id not in self.followers:
				self.TWAPI.destroy_friendship(user_id=followed_id)
				unfollowed.add(followed_id)
				print("Unfollowed {} cuz he/she wasn't following me back >:c".format(followed_id))
				break

		self.isFollowed = self.isFollowed - unfollowed

	# Follow back everyone that is following me
	def followBackAll(self):
		for follower_id in self.followers:
			if follower_id in self.followed: continue

			if follower_id not in self.isFollowed:
				self.follow(follower_id)

	# Unfollow [amount] people I've followed who aren't following me - in chronological order
	def unfollowFollowedChronologicalNonFollowers(self, amount): # what a mouthful
		pass
