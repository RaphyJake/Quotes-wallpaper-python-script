#!/bin/python3
import os
import subprocess
import re
from random import randint
import linecache
from PIL import Image, ImageFont, ImageDraw
from sys import argv, platform


# the fucker reading arguments


def main():
    if argv.__len__() == 1 or argv[1] == "--help":
        print(hellp)
    if "--v" in argv:
        print(version)
    if "-l" in argv and "-t" in argv:
        print("Damn son, -z and -t won't work togheter! choose one")
        exit(0)
    if any(i in argvlist for i in argv):
        picgen(argv)


def picgen(agrv):

    # fetch screen res
    p = subprocess.Popen("xrandr  | grep \* | cut -d' ' -f4", stdout=subprocess.PIPE, shell=True).communicate()[0]
    res = (re.sub("[^\w\d]|[bn]", "", str(p))).split("x")
    res = [int(i) for i in res]

    # fetch quotes from source

    quotes = cwd + "/quotes.txt"
    f = open(quotes)
    num_lines = len(f.readlines())

    if "-l" in argv:
        k = argv.index("-l")
        try:
            q = str(linecache.getline(quotes, int(argv[k+1])))
        except IndexError:
            print("Error: There's no "+str(k+1)+"th line in your file!")
            exit(0)
        except ValueError:
            print("Error: \""+str(k)+"\" is not a integer!")
            exit(0)
    elif "-t" in argv:

        for i in argv:
            if "[" in i:
                start = argv.index(i)
            if "]" in i:
                end = argv.index(i)
        try:
            q = (" ".join(argv[start:end+1])).strip("[]")
        except UnboundLocalError:
            print("Darn son, put some brackets!")
            exit(0)

    else:
        q = str(linecache.getline(quotes, randint(1, num_lines)))
    q = q.replace("\\n", "\n")

    if "-s" in argv:
        k = argv.index("-s")
        try:
            pic = Image.open(argv[k+1])
        except FileNotFoundError:
            print("Looks like the file doesn't exist!")
            exit(0)
        except IndexError:
            print("Darn son, put some path after that -s")
            exit(0)
        except OSError:
            print("That doesn't look like an image!")
            exit(0)
        res = [int(i) for i in pic.size]
    else:
        pic = Image.new("RGB", res)
    d = ImageDraw.Draw(pic)

    if "-z" in argv:
        k = argv.index("-z")
        try:
            j = argv[k+1]
        except IndexError:
            print("Darn son, put some int after that -z")
            exit(0)
        if j.isnumeric():
            h = int(j)
        else:
            try:
                h = sizedict[j]
            except KeyError:
                print("Size isn't either a number or \"huge\"/ \"small\"")
                exit(0)
    else:
        h = 36

    font = ImageFont.truetype(cwd + "/font1.ttf", int(h))
    h_len, v_len = (d.textsize(q, font))

    while h_len >= res[0]:
        h -= 1
        font = ImageFont.truetype(os.getcwd() + "/font1.ttf", h)
        h_len, v_len = (d.textsize(q, font))

    d.text((res[0] - h_len - 10, res[1] - v_len), q, (255, 255, 255), font=font)

    if "-n" in agrv:
        k = agrv.index("-n")
        name = argv[k+1]+".png"
    else:
        name = str(randint(0, 300)) + ".png"

    if "-p" in argv:
        os.system("rm " + cwd + "/*.png")

    pic.save(name)

    if "-w" in argv:
        save(name)
    exit(0)


def save(name):
    os = platform
    if os == "win32":
        from ctypes import windll
        windll.user32.SystemParametersInfoW(20, 0, cwd+"/"+name, 0)
        exit(0)
    else:
        de = subprocess.Popen("echo $XDG_CURRENT_DESKTOP", stdout=subprocess.PIPE, shell=True).communicate()[0]
        de = re.sub("[^\w\d]|[bn]", "", str(de))

    kdecmd = """ 'var allDesktops = desktops();print (allDesktops);
for (i=0;i<allDesktops.length;i++)
{d = allDesktops[i];d.wallpaperPlugin = "org.kde.image";
d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
d.writeConfig("Image",\""""+cwd+"/"+name+"""\")}'
"""
    if de == "GNOME":
        subprocess.Popen("gsettings set org.gnome.desktop.background picture-uri "+cwd+"/"+name, shell=True)
    elif de == "KDE":
        subprocess.Popen("qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript"+kdecmd, shell=True)
    else:
        print("Sorry dude, DE not supported yet.. :(")


# various globals
sizedict = {"huge": 100, "small": 16}

argvlist = ("-l", "-n", "-r", "-p", "-s", "-w", "-z", "-t")
version = "alpha 0.4"
cwd = str(os.getcwd())
hellp = """Usage:
--help                             = Show this page.
--v                                = Display version\n
-l [integer]                       = Choose wich line to use
-n [text]                          = choose filename (.png)
-r                                 = use a random line. Default behaviour.
-p                                 = purge old pictures.
-s [path]                          = Use a custom source picture
-w                                 = Set as current wallpaper. (Experimental..)
-z [small | huge | value]          = set text sixe (Note = Default is 36, but it automatically shrinks text to fit in.
                                    So this comes really handy just you use the -s option.
-t [text]                          = Use your custom text and ignore quotes.txt. Can't obviously be used with -l
                                    Wrap your text inside two square brakets [text]. (buggy, watch out for bash shit son
                                    """


if __name__ == "__main__":
    main()
