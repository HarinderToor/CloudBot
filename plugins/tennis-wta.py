import requests
import json
from lxml import html
from datetime import date
from cloudbot import hook


@hook.command("wta")
def wta(text):
    today = date.today()
    aus_min = date(2018, 1, 14)
    aus_max = date(2018, 1, 28)
    rg_min = date(2018, 5, 27)
    rg_max = date(2018, 6, 10)
    wim_min = date(2018, 7, 2)
    wim_max = date(2018, 7, 15)
    us_min = date(2018, 8, 27)
    us_max = date(2018, 9, 10)
    if (today >= aus_min and today <= aus_max) or (today >= rg_min and today <= rg_max) or (
        today >= wim_min and today <= wim_max) or (today >= us_min and today <= us_max):
        url = 'http://www.wtatennis.com/scores_gs.json'
    else:
        url = 'http://www.wtatennis.com/scores.json'

    slam_dict = {'Australian Open': 'Melbourne, Australia', 'Championnats Internationaux de France': 'Paris, France',
                 'The Championships': 'Wimbledon, United Kingdom', 'US Open': 'New York City, USA'}

    wta_scores = requests.get(url)
    wta_json = json.loads(wta_scores.text)
    wta_keys = list(wta_json.keys())
    wta_master = {}

    for key in wta_keys:
        match = html.fromstring(wta_json[key])
        match_type = match.get('class').split()[-1]
        round_name = match.xpath('//div[@class="round-ls"]/text()')[0]
        if round_name[0] == ' ':
            round_name = round_name[1:]
        try:
            tournament_name = match.xpath('//div[@class="tournamentname tile_transit transit-attached"]/a/text()')[0]
        except IndexError:
            tournament_name = match.xpath('//div[@class="tournamentname tile_transit transit-attached"]/text()')[0]
        if tournament_name[0] == ' ':
            tournament_name = tournament_name[1:]
        location_element = match.xpath('//div[@class="tournamentname tile_transit transit-attached"]/a/@href')
        try:
            location_name = ' '.join(location_element[0].split('-')[1:]).split(' ')
            location = str(location_name[0]).title() + ', ' + str(location_name[1]).title()
        except IndexError:
            location = slam_dict[tournament_name]
        tournament = f'{tournament_name} ({location})'
        if tournament in wta_master:
            pass
        else:
            wta_master[tournament] = dict.fromkeys(
                ['PlayerOne', 'PlayerTwo', 'OneSetList', 'TwoSetList', 'PointOne', 'PointTwo', 'Status', 'Type',
                 'Server', 'Misc'])
            wta_master[tournament]['PlayerOne'] = []
            wta_master[tournament]['PlayerTwo'] = []
            wta_master[tournament]['OneSetList'] = []
            wta_master[tournament]['TwoSetList'] = []
            wta_master[tournament]['PointOne'] = []
            wta_master[tournament]['PointTwo'] = []
            wta_master[tournament]['Status'] = []
            wta_master[tournament]['Type'] = []
            wta_master[tournament]['Server'] = []
            wta_master[tournament]['Misc'] = []
            wta_master[tournament]['Round'] = []
        players = match.xpath('//div[@class="player-name tile_transit transit-attached"]')
        if match_type == 'singles':
            try:
                player1 = players[0].xpath('a/text()')[0]
            except IndexError:
                player1 = players[0].xpath('text()')[0]
            try:
                player2 = players[1].xpath('a/text()')[0]
            except IndexError:
                player2 = players[1].xpath('text()')[0]
            if player1[0] == ' ':
                player1 = player1[1:]
            if player2[0] == ' ':
                player2 = player2[1:]
            if player1 in wta_master[tournament]['PlayerOne'] or player1 in wta_master[tournament][
                'PlayerTwo'] or player2 in wta_master[tournament]['PlayerOne'] or player2 in wta_master[tournament][
                'PlayerTwo']:
                continue
            else:
                wta_master[tournament]['PlayerOne'].append(player1)
                wta_master[tournament]['PlayerTwo'].append(player2)
        else:
            try:
                player11 = players[0].xpath('a/text()')[0]
            except IndexError:
                player11 = players[0].xpath('text()')[0]
            try:
                player12 = players[1].xpath('a/text()')[0]
            except IndexError:
                player12 = players[1].xpath('text()')[0]
            try:
                player21 = players[2].xpath('a/text()')[0]
            except IndexError:
                player21 = players[2].xpath('text()')[0]
            try:
                player22 = players[3].xpath('a/text()')[0]
            except IndexError:
                player22 = players[3].xpath('text()')[0]
            if player11[0] == ' ':
                player11 = player11[1:]
            if player12[0] == ' ':
                player12 = player12[1:]
            if player21[0] == ' ':
                player21 = player21[1:]
            if player22[0] == ' ':
                player22 = player22[1:]
            team1 = f'{player11} / {player12}'
            team2 = f'{player21} / {player22}'
            if team1 in wta_master[tournament]['PlayerOne'] or team1 in wta_master[tournament]['PlayerTwo'] or team2 in \
                wta_master[tournament]['PlayerOne'] or team2 in wta_master[tournament]['PlayerTwo']:
                continue
            else:
                wta_master[tournament]['PlayerOne'].append(team1)
                wta_master[tournament]['PlayerTwo'].append(team2)
        servea = match.xpath('//div[@class="serve serve-a serve-active"]')
        serveb = match.xpath('//div[@class="serve serve-b serve-active"]')
        if servea:
            wta_master[tournament]['Server'].append('PlayerOne')
        elif serveb:
            wta_master[tournament]['Server'].append('PlayerTwo')
        else:
            wta_master[tournament]['Server'].append('')
        set1_list = match.xpath('//div[@class="set set1"]')
        set2_list = match.xpath('//div[@class="set set2"]')
        set3_list = match.xpath('//div[@class="set set3"]')
        try:
            set11 = set1_list[0].xpath('span/text()')[0]
        except IndexError:
            set11 = ''
        try:
            set21 = set1_list[1].xpath('span/text()')[0]
        except IndexError:
            set21 = ''
        try:
            set12 = set2_list[0].xpath('span/text()')[0]
        except IndexError:
            set12 = ''
        try:
            set22 = set2_list[1].xpath('span/text()')[0]
        except IndexError:
            set22 = ''
        try:
            set13 = set3_list[0].xpath('span/text()')[0]
        except IndexError:
            set13 = ''
        try:
            set23 = set3_list[1].xpath('span/text()')[0]
        except IndexError:
            set23 = ''
        try:
            point1 = match.xpath('//div[@class="point point-a"]/span/text()')[0]
        except IndexError:
            point1 = ''
        try:
            point2 = match.xpath('//div[@class="point point-b"]/span/text()')[0]
        except IndexError:
            point2 = ''
        if match.xpath('//div[@class="win"]'):
            wta_master[tournament]['Status'].append('Finished')
        else:
            wta_master[tournament]['Status'].append('Ongoing')
        wta_master[tournament]['OneSetList'].append([set11, set12, set13])
        wta_master[tournament]['TwoSetList'].append([set21, set22, set23])
        wta_master[tournament]['PointOne'].append(point1)
        wta_master[tournament]['PointTwo'].append(point2)
        susp = match.xpath('.//span[text()="suspended"]')
        if susp:
            wta_master[tournament]['Misc'].append('(Suspended)')
        else:
            wta_master[tournament]['Misc'].append('')
        wta_master[tournament]['Type'].append(match_type)
        wta_master[tournament]['Round'].append(round_name)

    if wta_master:
        for tourney in wta_master:
            ons = ''
            ond = ''
            fins = ''
            fin_d = ''
            for i in range(len(wta_master[tourney]['PlayerOne'])):
                if wta_master[tourney]['Type'][i] == 'singles':
                    if wta_master[tourney]['Status'][i] == 'Ongoing':
                        teama = f'{wta_master[tourney]["PlayerOne"][i]}'
                        teamb = f'{wta_master[tourney]["PlayerTwo"][i]}'
                        s = f' {round_name}: {teama} vs. {teamb}: '
                        if wta_master[tourney]['OneSetList'][i][0]:
                            s = s + f'{wta_master[tourney]["OneSetList"][i][0]}-{wta_master[tourney]["TwoSetList"][i][0]}'
                        else:
                            pass
                        if wta_master[tourney]['OneSetList'][i][1]:
                            s = s + f', {wta_master[tourney]["OneSetList"][i][1]}-{wta_master[tourney]["TwoSetList"][i][1]}'
                        else:
                            pass
                        if wta_master[tourney]['OneSetList'][i][2]:
                            s = s + f', {wta_master[tourney]["OneSetList"][i][2]}-{wta_master[tourney]["TwoSetList"][i][2]}'
                        else:
                            pass
                        if wta_master[tourney]['PointOne']:
                            s = s + f' {wta_master[tourney]["PointOne"][i]}-{wta_master[tourney]["PointTwo"][i]} '
                        else:
                            pass
                        ons = ons + s + ' |' + wta_master[tournament]['Misc'][i]
                    else:
                        if '' in wta_master[tourney]['OneSetList'][i]:
                            if (int(wta_master[tourney]['OneSetList'][i][0]) > int(
                                wta_master[tourney]['TwoSetList'][i][0]) and int(
                                wta_master[tourney]['OneSetList'][i][1]) > int(wta_master[tourney]['TwoSetList'][i][1])):
                                s = f' {round_name}: {wta_master[tourney]["PlayerOne"][i]} d. {wta_master[tourney]["PlayerTwo"][i]}: '
                                if wta_master[tourney]['OneSetList'][i][0]:
                                    s = s + f'{wta_master[tourney]["OneSetList"][i][0]}-{wta_master[tourney]["TwoSetList"][i][0]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][1]:
                                    s = s + f', {wta_master[tourney]["OneSetList"][i][1]}-{wta_master[tourney]["TwoSetList"][i][1]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][2]:
                                    s = s + f', {wta_master[tourney]["OneSetList"][i][2]}-{wta_master[tourney]["TwoSetList"][i][2]}'
                                else:
                                    pass
                                fins = fins + s + ' |' + wta_master[tourney]['Misc'][i]
                            else:
                                s = f' {round_name}: {wta_master[tourney]["PlayerTwo"][i]} d. {wta_master[tourney]["PlayerOne"][i]}: '
                                if wta_master[tourney]['OneSetList'][i][0]:
                                    s = s + f'{wta_master[tourney]["TwoSetList"][i][0]}-{wta_master[tourney]["OneSetList"][i][0]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][1]:
                                    s = s + f', {wta_master[tourney]["TwoSetList"][i][1]}-{wta_master[tourney]["OneSetList"][i][1]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][2]:
                                    s = s + f', {wta_master[tourney]["TwoSetList"][i][2]}-{wta_master[tourney]["OneSetList"][i][2]}'
                                else:
                                    pass
                                fins = fins + s + ' |' + wta_master[tourney]['Misc'][i]
                        else:
                            if (int(wta_master[tourney]['OneSetList'][i][0]) > int(
                                wta_master[tourney]['TwoSetList'][i][0]) and int(
                                wta_master[tourney]['OneSetList'][i][1]) > int(
                                wta_master[tourney]['TwoSetList'][i][1])) or (
                                int(wta_master[tourney]['OneSetList'][i][1]) > int(
                                wta_master[tourney]['TwoSetList'][i][1]) and int(
                                wta_master[tourney]['OneSetList'][i][2]) > int(
                                wta_master[tourney]['TwoSetList'][i][2])) or (
                                int(wta_master[tourney]['OneSetList'][i][0]) > int(
                                wta_master[tourney]['TwoSetList'][i][0]) and int(
                                wta_master[tourney]['OneSetList'][i][2]) > int(wta_master[tourney]['TwoSetList'][i][2])):
                                s = f' {round_name}: {wta_master[tourney]["PlayerOne"][i]} d. {wta_master[tourney]["PlayerTwo"][i]}: '
                                if wta_master[tourney]['OneSetList'][i][0]:
                                    s = s + f'{wta_master[tourney]["OneSetList"][i][0]}-{wta_master[tourney]["TwoSetList"][i][0]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][1]:
                                    s = s + f', {wta_master[tourney]["OneSetList"][i][1]}-{wta_master[tourney]["TwoSetList"][i][1]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][2]:
                                    s = s + f', {wta_master[tourney]["OneSetList"][i][2]}-{wta_master[tourney]["TwoSetList"][i][2]}'
                                else:
                                    pass
                                fins = fins + s + ' |' + wta_master[tourney]['Misc'][i]
                            else:
                                s = f' {round_name}: {wta_master[tourney]["PlayerTwo"][i]} d. {wta_master[tourney]["PlayerOne"][i]}: '
                                if wta_master[tourney]['OneSetList'][i][0]:
                                    s = s + f'{wta_master[tourney]["TwoSetList"][i][0]}-{wta_master[tourney]["OneSetList"][i][0]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][1]:
                                    s = s + f', {wta_master[tourney]["TwoSetList"][i][1]}-{wta_master[tourney]["OneSetList"][i][1]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][2]:
                                    s = s + f', {wta_master[tourney]["TwoSetList"][i][2]}-{wta_master[tourney]["OneSetList"][i][2]}'
                                else:
                                    pass
                                fins = fins + s + ' |' + wta_master[tourney]['Misc'][i]
                else:
                    if wta_master[tourney]['Status'][i] == 'Ongoing':
                        teama = f'{wta_master[tourney]["PlayerOne"][i]}'
                        teamb = f'{wta_master[tourney]["PlayerTwo"][i]}'
                        d = f' {round_name}: {teama} vs. {teamb}: '
                        if wta_master[tourney]['OneSetList'][i][0]:
                            d = d + f'{wta_master[tourney]["OneSetList"][i][0]}-{wta_master[tourney]["TwoSetList"][i][0]}'
                        else:
                            pass
                        if wta_master[tourney]['OneSetList'][i][1]:
                            d = d + f', {wta_master[tourney]["OneSetList"][i][1]}-{wta_master[tourney]["TwoSetList"][i][1]}'
                        else:
                            pass
                        if wta_master[tourney]['OneSetList'][i][2]:
                            d = d + f', {wta_master[tourney]["OneSetList"][i][2]}-{wta_master[tourney]["TwoSetList"][i][2]}'
                        else:
                            pass
                        if wta_master[tourney]['PointOne']:
                            d = d + f' {wta_master[tourney]["PointOne"][i]}-{wta_master[tourney]["PointTwo"][i]} '
                        else:
                            pass
                        ond = ond + d + ' |' + wta_master[tourney]['Misc'][i]
                    else:
                        if '' in wta_master[tourney]['OneSetList'][i]:
                            if (int(wta_master[tourney]['OneSetList'][i][0]) > int(
                                wta_master[tourney]['TwoSetList'][i][0]) and int(
                                wta_master[tourney]['OneSetList'][i][1]) > int(wta_master[tourney]['TwoSetList'][i][1])):
                                d = f' {round_name}: {wta_master[tourney]["PlayerOne"][i]} d. {wta_master[tourney]["PlayerTwo"][i]}: '
                                if wta_master[tourney]['OneSetList'][i][0]:
                                    d = d + f'{wta_master[tourney]["OneSetList"][i][0]}-{wta_master[tourney]["TwoSetList"][i][0]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][1]:
                                    d = d + f', {wta_master[tourney]["OneSetList"][i][1]}-{wta_master[tourney]["TwoSetList"][i][1]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][2]:
                                    d = d + f', {wta_master[tourney]["OneSetList"][i][2]}-{wta_master[tourney]["TwoSetList"][i][2]}'
                                else:
                                    pass
                                fin_d = fin_d + d + ' |' + wta_master[tourney]['Misc'][i]
                            else:
                                d = f' {round_name}: {wta_master[tourney]["PlayerTwo"][i]} d. {wta_master[tourney]["PlayerOne"][i]}: '
                                if wta_master[tourney]['OneSetList'][i][0]:
                                    d = d + f'{wta_master[tourney]["TwoSetList"][i][0]}-{wta_master[tourney]["OneSetList"][i][0]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][1]:
                                    d = d + f', {wta_master[tourney]["TwoSetList"][i][1]}-{wta_master[tourney]["OneSetList"][i][1]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][2]:
                                    d = d + f', {wta_master[tourney]["TwoSetList"][i][2]}-{wta_master[tourney]["OneSetList"][i][2]}'
                                else:
                                    pass
                                fin_d = fin_d + d + ' |' + wta_master[tourney]['Misc'][i]
                        else:
                            if (int(wta_master[tourney]['OneSetList'][i][0]) > int(
                                wta_master[tourney]['TwoSetList'][i][0]) and int(
                                wta_master[tourney]['OneSetList'][i][1]) > int(
                                wta_master[tourney]['TwoSetList'][i][1])) or (
                                int(wta_master[tourney]['OneSetList'][i][1]) > int(
                                wta_master[tourney]['TwoSetList'][i][1]) and int(
                                wta_master[tourney]['OneSetList'][i][2]) > int(
                                wta_master[tourney]['TwoSetList'][i][2])) or (
                                int(wta_master[tourney]['OneSetList'][i][0]) > int(
                                wta_master[tourney]['TwoSetList'][i][0]) and int(
                                wta_master[tourney]['OneSetList'][i][2]) > int(wta_master[tourney]['TwoSetList'][i][2])):
                                d = f' {round_name}: {wta_master[tourney]["PlayerOne"][i]} d. {wta_master[tourney]["PlayerTwo"][i]}: '
                                if wta_master[tourney]['OneSetList'][i][0]:
                                    d = d + f'{wta_master[tourney]["OneSetList"][i][0]}-{wta_master[tourney]["TwoSetList"][i][0]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][1]:
                                    d = d + f', {wta_master[tourney]["OneSetList"][i][1]}-{wta_master[tourney]["TwoSetList"][i][1]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][2]:
                                    d = d + f', {wta_master[tourney]["OneSetList"][i][2]}-{wta_master[tourney]["TwoSetList"][i][2]}'
                                else:
                                    pass
                                fin_d = fin_d + d + ' |' + wta_master[tourney]['Misc'][i]
                            else:
                                d = f' {round_name}: {wta_master[tourney]["PlayerTwo"][i]} d. {wta_master[tourney]["PlayerOne"][i]}: '
                                if wta_master[tourney]['OneSetList'][i][0]:
                                    d = d + f'{wta_master[tourney]["TwoSetList"][i][0]}-{wta_master[tourney]["OneSetList"][i][0]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][1]:
                                    d = d + f', {wta_master[tourney]["TwoSetList"][i][1]}-{wta_master[tourney]["OneSetList"][i][1]}'
                                else:
                                    pass
                                if wta_master[tourney]['OneSetList'][i][2]:
                                    d = d + f', {wta_master[tourney]["TwoSetList"][i][2]}-{wta_master[tourney]["OneSetList"][i][2]}'
                                else:
                                    pass
                                fin_d = fin_d + d + ' |' + wta_master[tourney]['Misc'][i]

                if 'doubles' in text:
                    final_string = f'{tourney}: |' + ond + fin_d
                else:
                    final_string = f'{tourney}: |' + ons + fins

            return final_string
