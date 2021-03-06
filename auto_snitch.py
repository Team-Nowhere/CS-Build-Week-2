from endpoints import *
from main_functions import *
import os
import subprocess
import argparse
import time

parser = argparse.ArgumentParser(description='Snitch Locator')
parser.add_argument('--snitches')
args = parser.parse_args()

want = int(args.snitches)

os.system('pipenv shell')

current_room = get_current_room()

# Cooldown penalty check
if current_room['errors'] is not None and len(current_room['errors']) > 0:
    print('\n!!!! Cooldown Penalty !!!!')
    cooldown(current_room)
    print('Getting current room id...')
    current_room = get_current_room()
    cooldown(current_room)
else:
    print('Getting current room id...')
    cooldown(current_room)

if int(current_room["room_id"]) != 555:
    os.system('python fast_travel.py --room 555')


def well_number():
    data = examine('Well')
    time.sleep(data['cooldown'])
    desc = data['description']

    desc = desc.strip('You see a faint pattern in the water...\n\n').split('\n')

    with open('well_data.txt', 'w') as data:
        for i in desc:
            data.write(f'{i}\n')

    time.sleep(2)
    cmd = ['python', 'ls8.py', 'well_data.txt']


    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    output = output.decode('utf-8').replace('\n', '').split(' ')[-3]
    snitch_room = output.rstrip('HALTING')

    return snitch_room, data




captured = 0
wait_for_snitch = False

# Get abilities
status_res = status()
print('\nGetting abilities...')
cooldown(status_res)
tries = 0
while captured < want:
    # Examine the well
    start_snitch, data = well_number()
    new_num = start_snitch
    camp_wait = 0

    print('\nCamping for 60 iterations')

    while new_num == start_snitch and camp_wait < 60:
        new_num, data = well_number()
        camp_wait += 1

    tries += 1
    print(f'\nSnitch located in room {new_num}\n')

    run_script = f'python fast_travel.py --room {new_num}'
    if status_res['abilities']:
        run_script += ' --abilities'
        for ability in status_res['abilities']:
            run_script += f' {ability}'
    
    run_script += f' --start_room 555'

    os.system(run_script)


    take_res = take('golden snitch')
    cooldown(take_res)
    if not take_res['errors']:
        if take_res['messages']:
            if 'warmth' in take_res['messages'][0]:
                print('''
>!!!!!!!!!!!!!!!!!!!!!!!<
>!!!                 !!!<
>!!! Snitch Captured !!!<
>!!!                 !!!<
>!!!!!!!!!!!!!!!!!!!!!!!<
                ''')

                captured += 1
                wait_for_snitch = False
            else:
                print('\nThere is no snitch here\n')
                wait_for_snitch = True

    print(f'\nSnitches Captured: {captured} out of {tries}\n')

    run_script = 'python fast_travel.py --room 555'
    if status_res['abilities']:
        run_script += ' --abilities'
        for ability in status_res['abilities']:
            run_script += f' {ability}'

    run_script += f' --start_room {new_num}'
        
    os.system(run_script)



