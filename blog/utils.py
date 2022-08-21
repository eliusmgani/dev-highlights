import cv2
import os
import json
import requests

from PIL import Image
from io import BytesIO
from decouple import config

from . models import BlogPost
from account.models import Account



def is_image_aspect_ratio_valid(img_url):
	img = cv2.imread(img_url)
	dimensions = tuple(img.shape[1::-1]) # gives: (width, height)
	# print("dimensions: " + str(dimensions))
	aspect_ratio = dimensions[0] / dimensions[1] # divide w / h
	# print("aspect_ratio: " + str(aspect_ratio))
	if aspect_ratio < 1:
		return False
	return True


def is_image_size_valid(img_url, mb_limit):
	image_size = os.path.getsize(img_url)
	# print("image size: " + str(image_size))
	if image_size > mb_limit:
		return False
	return True


def get_scheduled_posts():
	print("running cron job")

	results = make_request()
	
	if not results:
		print("no results")
		return False

	for post in results[:5]:
		if not post.get("summary") or not post.get("title") or not post.get("media"):
			continue

		status = create_blog_post(post)
	
	return True


def make_request():

	url = "https://newscatcher.p.rapidapi.com/v1/latest_headlines"

	querystring = {"topic": "tech", "lang":"en","media":"True"}

	headers = {
		"X-RapidAPI-Key": config("API_KEY"),
		"X-RapidAPI-Host": config("API_HOST"),
	}
	
	try:
		response = requests.request("GET", url, headers=headers, params=querystring)

		if response.status_code == 200:
			results = json.loads(response.text)
			return results.get("articles")
	
	except Exception as e:
		print("error: " + str(e))
		return False


def create_blog_post(obj):

	if obj.get("author"):
		user = create_user_account(obj.get("author"))
	else:
		user = "eliasmgani@gmail.com"

	if not BlogPost.objects.filter(title=obj.get("title")).exists():
		try:
			img_name = obj.get("title")[:10]

			r = requests.get(obj.get("media"))
			img = Image.open(BytesIO(r.content))
			img.save("media_cdn/" + img_name.lower() + ".png")

			BlogPost.objects.create(
				title=obj.get("title"),
				body=obj.get("summary"),
				image=img_name.lower() + ".png",
				author=user,
				date_published=obj.get("published_date"),
			)

			return True

		except Exception as e:
			print("error: " + str(e))
					

def create_user_account(name):

	if name.count(" ") == 0:
		user_name = name
	else:
		user_name = name.split(" ")[0] + name.split(" ")[1]

	email = user_name.lower() + "@dev.com"
	if Account.objects.filter(email=email).exists():
		return Account.objects.get(email=email)

	return Account.objects.create_user(
		email=email,
		username=name,
		password="123"

	)
