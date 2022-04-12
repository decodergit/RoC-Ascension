#!/bin/env python3

'''
Данная программа составляет сырую таблицу расстановки войск во втором уровне Охоты за Сокровищами.
'''

import os

user_names = {
    'alexey': 'Алексей',
    'decoder': 'decoder',
    'sargon': 'Sargon',
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

for fight in range(21, 40):
    print(f'\\hyperlink{{fight{fight}}}{{{fight}}}, ')
print('\\hyperlink{fight40}{40}.')

print('''
\\noindent
\\begin{longtable}{|c|c|c|}
    \\hline
    Битва & Вариант & Расстановка \\\\\\hline\\endhead''')

for fight in range(21, 41):
    #print(f'    \\hypertarget{{fight{fight}}}{{}}')
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
        if len(images) == 1:
            print(f'''    {fight} & {user_names[user_name]} &
    \\hypertarget{{fight{fight}}}{{\\includegraphics[width=0.5\\linewidth]{{./parts/media/TreasureHunt/{fight}/{user_name}/{images[0]}}}}} \\\\''')
        else:
            print(f'''    \multirow{{{total_images}}}{{*}}{{{fight}}} & {user_names[user_name]} &
    \\hypertarget{{fight{fight}}}{{\\includegraphics[width=0.75\\linewidth]{{./parts/media/TreasureHunt/{fight}/{user_name}/{images[0]}}}}} \\\\''')
            for image in images[1:]:
                print(f'''    & {user_names[user_name]} &
    \\includegraphics[width=0.75\\linewidth]{{./parts/media/TreasureHunt/{fight}/{user_name}/{image}}} \\\\''')
        print('    \\hline')

print('\\end{longtable}')

print('\n\n\n\n\n\n\nНе хватает скриншотов (битва: есть/нужно):\n')
for user_name in no_screens.keys():
    if len(no_screens[user_name]) > 0:
        print(f'{user_names[user_name]}:')
        for line in no_screens[user_name]:
            print(line)
        print('')
