import curses
from apps import Program

class Option:
    def __init__(self, program: Program) -> None:
        self.program = program
    
    def print(self, stdscr, pos, is_focused):
        checkbox = "[X]" if self.program.download_needed else "[ ]"
        y, x = pos
        if is_focused:
            stdscr.addstr(y, x, f"{checkbox} {self.program.name}", curses.A_REVERSE | curses.color_pair(1))
        else:
            stdscr.addstr(y, x, f"{checkbox} {self.program.name}")
            
    def toggle(self):
        self.program.download_needed = not self.program.download_needed

class Window:
    def __init__(self) -> None:
        self.__categories: dict[str, list[Option]] = {}
        self.selected_category = 0
        self.focused_option = 0
        self.download_mode = 0
        self.selected_count = 0
        
    def start(self):
        curses.wrapper(self.__start)
        abort = False
        if (self.download_mode):
            c = 0
            for category in self.__categories.keys():
                if abort:
                    break
                for option in self.__categories[category]:
                    program = option.program
                    if program.download_needed:
                        c+=1
                        if self.download_mode == 1:
                            if option.program.install((c, self.selected_count)) < 0: return
                        elif self.download_mode == 2:
                            if option.program.download((c, self.selected_count)) < 0:
                                return
                            #app_list[option.program.name] = status
                            #if option.program.download((c, self.selected_count)) < 0: return
              
    def __start(self, stdscr):
        curses.curs_set(0)  # Desliga o cursor
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLUE, -1)
        stdscr.clear()
        
        min_height, min_width = 10, 90  # Altura e largura mínima da janela
        
        while True:
            h, w = stdscr.getmaxyx()
            stdscr.clear()

            if h < min_height or w < min_width:
                stdscr.addstr(0, 0, f"Por favor, aumente o tamanho da janela para pelo menos {min_width}x{min_height}.")
                stdscr.refresh()
                stdscr.getch()
                continue
            stdscr.addstr(0, 0, f"Número de Apps Selecionadas: {self.selected_count}")
            
            # Exibe as categorias na tela
            for i, category in enumerate(self.__categories):
                y = i + 2
                if i == self.selected_category:
                    stdscr.addstr(y, 1, f"> {category}", curses.A_BOLD | curses.color_pair(1))
                else:
                    stdscr.addstr(y, 1, f" {category}")
            
            if self.selected_category == len(self.__categories):
                stdscr.addstr(len(self.__categories)+2, 1, f"> Download and Install", curses.A_BOLD | curses.color_pair(1))
            else:
                stdscr.addstr(len(self.__categories)+2, 1, f" Download and Install")
            if self.selected_category == len(self.__categories) + 1:
                stdscr.addstr(len(self.__categories)+3, 1, f"> Download Only", curses.A_BOLD | curses.color_pair(1))
            else:
                stdscr.addstr(len(self.__categories)+3, 1, f" Download Only")

            stdscr.refresh()
            key = stdscr.getch()

            # Navegação entre as categorias
            if key == curses.KEY_UP:
                self.selected_category = max(0, self.selected_category - 1)
                self.focused_option = 0  # Reinicia a seleção de opções ao mudar de categoria
            elif key == curses.KEY_DOWN:
                self.selected_category = min(len(self.__categories)+1, self.selected_category + 1)
                self.focused_option = 0  # Reinicia a seleção de opções ao mudar de categoria
            elif key == ord('q'):
                break
            elif key == ord(' ') or key == curses.KEY_ENTER or key in [10, 13]:
                # Expande a categoria selecionada para exibir os programas
                if self.selected_category < len(self.__categories):
                    selected_category = list(self.__categories.keys())[self.selected_category]
                    self.__show_category_programs(stdscr, selected_category)
                else:
                    if (self.selected_category == len(self.__categories)):
                        self.download_mode = 1
                    elif(self.selected_category == len(self.__categories)+1):
                        self.download_mode = 2
                    break
                    
        stdscr.clear()
        stdscr.refresh()

    def add_program(self, program: Program):
        category = program.category
        if category not in self.__categories:
            self.__categories[category] = []
        self.__categories[category].append(Option(program))

    def __show_category_programs(self, stdscr, category):
        stdscr.clear()
        programs = sorted(self.__categories[category], key=lambda item: item.program.name)
        
        min_height, min_width = 10, 90  # Altura e largura mínima da janela
        
        while True:
            h, w = stdscr.getmaxyx()
            stdscr.clear()
            
            if h < min_height or w < min_width:
                stdscr.addstr(0, 0, f"Por favor, aumente o tamanho da janela para pelo menos {min_width}x{min_height}.")
                stdscr.refresh()
                stdscr.getch()
                continue
            
            stdscr.addstr(0, 0, f"Categoria: {category}", curses.A_BOLD)
            
            max_col = max(1, (w // 30))  # Limita o número de colunas com uma largura mínima de 30
            col_width = w // max_col
            
            stdscr.addstr(1, 1, "["+ ("X" if all(option.program.download_needed for option in programs) else " ")+"] Selecionar Todos", (curses.A_REVERSE | curses.color_pair(1))  if self.focused_option == 0 else curses.A_NORMAL)
            
            for i, option in enumerate(programs):
                col_number = i % max_col
                row_number = i // max_col
                x = 1 + col_number * col_width
                y = row_number + 2 + 1  # +1 para compensar a linha da opção "Selecionar Todos"
                option.print(stdscr, (y, x), i == (self.focused_option - 1))

            #stdscr.addstr(h - 1, 0, "Use as setas para mover, Espaço para marcar/desmarcar, Q para voltar.")
            stdscr.refresh()
            
            key = stdscr.getch()

            # Navegação entre as opções
            if key == curses.KEY_UP:
                if self.focused_option == 0:
                    self.focused_option = max(0, self.focused_option - 1)
                else:
                    self.focused_option = max(0, self.focused_option - max_col)
            elif key == curses.KEY_DOWN:
                if self.focused_option == 0:
                    self.focused_option = min(len(programs), self.focused_option + 1)
                else:
                    self.focused_option = min(len(programs), self.focused_option + max_col)
            elif key == curses.KEY_LEFT:
                self.focused_option = max(0, self.focused_option - 1)
            elif key == curses.KEY_RIGHT:
                self.focused_option = min(len(programs), self.focused_option + 1)
            elif key == ord('q'):
                break
            elif key == ord(' ') or key == curses.KEY_ENTER or key in [10, 13]:
                if self.focused_option == 0:
                    all_selected = all(option.program.download_needed for option in programs)
                    for option in programs:
                        if (all_selected):
                            self.selected_count -= 1
                        elif (not option.program.download_needed):
                            self.selected_count += 1
                        option.program.download_needed = not all_selected
                else:
                    programs[self.focused_option - 1].program.download_needed = not programs[self.focused_option - 1].program.download_needed
                    if (programs[self.focused_option - 1].program.download_needed):
                        self.selected_count +=1
                    else:
                        self.selected_count -= 1
