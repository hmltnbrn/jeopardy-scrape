import sys
import urllib2
import json
import re
import datetime
import uuid
from bs4 import BeautifulSoup

quick_access = {} # access contestants throughout

class Game(object):

    def __init__(self, link, season):
        self.link = link
        self.html = BeautifulSoup(urllib2.urlopen(link), "html.parser")
        self.season = str(season)
        self.show_number, self.air_date = self.html.find(id='game_title').find('h1').find(text=True).split(' - ')
        self.before_double = self.check_double()
        self.contestants = self.set_contestants()
        self.rounds = self.set_rounds()
        self.set_winners()

    def check_double(self):
        if(datetime.datetime.strptime(self.air_date, '%A, %B %d, %Y').isoformat() < "2001-11-26T00:00:00"):
            return True
        else:
            return False

    def set_rounds(self):
        rounds = []
        first_round = self.html.find(id='jeopardy_round')
        second_round = self.html.find(id='double_jeopardy_round')
        final_round = self.html.find(id='final_jeopardy_round')
        if first_round:
            rounds.append(Round(1, "Jeopardy!", self.before_double, first_round))
        if second_round:
            rounds.append(Round(2, "Double Jeopardy!", self.before_double, second_round))
        if final_round:
            rounds.append(Round(3, "Final Jeopardy!", self.before_double, final_round))
        return rounds

    def set_contestants(self):
        contestants = []
        people = self.html.findAll(class_='contestants')
        for i in xrange(len(people)):
            parse_string = re.search('( a | an )(.*)( from )(.*)', people[i].get_text())
            id = people[i].find("a")["href"].split("=")[1]
            name = people[i].find("a").get_text()
            quick_access[name.split(" ")[0]] = id
            contestants.append(Contestant(id, name, parse_string.group(2).replace(" originally", ""), parse_string.group(4), self.html, i))
        return contestants

    def set_winners(self):
        all_totals = [i.game_status.final_jeopardy_total for i in self.contestants]
        biggest = 0
        index = 0
        tie = False
        for i in xrange(len(all_totals)):
            if(biggest == all_totals[i]):
                tie = True
            elif(biggest < all_totals[i]):
                tie = False
                biggest = all_totals[i]
                index = i
        if not tie:
            self.contestants[index].game_status.set_winner()
        else:
            if(all_totals[0] == 0 and all_totals[1] == 0 and all_totals[2] == 0):
                return

    def get_data(self):
        return {
            "id": self.link.split("=")[1],
            "season": self.season,
            "show_number": self.show_number.split(" #")[1],
            "air_date": datetime.datetime.strptime(self.air_date, '%A, %B %d, %Y').isoformat(),
            "before_double": self.before_double,
            "rounds": [i.get_data() for i in self.rounds],
            "contestants": [i.get_data() for i in self.contestants]
        }

class Round(object):

    def __init__(self, id, name, before_double, html):
        self.id = id
        self.name = name
        self.before_double = before_double
        self.html = html
        self.categories = self.set_categories()

    def set_categories(self):
        categories = []
        cats = self.html.findAll(class_='category')
        clues = self.html.findAll(class_='clue')
        for i in xrange(len(cats)):
            cat_name = cats[i].find(class_='category_name')
            if cat_name:
                categories.append(Category(cat_name.find(text=True), clues[i:len(clues):6], self.id, self.before_double, self.html if self.name == 'Final Jeopardy!' else None))
        return categories

    def get_data(self):
        return {
            "id": self.id,
            "categories": [i.get_data() for i in self.categories]
        }

class Category(object):

    def __init__(self, name, html, round, before_double, answer_div = None):
        self.id = uuid.uuid4()
        self.name = name
        self.html = html
        self.round = round
        self.before_double = before_double
        self.answer_div = answer_div
        self.clues = self.set_clues()

    def set_clues(self):
        clues = []
        for i in xrange(len(self.html)):
            value = self.html[i].find(class_="clue_value") if self.html[i].find(class_="clue_value_daily_double") is None else self.html[i].find(class_="clue_value_daily_double")
            question = self.html[i].find(class_="clue_text")
            answer = self.answer_div.find("div") if self.answer_div is not None else self.html[i].find("div")
            if(value and question and answer):
                clues.append(Clue(value.find(text=True), question.get_text(), re.sub('<[^<]+?>', '', re.search('<em class="correct_response">(.*)</em>', answer["onmouseover"]).group(1)), answer["onmouseover"], i, self.round, self.before_double))
            elif(question and answer):
                clues.append(Clue("", question.get_text(), re.search(r'<em class=\\"correct_response\\">(.*)</em>', answer["onmouseover"]).group(1), answer["onmouseover"], i, self.round, self.before_double))
        return clues

    def get_data(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "clues": [i.get_data() for i in self.clues]
        }

