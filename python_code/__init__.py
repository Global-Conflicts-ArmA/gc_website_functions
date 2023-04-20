
from pymongo import MongoClient
from .threading_utils import call_slow_function, has_call_finished, get_call_value
from datetime import datetime
import logging
import os
from .env import mongo_host_uri, debug
import requests as requests
from bson import ObjectId


logger = logging.getLogger(__name__)


logger.debug("mongo host:::: %s", mongo_host_uri)

client = MongoClient(mongo_host_uri)
db = client.prod


def submit_review(my, arguments):
    return ["submit_review", 42, True, (1, 2)]


def submit_bug_report(my, arguments):
    return ["submit_bug_report", 42, True, (1, 2)]


def submit_rating(my, arguments):
    return ["submit_rating", 42, True, (1, 2)]


def validate_user(steam_id):
    user = db.get_collection("users").find_one(
        {"steam.steam_id": steam_id})

    if not user:
        return {
            "error": "Steam account not linked. Go to your profile page on the website and link it to use this feature."}

    try:
        is_blacklisted = user['blacklist']['website']
        if is_blacklisted:
            return {"error": "You are blacklisted from interactions with the website."}
    except KeyError:
        pass
    return {"user": user, "error": None}


def submit_review(message, steam_id, mission_name):

    if debug:
        steam_id = "76561198000360814"
        mission_name = "co23_testmiss_v2.mapn_ame"

    validation_result = validate_user(steam_id)

    if validation_result["error"]:
        return validation_result["error"]

    user = validation_result["user"]

    name_start = mission_name.find("_")
    name_end = mission_name.rfind(".")
    unique_name_with_version = mission_name[name_start + 1:name_end]
    version = unique_name_with_version[unique_name_with_version.rfind(
        "_") + 1:]
    name_end = unique_name_with_version.rfind("_")

    unique_name = unique_name_with_version[:name_end]

    review = {
        "_id": ObjectId(),
        "version": version,
        "authorID": user["discord_id"],
        "date": datetime.now(),
        "text": message.strip(),
    }

    mission = db.get_collection("missions").find_one_and_update(
        {
            "uniqueName": unique_name,
        },
        {
            "$addToSet": {"reviews": review},
        }, projection={"name": 1, "authorID": 1}
    )

    if not mission:
        logger.critical("Mission not found or review insertion failed. %s", str({
            "query": {
                "uniqueName": unique_name,
            },
            "update": {
                "$addToSet": {"reviews": review},
            }
        }))
        return "Failed submiting review."

    discord_user = get_discord_user(user["discord_id"])

    review_data = {
        "name": mission["name"],
        "uniqueName": unique_name,
        "review": message.strip(),
        "reviewAuthor": discord_user["nickname"] or discord_user["displayName"],
        "reviewDisplayAvatarURL": discord_user["displayAvatarURL"],
        "authorId": mission["authorID"],
    }

    try:
        send_review_to_bot(review_data)
    except Exception:
        return "Review Submited, but failed sending it to the bot."

    return "Review submited!"


def call_submit_review(message, steam_id, mission_name):
    return call_slow_function(submit_review, (message, steam_id, mission_name))


def send_review_to_bot(review_data):

    req = requests.post(
        "http://localhost:3001/missions/review", data=review_data)

    if req.status_code != 201:
        logger.warn("Failed sending it to the bot. %s", str(req))
        raise "Error sending review to bot."
    else:

        return "ok"


def get_discord_user(discord_id):

    req = requests.get(
        f'http://localhost:3001/users/{discord_id}')
    if req.status_code != 200:
        raise "Error sending retrieving Discord user."
    else:
        return req.json()


has_call_finished  # noqa - this function has been imported from threading_utils.py
get_call_value  # noqa - this function has been imported from threading_utils.py
