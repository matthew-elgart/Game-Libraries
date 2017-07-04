import os

class Game(object):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def play(self):
        raise NotImplementedError("Abstract version of method")

    def source(self):
        raise NotImplementedError("Abstract version of method")

class SteamGame(Game):
    def __init__(self, name, appid):
        Game.__init__(self, name)
        self.appid = appid

    def play(self):
        os.system('"C:\Program Files (x86)\Steam\steam.exe" -applaunch ' + self.appid)

    def source(self):
        return "Steam"

    def get_id(self):
        return self.appid

class GOGGame(Game):
    def __init__(self, name):
        Game.__init__(self, name)

    def play(self):
        os.system('"C:\Program Files (x86)\GOG Galaxy\Games\\' + self.name + '\Launch ' + self.name + '.lnk"')

    def source(self):
        return "GOG"

games_list = []

def get_steam_games(games):
    steamdir = "C:\Program Files (x86)\Steam\steamapps"
    if not os.path.isdir(steamdir):
        return games
    for dir in os.listdir(steamdir):
      if dir.startswith("appmanifest") and dir.endswith(".acf"):
        file_obj = open(os.path.join(steamdir, dir))
        lines = file_obj.readlines()
        name = lines[6][16:-2]
        appid = lines[2][11:-2]
        games.append(SteamGame(name, appid))
        file_obj.close()
    return games

def get_gog_games(games):
    gogdir = "C:\Program Files (x86)\GOG Galaxy\Games"
    if not os.path.isdir(gogdir):
        return games
    for dir in os.listdir(gogdir):
        games.append(GOGGame(dir))
    return games

games_list = get_steam_games(games_list)
games_list = get_gog_games(games_list)

games_list.sort(key=lambda x:x.name)
for i in range(len(games_list)):
    #TODO: polymorphize this to say (Steam) or (GOG) or whatever
    print str(i+1) + ": " + games_list[i].get_name() + " (" + games_list[i].source() + ")"
    
selection = int(input("Select number from games list: "))
if selection >= 1 and selection <= len(games_list):
    game = games_list[selection-1]
    print "You have selected " + game.get_name()
    game.play()
else:
    print "Your selection is wrong. Git gud and try again."

#print ""
#localdir = "hi"
#print os.path.join(rootdir, localdir)
#os.system(os.path.join(rootdir, localdir))
