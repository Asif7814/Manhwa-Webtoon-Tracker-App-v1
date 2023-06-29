import csv

path = ''
user_file_decision = int(input('\nWhich file would you like to open? ([1] - Webtoon Tracker, [2] - Manhwa Tracker): '))

while user_file_decision < 1 or user_file_decision > 2:
    print('You did not choose from the given options (1 - 2)\n')
    user_file_decision = int(input('Which file would you like to open? ([1] - Webtoon Tracker, [2] - Manhwa Tracker): '))

if user_file_decision == 1: # Webtoon Tracker file
    path = 'C:\\Users\\ashad\\Documents\\python_programs\\practical_projects\\Manhwa-Webtoon-Tracker-App-v1\\webtoon_tracker.csv'
else:
    path = 'C:\\Users\\ashad\\Documents\\python_programs\\practical_projects\\Manhwa-Webtoon-Tracker-App-v1\\manhwa_tracker.csv'

def check_chapter_validity(chapter):
    if not chapter.isdigit(): 
        print('Your input must only contain numbers')
        return -1
    else:
        return chapter

def get_new_descriptions():
    descriptions = []
    user_choice = ''
    
    while user_choice != 'N':
        description = {'Title':'', 'Status':'', 'Current Chapter':'x', 'Latest Chapter':'', 'Release Days':'x', 'Author':'', 'Genres':[]}
        prompt_count = 0

        while prompt_count < len(description):
            title = input('Title: ')
            description.update({'Title':title})
            prompt_count+=1

            status_choice = int(input('Status (Input one of the following options: [1] Reading, [2] Caught Up, [3] On Hold, [4] Finished, [5] Plan To Read): '))

            while status_choice < 1 or status_choice > 5:
                print('You did not choose from the list of given options (1 - 5)') 
                status_choice = int(input('Status (Input one of the following options: [1] Reading, [2] Caught Up, [3] On Hold, [4] Finished, [5] Plan To Read): '))

            if status_choice == 5: 
                status = 'Plan To Read'
                prompt_count+=1 # temp sol'n only
            elif status_choice == 4:
                status = 'Finished'
                prompt_count+=1 # temp sol'n only
            elif status_choice >= 1:
                if status_choice == 3:
                    status = 'On Hold'
                elif status_choice == 2:
                    status = 'Caught Up'
                else:
                    status = 'Reading'

                current_ch = check_chapter_validity(input('Current Chapter: '))

                while current_ch == -1:
                    current_ch = check_chapter_validity(input('Current Chapter: '))
                    
                description.update({'Current Chapter':current_ch})
                prompt_count+=1

            latest_ch = check_chapter_validity(input('Latest Chapter: '))
                
            while latest_ch == -1:
                latest_ch = check_chapter_validity(input('Latest Chapter: '))
                
            description.update({'Latest Chapter':latest_ch})
            prompt_count+=1
                
            description.update({'Status':status})
            prompt_count+=1

            release_day_choice = int(input('Release Days ([0] Series Has Finished Publishing, [1] Sundays, [2] Mondays, [3] Tuesdays, [4] Wednesdays, [5] Thursdays, [6] Fridays, [7] Saturdays): '))

            while release_day_choice < 0 or release_day_choice > 7:
                print('You did not choose from the list of given options\n')
                release_day_choice = input('Release Days ([0] Series Has Finished Publishing, [1] Sundays, [2] Mondays, [3] Tuesdays, [4] Wednesdays, [5] Thursdays, [6] Fridays, [7] Saturdays): ')

            if release_day_choice == 0:
                release_day = 'x'
            elif release_day_choice == 1:
                release_day = 'Sundays'
            elif release_day_choice == 2:
                release_day = 'Mondays'
            elif release_day_choice == 3:
                release_day = 'Tuesdays'
            elif release_day_choice == 4:
                release_day = 'Wednesdays'
            elif release_day_choice == 5:
                release_day = 'Thursdays'
            elif release_day_choice == 6:
                release_day = 'Fridays'
            else:
                release_day = 'Saturdays'

            description.update({'Release Days':release_day})
            prompt_count+=1

            author = str(input('Author: '))
            description.update({'Author':author})
            prompt_count+=1

            genres = []
            genre = ''

            while genre != 'X':
                genre = input("Genre (add as many as you would like one at a time; enter 'X' to stop): ")
                
                if genre == 'X':
                    break

                genres.append(genre)
            
            description.update({'Genres':genres})
            prompt_count+=1

        print()
        descriptions.append(description)
        user_choice = input("Would you like to add another series to the list? ('Y' = Yes, 'N' = No): ").upper()
        print()

    return descriptions 

