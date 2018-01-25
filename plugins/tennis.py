# coding: utf-8

from datetime import datetime

import requests

from cloudbot import hook


@hook.command("scores", "tennis", "game", "match")
def scores(text):

    now = datetime.now()
    if now.month < 10:
        month = f'0{now.month}'
    else:
        month = f'{now.month}'

    day = now.day
    if 'yesterday' or 'y' in text:
        day = now.day - 1

    date_string = f'{now.year}-{month}-{day}'
    time_string = f'{now.hour}{now.minute}{now.second}'

    url = f'http://ace.tennis.com/pulse/{date_string}_livescores_new.json?v={time_string}'
    scores_json = requests.get(url).json()

    tournaments = scores_json['tournaments']
    results = []

    for tournament in tournaments:
        tournament_data = {}
        name = tournament['name']
        if 'Boys' in name:
            continue
        elif 'Girls' in name:
            continue
        matches = tournament['events']
        city = tournament['location']
        country = tournament['country']
        gender = tournament['gender']
        match_names = []
        for match in matches:
            match_data = {}
            teams = []
            round_title = match['round']
            players = match['players']

            for player in players:
                team_data = {}

                player_name = player['name']
                if player['is_serving']:
                    player_name += "*"
                team_data['player_name'] = player_name

                set_score_list = player['set_games']
                team_data['set_score_list'] = set_score_list
                team_data['winner'] = player['is_winner']
                teams.append(team_data)

            match_data['status'] = match['status']
            match_data['team_data'] = teams
            match_data['round'] = round_title
            match_names.append(match_data)

        tournament_data['name'] = name
        tournament_data['city'] = city
        tournament_data['country'] = country
        tournament_data['gender'] = gender
        tournament_data['match_data'] = match_names
        results.append(tournament_data)

    if results:
        final_mstring = ''
        final_wstring = ''
        final_cmstring = ''
        final_cwstring = ''
        for tourney in results:
            tourney_type = ''
            if tourney['gender'] == 'male' and 'Challenger' not in tourney['name']:
                final_m = f'{tourney["name"]} ({tourney["city"]}, {tourney["country"]}): '
                nsm = ''
                om = ''
                fm = ''
                tourney_type = 'a'
            elif tourney['gender'] == 'female' and 'Challenger' not in tourney['name']:
                final_w = f'{tourney["name"]} ({tourney["city"]}, {tourney["country"]}): '
                nsw = ''
                ow = ''
                fw = ''
                tourney_type = 'w'
            elif tourney['gender'] == 'male' and 'Challenger' in tourney['name']:
                final_cm = f'{tourney["name"]} ({tourney["city"]}, {tourney["country"]}): '
                nscm = ''
                ocm = ''
                fcm = ''
                tourney_type = 'cm'
            elif tourney['gender'] == 'female' and 'Challenger' in tourney['name']:
                final_cw = f'{tourney["name"]} ({tourney["city"]}, {tourney["country"]}): '
                nscw = ''
                ocw = ''
                fcw = ''
                tourney_type = 'cw'
            for match in tourney['match_data']:
                first_name = match['team_data'][0]['player_name']
                first_set_num = match['team_data'][0]['set_score_list']
                second_name = match['team_data'][1]['player_name']
                second_set_num = match['team_data'][1]['set_score_list']
                round_name = match['round']
                if match['status'] == 'Not started':
                    s = f'| {round_name}: {first_name} vs. {second_name} '
                    if tourney_type == 'a':
                        nsm = nsm + s
                    elif tourney_type == 'w':
                        nsw = nsw + s
                    elif tourney_type == 'cm':
                        nscm = nscm + s
                    elif tourney_type == 'cw':
                        nscw = nscw + s
                elif match['status'] == 'Finished':
                    if match['team_data'][0]['winner']:
                        s = f'| {round_name}: {first_name} d. {second_name}: {first_set_num[0]}-{second_set_num[0]}'
                        try:
                            s = s + f', {first_set_num[1]}-{second_set_num[1]}'
                        except IndexError:
                            pass
                        try:
                            s = s + f', {first_set_num[2]}-{second_set_num[2]}'
                        except IndexError:
                            pass
                        try:
                            s = s + f', {first_set_num[3]}-{second_set_num[3]}'
                        except IndexError:
                            pass
                        try:
                            s = s + f', {first_set_num[4]}-{second_set_num[4]}'
                        except IndexError:
                            pass
                    else:
                        s = f'| {round_name}: {second_name} d. {first_name}: {second_set_num[0]}-{first_set_num[0]}'
                        try:
                            s = s + f', {second_set_num[1]}-{first_set_num[1]}'
                        except IndexError:
                            pass
                        try:
                            s = s + f', {second_set_num[2]}-{first_set_num[2]}'
                        except IndexError:
                            pass
                        try:
                            s = s + f', {second_set_num[3]}-{first_set_num[3]}'
                        except IndexError:
                            pass
                        try:
                            s = s + f', {second_set_num[4]}-{first_set_num[4]}'
                        except IndexError:
                            pass
                    s = s + ' '
                    if tourney_type == 'a':
                        fm = fm + s
                    elif tourney_type == 'w':
                        fw = fw + s
                    elif tourney_type == 'cm':
                        fcm = fcm + s
                    elif tourney_type == 'cw':
                        fcw = fcw + s
                else:
                    try:
                        s = f'| {first_name} vs. {second_name}: {first_set_num[0]}-{second_set_num[0]}'
                    except IndexError:
                        s = f'| {first_name} vs. {second_name}: 0-0'
                    try:
                        s = s + f', {first_set_num[1]}-{second_set_num[1]}'
                    except IndexError:
                        pass
                    try:
                        s = s + f', {first_set_num[2]}-{second_set_num[2]}'
                    except IndexError:
                        pass
                    try:
                        s = s + f', {first_set_num[3]}-{second_set_num[3]}'
                    except IndexError:
                        pass
                    try:
                        s = s + f', {first_set_num[4]}-{second_set_num[4]}'
                    except IndexError:
                        pass
                    # m = m + f' {first_game_score}-{second_game_score} '
                    s = s + ' '
                    if tourney_type == 'a':
                        om = om + s
                    elif tourney_type == 'w':
                        ow = ow + s
                    elif tourney_type == 'cm':
                        ocm = ocm + s
                    elif tourney_type == 'cw':
                        ocw = ocw + s

            if tourney_type == 'a':
                final_m = final_m + om + nsm + fm
                final_mstring = final_mstring + final_m + '\n'
            elif tourney_type == 'w':
                final_w = final_w + ow + nsw + fw
                final_wstring = final_wstring + final_w + '\n'
            elif tourney_type == 'cm':
                final_cm = final_cm + ocm + nscm + fcm
                final_cmstring = final_cmstring + final_cm + '\n'
            elif tourney_type == 'cw':
                final_cw = final_cw + ocw + nscw + fcw
                final_cwstring = final_cwstring + final_cw + '\n'

        if 'atp' in text.lower():
            return final_mstring
        elif 'wta' in text.lower():
            return final_wstring
        elif 'cm' in text.lower():
            return final_cmstring
        elif 'cw' in text.lower():
            return final_cwstring
        else:
            return"Please pick a valid tour (ATP, WTA, CM (Men's Challenger), or CW (Women's Challenger))."
