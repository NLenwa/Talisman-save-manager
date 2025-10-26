#import typer
import cmd
import sys, os
import datetime, time
from tabulate import tabulate
#app = typer.Typer()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


class Memory():
    appdata_path = os.getenv('LOCALAPPDATA')
    save_path = r'C:\Users\norbe\AppData\Roaming\Nomad Games\Talisman\saved_game'

    # [Save Name, [Players], Last Played Date, path]
    save_list = [
        ['Save_name', 3, 'players', 'last_played'],
        ['Save_name', 3, 'players', 'last_played'],
        ['Save_name', 3, 'players', 'last_played'],
    ]

    save_list_headers = [
                            'id',
                            'Save Name',
                            'Player Count',
                            'Player names',
                            'Last Played',
                        ]
    
    last_action = ''

    def load_memory(self):
        self.appdata_path = ''
        self.save_list = ''

    def add(self, save_name, players, date):
        self.save_list.append([save_name, len(players), players, date])

    def delete(self, id):
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
        return True

    def do_start(self, arg):
        if self.memory.save_path == '':
            self.memory.update_save_path()
      
        if self.memory.save_path != '':
            self.do_update()



if __name__ == "__main__":
    app = SaveManagerCli().cmdloop()
    