def add_new_series():
    new_series = get_new_descriptions()  

    with open(path, 'a', newline="") as file:
        csv_writer = csv.DictWriter(file, fieldnames=['Title','Status','Current Chapter','Latest Chapter','Release Days','Author','Genres'])

        csv_writer.writerows(new_series)

def read_file():
    with open(path, 'r') as file:
        csv_reader = csv.DictReader(file)

        def print_series():
            print('Titles:\n---------------------------')

            count_series = 0
            count_chapters = 0

            count_plan_to_read = 0
            count_finished = 0
            count_on_hold = 0
            count_caught_up = 0
            count_reading = 0

            for line in csv_reader:
                if 'Plan To Read' in line['Status']:
                    if count_plan_to_read == 0:
                        print('\nPlan To Read:')

                    print(line['Title'] + ' [' + line['Latest Chapter'] + ' Chapters]')
                    count_plan_to_read += 1
                elif 'On Hold' in line['Status']:
                    if count_on_hold == 0:
                        print('\nOn Hold:')
                
                    print(line['Title'] + ' [' + line['Latest Chapter'] + ' Chapters]')    
                    count_on_hold += 1 
                elif 'Finished' in line['Status']:
                    if count_finished == 0:
                        print('\nFinished:')
                
                    print(line['Title'] + ' [' + line['Latest Chapter'] + ' Chapters]')
                    count_chapters += int(line['Latest Chapter'])
                    count_finished += 1
                else:
                    if 'Caught Up' in line['Status']: 
                        if count_caught_up == 0:
                            print('\nCaught Up:')

                        count_caught_up += 1
                    else:
                        if count_reading == 0: 
                            print('\nReading:')

                        count_reading += 1
                    
                    print(line['Title'] + ' Chapter ' + line['Current Chapter'] + '/' + line['Latest Chapter'])
                    count_chapters += int(line['Current Chapter'])

            count_series = count_reading + count_caught_up + count_finished
            print('\n---------------------------')
            print(f'\nTotal Series Read: {count_series}')
            print(f'Total Chapters Read: {count_chapters}')
            
            stats_decision = str(input('\nWould you like to see more specific stats? (Y - Yes, N - No): ')).capitalize()
            
            if stats_decision == 'Y':
                print(f'\nTotal Reading: {count_reading}')
                print(f'Total Caught Up: {count_caught_up}')
                print(f'Total Finished: {count_finished}')
                print(f'Total On Hold: {count_on_hold}')
                print(f'Total Plan To Read: {count_plan_to_read}')

        def check_release_days():
            user_day = str(input('Day of the Week (Sundays, Mondays, Tuesdays, Wednesdays, Thursdays, Fridays, Saturdays): '))
            
            print('\n---------------------------')
            print(user_day + ':')

            count = 0
            for line in csv_reader:
                if user_day in line['Release Days']:
                    print(line['Title'])
                    count += 1
            
            print('\n---------------------------')
            print(f'\nTotal on {user_day}: {count}')
        
        def check_genres():
            user_genre = str(input('Genre: '))

            print('\n---------------------------')
            print(user_genre + ':')
            
            count = 0
            for line in csv_reader:
                if user_genre in line['Genres']:
                    print(line['Title'])
                    count += 1
            
            print(f'\nTotal {user_genre} Series: {count}')

        user_read_decision = int(input('What would you like to check? ([1] All Series, [2] Series by Release Day, [3] Series by Genre): '))
        
        while user_read_decision < 1 or user_read_decision > 5:
            print('Choose from the list of given options (1 - 5)\n')
            user_read_decision = int(input('What would you like to check? ([1] All Series, [2] Series by Release Day, [3] Series by Genre): '))

        print()

        if user_read_decision == 3:
            check_genres()
        elif user_read_decision == 2:
            check_release_days()
        else:
            print_series()

user_starting_decision = int(input('What would you like to do? ([1] Add Series, [2] Read Series File): '))

while user_starting_decision < 1 or user_starting_decision > 2:
    print('You did not choose from the given options (1 - 2)\n')
    user_starting_decision = int(input('What would you like to do? ([1] Add Series, [2] Read Series File): '))

if user_starting_decision == 1:
    add_new_series()
else:
    read_file()
