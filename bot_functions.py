import json
from time_converter import TimeConverter
from datetime import datetime
import os.path
import discord
import discord.ext

class BotFunctions():

    # Variables
    tc = TimeConverter()
    after_10_15 = tc.compare_times(hour1=datetime.now(
    ).hour, hour2=22, minute1=datetime.now().minute, minute2=15)

    bossy_bdo = None
    days_of_the_week = ["Monday", "Tuesday",
                        "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = datetime.today().weekday()

    # Read json file upon init
    def __init__(self):
        with open("bosses.json", "r") as bossy:
            self.bossy_bdo = json.load(bossy)
        self.notepad = "notepad.txt"
        self.if_file_exists(self.notepad)

    def if_file_exists(self, filename):
        if os.path.exists(filename):
            print(f"Plik {filename} istnieje")
        else:
            print(f"Plik {filename} nie istnieje. Tworzę nowy.")
            try:
                f = open(filename, "w")
                f.close()
            except FileNotFoundError:
                print(f"Nie można utworzyć pliku {filename}")
    # Return next boss
    def next_boss(self):

        if(self.after_10_15 == False):
            return self.todays_next_boss()
        else:
            return self.first_boss_tomorrow()

    # If it's before 10.15pm return this
    def todays_next_boss(self):
        time = datetime.now()
        hour = time.strftime("%H:%M:%S")
        time_of_next_boss = ""
        next_boss = ""
        todays_day = self.days_of_the_week[int(datetime.now().weekday())]
        todays_bosses = self.bossy_bdo["bosses"]["days"][todays_day]

        for i in range(len(todays_bosses)):
            time = todays_bosses[i][1].split(":")
            if(self.tc.compare_times(hour1=time[0], hour2=datetime.now().hour, minute1=int(time[1]) + 10, minute2=datetime.now().minute)):
                time_of_next_boss = time
                next_boss = todays_bosses[i][0]
                break

        return f"\nAktualna godzina: {hour}\n**Nastepny boss:**\n\n{next_boss} - {time[0]}:{time[1]}"

    # If it's after 10.15pm return this
    def first_boss_tomorrow(self):
        next = self.bossy_bdo["bosses"]["days"][self.days_of_the_week[datetime.now(
        ).weekday() + 1]][0][0]
        time = self.bossy_bdo["bosses"]["days"][self.days_of_the_week[datetime.now(
        ).weekday() + 1]][0][1]

        return f"**Nastepny boss:**\n\n{next} - {time}"

    # Return all the bosses for today
    def all_todays_bosses(self):
        time = datetime.now()
        hour = time.strftime("%H:%M:%S")
        time_change = 1
        next_boss_index = self.todays_next_index()
        bosses = f"\n**Dzisiejsze bossy:** \nAktualna godzina: {hour}\n\n"
        todays_day = self.days_of_the_week[int(datetime.now().weekday())]
        todays_bosses = self.bossy_bdo["bosses"]["days"][todays_day]
        for i in range((len(todays_bosses))):
            if(i == next_boss_index):
                bosses += f"**{todays_bosses[i][0]}: {todays_bosses[i][1]} - nastepny/obecny boss\n**"
            else:
                bosses += f"{todays_bosses[i][0]}: {todays_bosses[i][1]}\n"
        if time_change == 0:
            return bosses
        else:
            return bosses + "\nUWAGA. Aktualnie zmieniono czas z zimowego na letni.\nDo środy, bossy respią się godzinę później, niż jest to pokazane wyżej."

    # Return index of the next boss until (t+10)

    def todays_next_index(self):
        index = None

        if(not self.after_10_15):
            todays_day = self.days_of_the_week[int(datetime.now().weekday())]
            todays_bosses = self.bossy_bdo["bosses"]["days"][todays_day]

            for i in range(len(todays_bosses)):
                time = todays_bosses[i][1].split(":")
                if(self.tc.compare_times(hour1=time[0], hour2=datetime.now().hour, minute1=int(time[1]) + 10, minute2=datetime.now().minute)):
                    index = i
                    break
        return index

    def all_tomorrows_bosses(self):
        embed_today = discord.Embed(
            color=discord.Colour.orange()
        )
        next_boss_index = self.todays_next_index()
        embed_today.set_author(name='Завтрашние боссы:')
        if(datetime.now().weekday() == 6):
            tomorrow = self.days_of_the_week[0]
        else:
            tomorrow = self.days_of_the_week[int(
                datetime.now().weekday()) + 1]

        tomorrows_bosses = self.bossy_bdo["bosses"]["days"][tomorrow]
        for i in range((len(tomorrows_bosses))):
            embed_today.add_field(name='_ _', value=f"{tomorrows_bosses[i][0]}: {tomorrows_bosses[i][1]}")

        return embed_today

    def resetNick(self, nickname):
        pt_list = ['[PT 1] ', '[PT 2] ', '[PT 3] ']
        try:
            for pt in pt_list:
                if pt in nickname:
                    new_nick = nickname[7:]
                elif pt not in nickname:
                    continue
                else:
                    new_nick = nickname
            return new_nick
        except UnboundLocalError:
            return nickname

    def addParty(self, nick, party):
        party_dict = {1: '[PT 1] ', 2: '[PT 2] ', 3: '[PT 3] '}
        nick = self.resetNick(nick)
        nick = party_dict[party] + nick
        return str(nick)

    def help(self):
        help_list = """```
.b - pokazuje bossy na dziś, wraz z aktualnym\n 
.jutro - pokazuje bossy na jutro\n
.next - pokazuje następnego bossa\n
------------------\n
.pt1 - party 1\n
.pt2 - party 2\n
.pt3 - party 3\n
.reset - reset party
------------------\n
.discord - zaproszenie na discorda
```
        """
        return help_list

    def save_notepad_message(self, name, message):
        with open(f"{self.notepad}", "a") as f:

            print("Otwarto plik")
            f.write(f"{name}\n{message}\nend\n")
            print(f"Zapisano tytul: {name}\nWiadomość: {message}")



    def show_notepad_message(self, name):
        with open (f"{self.notepad}", "r") as notepad:
            lines = []
            answer = []
            for line in notepad:
                lines.append(line.strip())   #  [line.strip() for line in notepad]






