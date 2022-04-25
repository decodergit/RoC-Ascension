#!/bin/env python3

'''
Данная программа составляет сырую таблицу расстановки войск во втором уровне Охоты за Сокровищами.
'''

import os

user_names = {
    'alexey': 'Алексей',
    'decoder': 'decoder',
    'sargon': 'Sargon',
    'Preyton': 'Preyton'
}

two_waves = {25, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40}
no_screens = dict()
for user_name in user_names.keys():
    no_screens[user_name] = []

print('''\subsection{Примеры расстановки во втором уровне Охоты за Сокровищами}

В целях обучения можно посмотреть
\\underline{\href{https://youtu.be/JD1PWm27lHg}{видео}}
о прохождении первого уровня Охоты за Сокровищами.

Ниже представлены примеры расстановки войск, собранные нашим Альянсом:''')

for fight in range(21, 41):
    print(f'\\hyperlink{{fight{fight}}}{{{fight}}}, ')

for fight in range(21, 41):
    screens = dict()
    total_images = 0
    for user_name in os.listdir(f'./Устав/parts/media/TreasureHunt/{fight}/'):
        screens[user_name] = os.listdir(f'./Устав/parts/media/TreasureHunt/{fight}/{user_name}/')
        total_images += len(screens[user_name])
    for user_name, images in zip(screens.keys(), screens.values()):
        if fight in two_waves:
            needed_screens = 4
        else:
            needed_screens = 2
        if len(images) < needed_screens:
            no_screens[user_name].append(f'{fight}: {len(images)}/{needed_screens}')
        if len(images) == 0:
            continue
        print(f'''
\\newpage
\\begin{{center}}
    \\hypertarget{{fight{fight}}}{{\\textbf{{Битва {fight} ({user_names[user_name]}).}}}}
\\end{{center}}''')
        for image in images:
                print(f'\\noindent\\includegraphics[width=\\linewidth]{{./parts/media/TreasureHunt/{fight}/{user_name}/{image}}} \\newline')

print('\n\n\n\n\n\n\nНе хватает скриншотов (битва: есть/нужно):\n')
for user_name in no_screens.keys():
    if len(no_screens[user_name]) > 0:
        print(f'{user_names[user_name]}:')
        for line in no_screens[user_name]:
            print(line)
        print('')
