from instabot import Bot
from package import variables as v
username = v.usernameinsta
password = v.passwordinsta
bot = Bot()
bot.login(username=username, password=password)

#bot.upload_photo("yoda.jpg", caption="biscuit eating baby")
bot.follow("elon.ai")