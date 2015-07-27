# -*- coding: utf-8 -*-
import os
import logging
import random
import time
from os.path import expanduser

homedir = expanduser("~")
repodir = '/git/lists/'

class irc_colors:
        NORMAL = u"\u000f"
        BOLD = u"\u0002"
        UNDERLINE = u"\u001f"
        REVERSE = u"\u0016"
        WHITE = u"\u00030"
        BLACK = u"\u00031"
        DARK_BLUE = u"\u00032"
        DARK_GREEN = u"\u00033"
        RED = u"\u00034"
        BROWN = u"\u00035"
        GREEN = u"\u00039"

logging.basicConfig(level=logging.WARNING, format="[%(asctime)s] [%(levelname)s] %(message)s")

def getuser(ircmsg):
    return ircmsg.split(":")[1].split('!')[0]


_command_dict = {}


def command(name):
    # The decorator appending all fn's to a dict
    def _(fn):
        # Decorators return an inner function whom we
        # pass the function.
        _command_dict[name] = fn
    return _


def nothing(args):
    return ""

def get_command(name):
    # Explicity over implicity?
    # Fuck that

    # We just lower the string.
    # and check later its upper cased
    if name.lower() in _command_dict:
        return _command_dict[name.lower()]
    else:
        return nothing

@command("help")
def get_help(args):
    sendmsg = args["sendmsg"]
    commands = [
        ".add: add an item to your list",
        ".del: delete an item from your list",
        ".newlist: erase your list to start anew"
    ]
    for command in commands:
        sendmsg(getuser(args["raw"]), command)
        time.sleep(1)
    return "sent ;)"

@command("add")
def add(args):
    user = getuser(args["raw"])
    item = args["args"]
    item = " ".join(item)
    try:

        logging.debug("Attempting to open file: " + homedir + repodir + user + ".txt [append/create]")

        with open(homedir + repodir + user + ".txt", "a+") as textlist:
            lines = textlist.readlines()
            for line in lines:

                logging.debug("Reading line from file: " + line)

                if item.strip().lower() == line.strip().lower():

                    logging.info("Found a match for " + item + "in file")

                    return user + ", you've already added that..."
            else:
                textlist.write(item + "\n")
        return irc_colors.BOLD + item.capitalize() + irc_colors.NORMAL + \
               " successfully added to " + user + "'s list."
    except IOError as error:
        logging.warning(str(error))
        return "uh something bad happened"

@command("del")
def delete(args):
    user = getuser(args["raw"])
    item = args["args"]
    item = " ".join(item)
    try:

        logging.debug('Attempting to open file: ' + homedir + repodir + user + ".txt [reading]")
        logging.debug('Attempting to open new file: ' + homedir +repodir + user + ".txt.new [writing]")

        with open(homedir + repodir + user + ".txt", "r") as oldlist, \
                open(homedir +repodir + user + ".txt.new", "w+") as newlist:
            found = 0
            for line in oldlist.readlines():

                logging.debug('Checking line in file: ' + line + ' against item: ' + item)

                if item.strip().lower() != line.strip().lower():

                    logging.debug("Writing " + line + " to " + homedir +repodir + user + ".txt.new")

                    newlist.write(line)
                else:
                    found = 1
            if found:

                logging.info("Found " + item + " in " + homedir + repodir + user + ".txt")

                os.rename(homedir +repodir + user + ".txt.new", homedir + repodir + user + ".txt")
                return irc_colors.BOLD + item.capitalize() + irc_colors.NORMAL +\
                       " successfully deleted from " + user + "'s list."
            else:
                os.remove(homedir +repodir + user + ".txt.new")
                return irc_colors.BOLD + item.capitalize() + irc_colors.NORMAL + " wasn't in " + user + "'s list."
    except IOError as error:
        logging.warning(str(error))
        return user + " doesn't have a list."

@command("newlist")
def new_list(args):
    user = getuser(args["raw"])
    try:
        logging.debug("Deleting file: " + homedir + repodir + user + ".txt")
        os.remove(homedir + repodir + user + ".txt")
    except OSError as error:
        logging.warning(str(error))
        return user + "'s list has already been cleared."
    return user + "'s previous list has been cleared."

@command("r")
def random_option(args):
    choices = " ".join(args["args"]).split("|")
    choice_list = []
    for choice in choices:
        choice_list.append(choice.strip())
    return random.choice(choice_list)

@command("hype")
def hype(args):
    import time
    hypeText = []
    toResolve = args["args"]
    argString = " ".join(toResolve)
    if len(toResolve) < 1:
        hypeText = ["F R O S T",
                    "R",
                    "O",
                    "S",
                    "T"]
    elif len(argString) > 8:
        return ""
    else:
        char = 0
        while char < len(argString):
            c = argString[char].upper()
            if char == 0:
                x = 1
                while x < len(argString):
                    c += (" " + argString[x].upper())
                    x += 1
            hypeText.append(c)
            char += 1
    
    sendmsg = args["sendmsg"]
    channel = args["channel"]
    for lines in hypeText:
        sendmsg(channel, lines)
        time.sleep(.3)
    return ""

@command("8")
def eightball(args):
    responses = [
        "It is decidedly so",
        "Without a doubt",
        "Yes definitely",
        "You may rely on it",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
        "Yes",
        "Signs point to yes",
        "Reply hazy try again",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don't count on it",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful"
    ]
    number = random.randint(0, 100)
    if number == 0:
        return "Commit suicide"
    else:
        return random.choice(responses)
