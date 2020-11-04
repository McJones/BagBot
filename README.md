# BagBot

The bot for my private Discord Server that assigns roles.
Probably not useful to you, but who knows it might be.

In its current form this bot reproduces the basic r*eact to a post, get assigned a role* functionality of almost every existing bot out there.
Why then would I build this myself instead of using Dyno/Meeseeks/etc?
Frankly I don't trust them, also it was fun learning exercise to see how the discord API works.

## Installation

First you will need to have Git and Python installed, I used Python 3.8 but go with whatever flavour you like that discord.py supports.
Next you will need some python libraries, both of which are on pip already, lucky us.

### Requirements

- discord.py
- dotenv

Ok with those done you now need to clone the repo: `git clone https://github.com/McJones/BagBot.git` to wherever you like to keep your projects.
Now it is time to set up the discord developer API side of things.

### Discord Configuration

This has quite a few steps and I am assuming at this point you already have a discord server you've admin permissions over ready and all the roles configured.
I am also assuming you are comfortable with managing Discord itself.

*I wrote these instructions when I did this myself, they might now be wrong by the time you are reading them, sorry, why not update them and send in a pull request?*

First go to the [Discord developer site](https://discord.com/developers/applications).
Then Click on the New Application button.
You'll have to give it a name so spend a bit of time thinking about it, after all names are important.

Discord uses the term application to mean anything that uses the API, we will be making a bot which is a subset of applications.
So all bots are applications, not all applications are bots.
To make a bot in the application page on the left side there should be a `bot` section, click it and there will be a button to make a bot, click that too.
In here you can customise the bots appearance and name, spend a bit of time and make it something lovely, after all you will have to live with it, not me.

Click on the Oauth section also over on the left of the page to get our token.
We will need the token so that Discord knows that it is our bot and not some random person.
Inside the oauth section there is a big grid of scopes, click `bot` and then you can set the bot specific permission in the grid that appears below that.
I selected the following permissions:

- `Manage Roles`
- `Send Messages`
- `Manage Messages`
- `Read Message History`
- `Use External Emoji`
- `Add Reactions`

Honestly not sure which I needed, I just didn't want to give it admin permissions so I took a guess at what it might need, it works and that's enough for me.
With that done grab that invite URL from that page, follow it to add your bot to the server.
This doesn't actually do anything besides set stuff up later for the bot.

Now we need to get the oauth token for our bot so tha Discord actually knows its us.
Jump back into the Bot section and there is a Token header on the page, copy the token from there, we will need it in just a second.

### Bot Configuration

Ah we are finally up to the good stuff, setting up our bot for our specific needs.

First you will need to create an environment file (also known as a text file...), I called mine `.env` but you can name yours whatever you want as long as you update the code to find it.
This will need four different variables set, the first is your oauth token:

```
DISCORD_TOKEN=BigLongTokenGoesHere
```

Remember that token we *just* copied?
Paste it in there.

Next you will need to set the name of your server and the channel that the reaction message will live in.

```
DISCORD_SERVER=Your Server Name Goes Here
REACTION_CHANNEL=Your Channel Name Goes Here
```

Finally you will need to ID of your message, if you aren't sure how to get the ID [Discord has a guide on this](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-):

```
REACTION_MESSAGE_ID=012345678911121314
```

Ok that is the environment configured, lets make some changes to the code.
Near the top part of the python file (`bagbot.py`) there is a `role_map` dictionary that looks something like the following:

```py
role_map = {
    '🥚' : 'Good Egg',
    '🛳️' : 'Thunderchild',
    '🔪' : 'Stabbing',
    '💯' : 'The Living Embodiment Of The 100 Emoji'}
```

Modify that dictionary so that it has the emoji and roles you care about.
With that done we are ready to turn on our bot.

### Running The Bot

Getting the bot running is easy, run the python file:

```
python bagbot.py
```

The bot will then connect and be ready to start assigning and removing roles.
It will last as long as the python process lasts.
This means for longer term use you will need to work out how you want to keep the bot alive.
I run mine on an old machine I have lying around, your needs and resources are likely different and will need a different approach.
Sorry I can't help with that.

## Contributing

This bot exists to fill a niche me and my friends needed, I am hesitant therefore to accept many contributions to the project.
As such I am also likely to close issues that aren't from friends/friends of friends as out of scope.
It's not personal, I don't really have the time to properly add another OSS project to my slate.
Feel free to still open them, I just make no promises as to what I will do with them...

That said, if you do have a good idea built or a bug fix ready then totally open a pull request and I will give it a look.
The first contribution *hint* *hint* should really be adding a contributors file, updating this section from the readme, and modifying the license to assign copyright to the contributors instead of just me.

## Fabulously Asked Questions

**Why not just use Dyno/Meeseeks/other bot?**

When initially setting up roles I did consider using one of them and even started setting it up.
Then a friend pointed out that these things have huge access to a lot of data and very few of them are open source.
Do I trust these companies with what is basically complete access to all comms in discord?

No, I don't think I do, and with them being primarily closed source means I can't easily check what they are doing.
I'm already putting a lot of trust in discord, I don't want to spread that.
Hence making my own.

**Hey your code isn't very Pythonic, why is that?**

I am not a Python developer, just discord.py is great so I used that.
Feel free to fix it to be a better follower of The Way Of The Snake and let me know.

**Why use .env files instead of format X?**

I like the minimal form of .env files and the dotenv python package.

**Have you considered adding feature X?**

Nope, if you like that idea, fork the repo and give it a go yourself, maybe even offer it back as a pull request.
Python is pretty easy to pick up with only a little bit of practice, you could be having your own little bot in no time.

**Will you be making this available for others to use?**

If you mean *am I fine for you running your own copy of this bot?*, yep totally go for it.
Not only does the license allow you to do this I actively encourage you to do so.

If you mean *am I going to let others use my bot directly as a service in a manner similar to Dyno?*, then the answer is no.
That sounds like a lot of work I don't have time for and more importantly flies in the face of the original intent of the project.

**The bot can't seem to assign any roles, what's up?**

At a guess either you've typoed the names of the emoji or the roles in the `role_map` dictionary.
Also for the bot to be able to assign roles those roles need to be **lower** in the roles list in your discord server than the bot's role.

**Why are IPAs so damn hoppy these days?**

Yeah no idea, it confuses me too.
It's *meant* to be a refreshing pale beer with a hoppy flavour, not liquid embalming fluid.
Oh well, it is what it is now I guess.

**Where can I contact you outside of Github?**

Probably the best spot is [twitter](http://twitter.com/the_mcjones), I am fairly responsive on there.
