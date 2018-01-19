import requests
from cloudbot import hook


@hook.command("atp")
def atp_scores(text):

    url = "http://www.atpworldtour.com/en/-/ajax/Scores/GetInitialScores"
    scores_json = requests.get(url).json()

    nbsp = "&nbsp;"
    team_keys = ['TeamOne', 'TeamTwo']
    set_key_names = ['SetOne', 'SetTwo', 'SetThree', 'SetFour', 'SetFive']

    tournaments = scores_json['liveScores']['Tournaments']
    results = []

    for tournament in tournaments:
        tournament_data = {}
        matches = tournament['Matches']
        name = tournament['Name']
        place = tournament['Location']
        match_names = []

        for match in matches:
            match_data = {}
            teams = []
            round_title = str(match['RoundTitle'])

            for team_name in team_keys:
                team_data = {}

                player_name = match[team_name]['PlayerOneName']
                if match[team_name]['PlayerTwoName'].strip():
                    player_name += " / " + match[team_name]['PlayerTwoName']
                if match[team_name]['TeamStatus'] == "now-serving":
                    player_name += "*"
                team_data['player_name'] = player_name

                score_string = ""
                set_score_list = []
                for set_name in set_key_names:
                    if set_name in match[team_name]['Scores'] and match[team_name]['Scores'][set_name] != nbsp:
                        score_string += match[team_name]['Scores'][set_name]
                        try:
                            set_score_list.append(int(match[team_name]['Scores'][set_name]))
                        except ValueError:
                            continue

                    score_string += " "

                if "CurrentScore" in match[team_name]['Scores'] and match[team_name]['Scores']['CurrentScore'] != nbsp:
                    score_string += match[team_name]['Scores']["CurrentScore"]

                team_data['score'] = score_string
                team_data['set_score_list'] = set_score_list
                teams.append(team_data)


            match_data['status'] = match['Status']
            match_data['info'] = match['MatchInfo']
            match_data['team_data'] = teams
            match_data['round'] = round_title
            match_names.append(match_data)

        tournament_data['name'] = name
        tournament_data['place'] = place
        tournament_data['match_data'] = match_names
        results.append(tournament_data)

    if results:
        for tourney in results:
            final_string = f'{tourney["name"]} ({tourney["place"]}): '
            final_s = ''
            final_d = ''
            for match in tourney['match_data']:
                first_name = ' '.join(str(match['team_data'][0]['player_name']).split())
                first_set_num = match['team_data'][0]['set_score_list']
                first_game_score = match['team_data'][0]['score'][-2:].replace(' ', '')
                second_name = ' '.join(str(match['team_data'][1]['player_name']).split())
                second_set_num = match['team_data'][1]['set_score_list']
                second_game_score = match['team_data'][1]['score'][-2:].replace(' ', '')
                round_name = match['round']
                if '/' in first_name:
                    if match['status'] == 'F':
                        if 'Walkover' in match['info']:
                            if first_name.upper().split()[1] in match['info']:
                                d = f'| {round_name}: {first_name} d. {second_name}: w/o'
                            else:
                                d = f'| {round_name}: {second_name} d. {first_name}: w/o'
                        elif (first_set_num[0] > second_set_num[0] and first_set_num[1] > second_set_num[1]) or (
                            first_set_num[1] > second_set_num[1] and first_set_num[2] > second_set_num[2]) or (
                            first_set_num[0] > second_set_num[0] and first_set_num[2] > second_set_num[2]):
                            d = f'| {round_name}: {first_name} d. {second_name}: {first_set_num[0]}-{second_set_num[0]}'
                            try:
                                d = d + f', {first_set_num[1]}-{second_set_num[1]}'
                            except IndexError:
                                pass
                            try:
                                d = d + f', {first_set_num[2]}-{second_set_num[2]}'
                            except IndexError:
                                pass
                            try:
                                d = d + f', {first_set_num[3]}-{second_set_num[3]}'
                            except IndexError:
                                pass
                            try:
                                d = d + f', {first_set_num[4]}-{second_set_num[4]}'
                            except IndexError:
                                pass
                        else:
                            d = f'| {round_name}: {second_name} d. {first_name}: {second_set_num[0]}-{first_set_num[0]}'
                            try:
                                d = d + f', {second_set_num[1]}-{first_set_num[1]}'
                            except IndexError:
                                pass
                            try:
                                d = d + f', {second_set_num[2]}-{first_set_num[2]}'
                            except IndexError:
                                pass
                            try:
                                d = d + f', {second_set_num[3]}-{first_set_num[3]}'
                            except IndexError:
                                pass
                            try:
                                d = d + f', {second_set_num[4]}-{first_set_num[4]}'
                            except IndexError:
                                pass
                        d = d + ' '
                    else:
                        d = f'| {first_name} vs. {second_name}: {first_set_num[0]}-{second_set_num[0]}'
                        try:
                            d = d + f', {first_set_num[1]}-{second_set_num[1]}'
                        except IndexError:
                            pass
                        try:
                            d = d + f', {first_set_num[2]}-{second_set_num[2]}'
                        except IndexError:
                            pass
                        try:
                            d = d + f', {first_set_num[3]}-{second_set_num[3]}'
                        except IndexError:
                            pass
                        try:
                            d = d + f', {first_set_num[4]}-{second_set_num[4]}'
                        except IndexError:
                            pass
                        d = d + f' {first_game_score}-{second_game_score} '
                    final_d = final_d + d
                else:
                    if match['status'] == 'F':
                        if 'Walkover' in match['info']:
                            if first_name.upper().split()[1] in match['info']:
                                s = f'| {round_name}: {first_name} d. {second_name}: w/o'
                            else:
                                s = f'| {round_name}: {second_name} d. {first_name}: w/o'
                        elif (first_set_num[0] > second_set_num[0] and first_set_num[1] > second_set_num[1]) or (
                            first_set_num[1] > second_set_num[1] and first_set_num[2] > second_set_num[2]) or (
                            first_set_num[0] > second_set_num[0] and first_set_num[2] > second_set_num[2]):
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
                    else:
                        s = f'| {round_name}: {first_name} vs. {second_name}: {first_set_num[0]}-{second_set_num[0]}'
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
                        s = s + f' {first_game_score}-{second_game_score} '
                    final_s = final_s + s

            if 'doubles' in text:
                final_string = final_string + final_d
            else:
                final_string = final_string + final_s

            return final_string
