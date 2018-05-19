"""
AnnounceDir main module.
Run it to check.
Settings are at settings.py
Using github3.py and requests
"""

from __future__ import print_function
from base64 import b64decode
import datetime
import re
import requests
import github3
from bs4 import BeautifulSoup
from settings import USERNAME, PASSWORD, REPOSITORY

FORUM = "https://scratch.mit.edu/discuss/5/"

REMOVE_BLANK_LINES = re.compile("\n{2,}")

def categorize(title):
    """ Return category """
    if "Wiki Wednesday " in title:
        return "Wiki"
    elif "Flash Player" in title:
        return "Flash"
    elif "Adobe Flash" in title:
        return "Flash"
    elif "Offline Editor" in title:
        return "Offline"
    elif "LEGO" in title:
        return "Extensions"
    elif "WeDo" in title:
        return "Extensions"
    elif "PicoBoard" in title:
        return "Extensions"
    elif "Scratch Video Update" in title:
        return "Video"
    elif "Blog" in title:
        return "Blog"
    elif "Scratch Day" in title:
        return "Event"
    elif "April Fool's" in title:
        return "Event"
    elif "Scratch Camp" in title:
        return "Event"
    elif "Hour of Code" in title:
        return "Event"
    elif "Updates!" in title:
        return "Web"
    elif "owntime" in title:
        return "Downtime"
    else:
        return "Uncategorized"

if __name__ == "__main__":
    # Log in to GitHub
    g = github3.login(USERNAME, PASSWORD)
    repo = g.repository(USERNAME, REPOSITORY)

    temp = repo.file_contents("template.html")
    temp_content = b64decode(temp.content).decode("utf-8")

    # Get Pages
    page = requests.get(FORUM).content
    soup = BeautifulSoup(page, "html.parser")
    contents = soup.find_all("div", class_="tclcon")

    # Parse

    flash = []
    offline = []
    extensions = []
    wiki = []
    video = []
    blog = []
    event = []
    web = []
    downtime = []
    uncategorized = []

    for tag in contents:
        page_name = tag.h3.a.string
        page_link = "https://scratch.mit.edu" + tag.h3.a["href"]
        if page_name == "The Announcements Directory":
            continue
        markup = "<li><a href='{link}'>{name}</a></li>\n".format(link=page_link, name=page_name)
        if markup[:-15] in temp_content:
            continue
        category = categorize(page_name)
        if category == "Wiki":
            wiki.append(markup)
        elif category == "Flash":
            flash.append(markup)
        elif category == "Offline":
            offline.append(markup)
        elif category == "Extensions":
            extensions.append(markup)
        elif category == "Video":
            video.append(markup)
        elif category == "Blog":
            blog.append(markup)
        elif category == "Event":
            event.append(markup)
        elif category == "Web":
            web.append(markup)
        elif category == "Downtime":
            downtime.append(markup)
        else:
            uncategorized.append(markup)
    args = {
        "lastUpdated" : "{lastUpdated}",
        "newTopicRules" : "",
        "newTopicFlash" : ("{newTopicFlash}\n" + ''.join(flash)),
        "newTopicOffline" : ("{newTopicOffline}\n" + ''.join(offline)),
        "newTopicExtensions" : ("{newTopicExtensions}\n" + ''.join(extensions)),
        "newTopicWiki" : ("{newTopicWiki}\n" + ''.join(wiki)),
        "newTopicVideo" : ("{newTopicVideo}\n" + ''.join(video)),
        "newTopicBlog" : ("{newTopicBlog}\n" + ''.join(blog)),
        "newTopicEvent" : ("{newTopicEvent}\n" + ''.join(event)),
        "newTopicMisc" : "",
        "newTopicVersion2" : "",
        "newTopicWikinews" : "",
        "newTopicWeb" : ("{newTopicWeb}\n" + ''.join(web)),
        "newTopicDowntime" : ("{newTopicDowntime}\n" + ''.join(downtime)),
        "newTopicUncategorized" : ("{newTopicUncategorized}\n" + ''.join(uncategorized)),
    }
    args2 = {
        "lastUpdated" : datetime.datetime.utcnow().strftime("%Y/%m/%d (%a) %H:%M"),
        "newTopicRules" : "",
        "newTopicFlash" : "",
        "newTopicOffline" : "",
        "newTopicExtensions" : "",
        "newTopicWiki" : "",
        "newTopicVideo" : "",
        "newTopicBlog" : "",
        "newTopicEvent" : "",
        "newTopicMisc" : "",
        "newTopicVersion2" : "",
        "newTopicWikinews" : "",
        "newTopicWeb" : "",
        "newTopicDowntime" : "",
        "newTopicUncategorized" : "",
    }


    temp_content_new = temp_content.format(**args)
    temp.update("Update Directory", temp_content_new.encode("utf-8"))

    index = repo.file_contents("index.html")
    index_content_new = temp_content_new.format(**args2)
    index_content_new = REMOVE_BLANK_LINES.sub("\n", index_content_new)
    index.update("Update Directory", index_content_new.encode("utf-8"))
