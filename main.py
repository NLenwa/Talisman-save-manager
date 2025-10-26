#import typer
import cmd
import os
import datetime, time, csv, shutil
from tabulate import tabulate
#app = typer.Typer()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


class Memory():
    appdata_path = os.getenv('APPDATA')
    memory_path = r'C:\Users\norbe\AppData\Roaming\Nomad Games\Talisman\saved_game'
    #memory_path = ''

    # [Save Name, [Players], Last Played Date, path]
    save_list = []

    save_list_headers = [
                            'id',
                            'Save Name',
                            'Player Count',
                            'Player names',
                            'Last Played',
                            'Save file'
                        ]
    
    last_action = ''

    def load_memory(self):
        self.save_path = os.path.join(self.appdata_path, 'Nomad Games', 'Talisman', 'saved_game')
        self.memory_path = os.path.join(self.appdata_path, 'Nomad Games', 'Talisman')
        rows = []
        try:
            with open(os.path.join(self.memory_path, 'save_manager_memory.csv'), mode='r') as f:
                csv_reader = csv.reader(f, delimiter=';')
                for row in csv_reader:
                    self.save_list.append(row)
            
            save_files = os.listdir(os.path.join(self.memory_path, 'Managed Saves'))
            
            for save in self.save_list:
                save_name = save[0]
                file_name = save[-1]
                if (save_name+'_'+file_name) not in save_files:
                    self.save_list.remove(save)
            self.update_last_action('Load memory', 'Save list read!')
        except:
            self.update_last_action('Load memory', 'No memory file found! File created')
            with open(os.path.join(self.memory_path, 'save_manager_memory.csv'), mode='w') as f:
                f.write('')

    def write_memory(self):
        with open(os.path.join(self.memory_path, 'save_manager_memory.csv'), mode='w', newline='') as f:
            csv_writer = csv.writer(f, delimiter=';')
            #for row in self.save_list:
            csv_writer.writerows(self.save_list)
            

    def add(self, save_name, players, date):
        os.makedirs(os.path.join(self.memory_path, 'Managed Saves'), exist_ok=True)
        files = os.listdir(self.save_path)
        file = [x for x in files if 'cloud' in x][0]
        shutil.copy2(os.path.join(self.save_path, file), os.path.join(self.memory_path, 'Managed Saves', f'{save_name}_'+file))
        self.save_list.append([save_name, len(players), players, date, file])

    def load_save(self, id):
        save_name = self.save_list[id][0]
        file = self.save_list[id][-1]
        shutil.copy2(os.path.join(self.memory_path, 'Managed Saves', f'{save_name}_'+file), os.path.join(self.save_path, file))
        

    def delete(self, id):
        #TODO delete save file
        save_name = self.save_list[id][0]
        file_name = self.save_list[id][-1]
        os.remove(os.path.join(self.memory_path, 'Managed Saves', save_name+'_'+file_name))
        del self.save_list[id]

    def update_save_path(self):
        path = input('Save Path is not defined. Provide Talisman game path: ')
        self.save_path = path

    def update_last_action(self, action, save_line):
        line = f'{action} - {save_line}'
        self.last_action = line



class SaveManagerCli(cmd.Cmd):
    user_name = str.capitalize(os.getenv('username'))
    intro = 'Welcome to Talisman Save Manage. Shall we start? [start/bye]'
    prompt = '<TSM> '
    file = None

    memory = Memory()


    def do_spath(self, arg):
        'Update Save Path'
        self.memory.update_save_path()
        self.memory.update_last_action('Update Save Path', '')
        self.do_update()

    def do_add(self, arg):
        'Add new save instance to memory'
        save_name, *players = input('Name Save and Players: ').split(' ')
        if save_name == 'None':
            return
        #TODO Get file to copy
        #TODO file = 
        #date = time.ctime(os.path.getmtime(file))
        date = "{:%d.%m.%Y %H:%M}".format(datetime.datetime.now())
        self.memory.add(save_name, players, date)
        self.memory.update_last_action('add', [save_name, players, date])
        self.do_update()

    def do_del(self, arg):
        'Remove save instance [id] from memory'
        id = input('Provide save id to DELETE: [integer/None]')
        if id == 'None':
            self.do_update()
            return
        else:
            try:
                id_int = int(id)
                save_name = self.memory.save_list[id_int][0]
                self.memory.delete(id_int)
                self.memory.update_last_action('del', save_name)
                self.do_update()
            except Exception as e:
                self.memory.update_last_action('del', 'Wrong input was given!')
                self.do_update()
                print(e)

    def do_load(self, arg):
        'Load save instance. This replaces currently used save file!'
        id = input('Provide save id to load [<integer>/None]: ')
        if id == 'None':
            return
        else:
            try:
                id_int = int(id)
                save_name = self.memory.save_list[id_int][0]
                check_input = input('Are you sure? [y/n]: ')
                if check_input == 'y':
                    self.memory.update_last_action('Load save', 'Save was loaded!')
                    self.memory.load_save(id_int)
                    self.do_update()
                else:
                    self.memory.update_last_action('Load save', 'Load was canceled!')
                    self.do_update()
                    return
            except Exception as e:
                self.memory.update_last_action('Load save', 'Wrong input was given!')
                self.do_update()
                print(e)

    def do_update(self):
        cls()
        print('----------------------------------------------------------------')
        print('----------------------------------------------------------------')
        print('SAVE MANAGER ——— TALISMAN: DIGITAL Classic Edition')
        print('by Lenwa, 2025')
        print('----------------------------------------------------------------')
        print('----------------------------------------------------------------')
        print('')
        print('Manage your saves:')
        print('')
        print(tabulate([[x] + self.memory.save_list[x] for x in range(len(self.memory.save_list))], self.memory.save_list_headers))
        print('')
        print('Write help or ? to display options :)')
        print('')
        print(f'Last action: {self.memory.last_action}')

    def do_bye(self, arg):
        'Close Talisman Save Manager'
        self.memory.write_memory()
        return True

    def do_start(self, arg):
        self.memory.load_memory()
        self.do_update()



if __name__ == "__main__":
    app = SaveManagerCli().cmdloop()
    
