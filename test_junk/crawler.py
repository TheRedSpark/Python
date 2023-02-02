from pywebcopy import save_website

save_website(
    url="http://agdsn.me/~hendrik.wolff/memes/",
    project_folder="D://savedpages//",
    project_name="my_site",
    bypass_robots=True,
    debug=False,
    open_in_browser=False,
    delay=None,
    threaded=False,
)
