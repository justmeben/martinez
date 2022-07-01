from datetime import datetime as dt
import calendar
import json
from typing import Dict

import requests
from bs4 import BeautifulSoup

DOMAIN_NAME = 'https://the-mafia.net'
BASE_URL = f'{DOMAIN_NAME}/?q=rate%2Fnightfall-premier-league-2022'
DATE_URL_TEMPLATE = '&date_from[date]=%(dfrom)s&date_to[date]=%(dto)s'
DATA_FILE = 'mafia_data.json'


class MafiaDataCollector:
    roles = ('citizen', 'mafia', 'sheriff', 'don')

    def __init__(self):
        self.base_url = BASE_URL
        self.date_url_template = DATE_URL_TEMPLATE
        self.last_month = dt.now().month
        self.league_year = dt.now().year

    def _fetch_one_month_html(self, month_number):
        start_date = f'{self.league_year}-{month_number}-1'
        end_date_day = calendar.monthrange(self.league_year, month_number)[1]
        end_date = f'{self.league_year}-{month_number}-{end_date_day}'
        formatted_url = self.base_url + self.date_url_template % {'dfrom': start_date, 'dto': end_date}
        resp = requests.get(formatted_url)
        return resp.content.decode()

    def _fetch_upto_month_html(self, month_number):
        start_date = f'{self.league_year}-1-1'
        end_date_day = calendar.monthrange(self.league_year, month_number)[1]
        end_date = f'{self.league_year}-{month_number}-{end_date_day}'
        formatted_url = self.base_url + self.date_url_template % {'dfrom': start_date, 'dto': end_date}
        resp = requests.get(formatted_url)
        return resp.content.decode()

    @classmethod
    def _parse_player_soup(cls, player: BeautifulSoup) -> Dict:
        """
        EDIT this function if the mafia website changes
        :param player: BeautifulSoup instance of a player
        :return: formatted dict of player stats
        """
        cols = player.find_all('td')
        try:
            parsed_player = {
                'games_url': DOMAIN_NAME + cols[1].find_all('a')[1].attrs['href'],
                'username': cols[1].find('a').attrs['href'].split('/')[2],
                'name': cols[1].find('a').text,
                'total_points': int(cols[2].text),
                'bonus_points': float(cols[3].text),
                'total_games': int(cols[4].text),
                'total_games_wins': int(cols[5].text.split('(')[0]),
                'citizen_games_wins': int(cols[10].text.split('/')[0]),
                'citizen_games_loses': int(cols[10].text.split('/')[1].split(' ')[0]),
                'mafia_games_wins': int(cols[11].text.split('/')[0]),
                'mafia_games_loses': int(cols[11].text.split('/')[1].split(' ')[0]),
                'sheriff_games_wins': int(cols[12].text.split('/')[0]),
                'sheriff_games_loses': int(cols[12].text.split('/')[1].split(' ')[0]),
                'don_games_wins': int(cols[13].text.split('/')[0]),
                'don_games_loses': int(cols[13].text.split('/')[1].split(' ')[0]),
            }
        except IndexError:
            return {}
        parsed_player['total_games_winrate'] = 100 * float(parsed_player['total_games_wins']) / float(parsed_player['total_games']) \
            if float(parsed_player['total_games']) != 0 else None
        parsed_player[f'total_games_loses'] = parsed_player[f'total_games'] - parsed_player[f'total_games_wins']
        for role in cls.roles:
            parsed_player[f'{role}_games'] = parsed_player[f'{role}_games_wins'] + parsed_player[f'{role}_games_loses']
            parsed_player[f'{role}_games_winrate'] = 100 * float(parsed_player[f'{role}_games_wins']) / float(parsed_player[f'{role}_games']) \
                if float(parsed_player[f'{role}_games']) != 0 else None

        return parsed_player

    def _html_data_to_json(self, html_data):
        soup = BeautifulSoup(html_data, features="html.parser")
        players = soup.find_all('tr')
        return {self._parse_player_soup(player)['username']: self._parse_player_soup(player)
                for player in players[1:]}

    def fetch_all_data(self):
        month = 1
        single_month_data = {}
        upto_month_data = {}
        while month <= self.last_month:
            print(f'Working on month {month}')
            single_month_data[month] = self._html_data_to_json(self._fetch_one_month_html(month))
            upto_month_data[month] = self._html_data_to_json(self._fetch_upto_month_html(month))
            month += 1

        return {'single_month_data': single_month_data, 'upto_month_data': upto_month_data}


if __name__ == '__main__':
    collector = MafiaDataCollector()
    data = collector.fetch_all_data()
    with open(DATA_FILE, 'w') as fh:
        fh.write(json.dumps(data))


