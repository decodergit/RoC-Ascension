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

print('''\subsection{Примеры расстановки во втором уровне Охоты за Сокровищами}

\\noindent
\\begin{longtable}{|c|c|c|}
    \\hline
    Битва & Вариант & Расстановка \\\\\\hline\\endhead''')

for fight in range(20, 41):
    screens = dict()
    total_images = 0
    for user_name in os.listdir(f'./Устав/parts/media/TreasureHunt/{fight}/'):
        screens[user_name] = os.listdir(f'./Устав/parts/media/TreasureHunt/{fight}/{user_name}/')
        total_images += len(screens[user_name])
    for user_name, images in zip(screens.keys(), screens.values()):
        if len(images) == 0:
            continue
        if len(images) == 1:
            print(f'''    {fight} & {user_names[user_name]} &
    \\includegraphics[width=0.5\\linewidth]{{./parts/media/TreasureHunt/{fight}/{user_name}/{images[0]}}} \\\\''')
        else:
            print(f'''    \multirow{{{total_images}}}{{*}}{{{fight}}} & {user_names[user_name]} &
    \\includegraphics[width=0.75\\linewidth]{{./parts/media/TreasureHunt/{fight}/{user_name}/{images[0]}}} \\\\''')
            for image in images[1:]:
                print(f'''    & {user_names[user_name]} &
    \\includegraphics[width=0.75\\linewidth]{{./parts/media/TreasureHunt/{fight}/{user_name}/{image}}} \\\\''')
        print('    \\hline')

print('\\end{longtable}')
