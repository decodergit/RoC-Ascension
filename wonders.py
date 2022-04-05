#!/bin/env python3

'''
Данная программа строит таблицы LaTeX Чудес Света на основании данных с сайта https://rise-of-cultures.fandom.com.
'''

import requests
from bs4 import BeautifulSoup
import math
import pprint


class Wonder:
    def __init__(self, name_en: str, name_ru: str):
        try:
            self.name_en = name_en
            self.name_ru = name_ru
            self.levels = dict()

            # Загрузка общей информации.
            r = requests.get(f'https://rise-of-cultures.fandom.com/wiki/World_Wonders/{self.name_en}')
            table = BeautifulSoup(r.content, 'html5lib').find('table', attrs={'class': 'article-table'})
            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                numbers = cells[3].text.strip().split(' ')
                if len(numbers) == 2 and numbers[0].isnumeric() and numbers[1].isnumeric():
                    level = {
                        'research':  int(numbers[0]),
                        'blueprint': int(numbers[1])
                    }
                else:
                    break
                self.levels[int(cells[2].text)] = level

            # Загрузка информации о наградах.
            r = requests.get('https://rise-of-cultures.fandom.com/wiki/World_Wonders/Contribution_Rewards')
            header = BeautifulSoup(r.content, 'html5lib').find('span', attrs={'id': self.name_en, 'class': 'mw-headline'})
            table = header.parent.findNext('table', attrs={'class': 'article-table'})
            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                level_id = int(cells[0].text)
                if level_id in self.levels:
                    prizes = []
                    pos_index = 1
                    for cell in cells[1:]:
                        numbers = cell.text.strip().split(' ')
                        prize = dict()
                        if len(numbers) == 2:
                            if numbers[0].isnumeric():
                                prize['research'] = int(numbers[0])
                                if numbers[1].isnumeric():
                                    prize['blueprint'] = int(numbers[1])
                        elif len(numbers) == 1:
                            if numbers[0].isnumeric():
                                prize['research'] = int(numbers[0])
                                prize['blueprint'] = 0
                        else:
                            break
                        if len(prize) > 0:
                            prize['position'] = pos_index
                            invest = math.ceil(self.levels[level_id]['research'] / (2**pos_index))
                            prize['invest'] = invest
                            prize['profit'] = prize['research'] / invest
                            pos_index += 1
                            prizes.append(prize)
                    if len(prizes):
                        self.levels[level_id]['prizes'] = prizes
        except:
            pass

    def __repr__(self):
        return f'{self.name_ru}:\n{pprint.pformat(self.levels)}'

    def latex(self):
        tex_table = f'\\subsubsection{{{self.name_ru}}}\n'
        try:
            tex_table += '''
\\begin{longtable}[c]{|c|c|c|c|c|c|c|c|}
    \\hline
    \\multirow{ 2}{*}{\\small Уровень} &
    \\multicolumn{2}{|c|}{\\small Нужно} &
    \\multirow{ 2}{*}{\\small Место} & 
    \\multirow{ 2}{*}{\\small Инвестиция} & 
    \\multicolumn{3}{|c|}{\\small Приз} \\\\\\cline{2-3}\\cline{6-8}
    &
    {\\small Колб} & 
    {\\small Чертежей} & 
    & &
    {\\small Колб} & 
    {\\small Чертежей} & 
    {\\small Профит}
    \\\\\\hline\\endhead
'''

            for level_id, level in zip(self.levels.keys(), self.levels.values()):
                prizes_quant = 1
                if 'prizes' in level:
                    prizes_quant = len(level["prizes"])
                tex_table += f'    \\multirow{{{prizes_quant}}}{{*}}{{{level_id}}} & \\multirow{{{prizes_quant}}}{{*}}{{{level["research"]}}} & \\multirow{{{prizes_quant}}}{{*}}{{{level["blueprint"]}}} & '
                if 'prizes' in level:
                    tex_table += f'1 & {level["prizes"][0]["invest"]} & {level["prizes"][0]["research"]} & {level["prizes"][0]["blueprint"]} & {level["prizes"][0]["profit"]:.2f}'
                    for index in range(1, len(level["prizes"])):
                        tex_table += f' \\\\\\cline{{4-8}}\n    & & & {index + 2} & {level["prizes"][index]["invest"]} & {level["prizes"][index]["research"]} & {level["prizes"][index]["blueprint"]} & {level["prizes"][index]["profit"]:.2f}'
                else:
                    tex_table += '& & & &'
                tex_table += ' \\\\\\hline\n'

            tex_table += '\\end{longtable}\n\n'
        except:
            pass
        return tex_table


print(Wonder('Stonehenge', 'Стоунхендж').latex())
print(Wonder('Hanging_Gardens', 'Висячие Сады').latex())
print(Wonder('Statue_of_Zeus', 'Статуя Зевса').latex())
print(Wonder('Temple_of_Artemis', 'Храм Артемиды').latex())
print(Wonder('Colosseum', 'Колизей').latex())
print(Wonder('Hagia_Sophia', 'Софийский Собор').latex())
print(Wonder('Palace_of_Aachen', 'Ахенский Дворец').latex())