class Clue(object):

    def __init__(self, value, question, answer, mouseover_text, slot, round, before_double):
        self.id = uuid.uuid4()
        self.value = None
        self.question = question
        self.answer = answer
        self.daily_double = False
        self.daily_double_wager = None
        self.triple_stumper = False
        self.rights = self.set_rights(mouseover_text)
        self.wrongs = self.set_wrongs(mouseover_text)
        self.slot = slot
        self.round = round
        self.before_double = before_double
        self.handle_value(value)

    def handle_value(self, value):
        if(value):
            if value[0] == "D":
                self.daily_double = True
                self.daily_double_wager = int(re.sub("[$,]", "", value.split(" ")[1]))
                self.value = int(self.set_dd_value())
            else:
                self.value = int(value.replace("$", ""))

    def set_dd_value(self):
        if(self.round == 1):
            if(self.before_double == True):
                return str(self.slot + 1) + "00"
            else:
                return str((self.slot + 1)*2) + "00"
        elif(self.round == 2):
            if(self.before_double == True):
                return str((self.slot + 1)*2) + "00"
            else:
                return str((self.slot + 1)*4) + "00"
        else:
            return None

    def set_rights(self, mouseover):
        html = BeautifulSoup(mouseover, "html.parser")
        rights = html.findAll(class_="right")
        return [quick_access[i.get_text()] for i in rights]

    def set_wrongs(self, mouseover):
        result = []
        html = BeautifulSoup(mouseover, "html.parser")
        wrongs = html.findAll(class_="wrong")
        for i in wrongs:
            if i.get_text() == "Triple Stumper":
                self.triple_stumper = True
            else:
                result.append(quick_access[i.get_text()])
        return result

    def get_data(self):
        return {
            "id": str(self.id),
            "clue": self.question,
            "value": self.value,
            "answer": self.answer,
            "daily_double": self.daily_double,
            "daily_double_wager": self.daily_double_wager,
            "triple_stumper": self.triple_stumper,
            "rights": self.rights,
            "wrongs": self.wrongs
        }

class Contestant(object):

    def __init__(self, id, name, profession, hometown, html, slot):
        self.id = id
        self.first_name = name.split(" ")[0]
        self.last_name = " ".join(name.split(" ")[1:])
        self.profession = profession
        self.hometown = hometown
        self.game_status = GameContestant(self.first_name, html, slot)

    def get_data(self):
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "profession": self.profession,
            "home_town": self.hometown,
            "game_status": self.game_status.get_data()
        }

class GameContestant(object):

    def __init__(self, fn, html, slot):
        self.winner = False
        self.jeopardy_total = None
        self.double_jeopardy_total = None
        self.final_jeopardy_total = None
        self.final_jeopardy_wager = None
        self.set_totals(fn, html, slot)
        self.set_wager(fn, html, slot)

    def set_totals(self, fn, html, slot):
        first_round = html.find(id='jeopardy_round').findAll(class_=re.compile("score_positive|score_negative"))
        self.jeopardy_total = int(re.sub("[$,]", "", first_round[(0-slot)-1].get_text())) if first_round is not None else None
        second_round = html.find(id='double_jeopardy_round').findAll(class_=re.compile("score_positive|score_negative"))
        self.double_jeopardy_total = int(re.sub("[$,]", "", second_round[(0-slot)-1].get_text())) if second_round is not None else None
        third_round = html.find(id='final_jeopardy_round').findAll(class_=re.compile("score_positive|score_negative"))
        self.final_jeopardy_total = int(re.sub("[$,]", "", third_round[(0-slot)-4].get_text())) if third_round is not None else None

    def set_wager(self, fn, html, slot):
        new_html = BeautifulSoup(html.find(id='final_jeopardy_round').find(class_='category').find("div")["onmouseover"], "html.parser").findAll("td")
        if(new_html):
            for i in xrange(len(new_html)):
                if(new_html[i].get_text() == fn):
                    self.final_jeopardy_wager = int(re.sub("[$,]", "", new_html[i+2].get_text()))

    def set_winner(self):
        self.winner = True

    def get_data(self):
        return {
            "winner": self.winner,
            "jeopardy_total": self.jeopardy_total,
            "double_jeopardy_total": self.double_jeopardy_total,
            "final_jeopardy_total": self.final_jeopardy_total,
            "final_jeopardy_wager": self.final_jeopardy_wager
        }

def get(link, season):
    game = Game(link, season)

    return game.get_data()

if __name__ == "__main__":
    print "Generating game data..."

    game = Game(sys.argv[1], sys.argv[2]) # first argument -- j-archive link | second -- season

    data = game.get_data()

    with open('game_data.json', 'w+') as f:
        json.dump(data, f)
        print "Finished successfully"
