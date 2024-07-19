from abc import ABC, abstractmethod
import requests
import re
import sys
from tqdm import tqdm
import winreg
import os
import winpty
import time

def get_downloads_path():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
        downloads_path = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
        return os.path.expandvars(downloads_path+"\\Installers")
    except Exception:
        return "C:\\Installers"
    

download_path = get_downloads_path()

def get_size(string):
    # Padrão para detectar MB, GB e KB
    pattern = r"(\d+(\.\d+)?)\s*(M|G|K)B\s*/\s*(\d+(\.\d+)?)\s*(M|G|K)B"

    matches = re.search(pattern, string)
    if matches:
        f1_value = float(matches.group(1))
        f1_unit = matches.group(3)
        f2_value = float(matches.group(4))
        f2_unit = matches.group(6)

        # Convertendo KB, MB e GB para MB
        unit_to_mb = {'K': 1/1024, 'M': 1, 'G': 1024}
        
        if f1_unit in unit_to_mb:
            f1_value *= unit_to_mb[f1_unit]
        
        if f2_unit in unit_to_mb:
            f2_value *= unit_to_mb[f2_unit]

        return f1_value, f2_value
    else:
        return -1, -1

    

class Program(ABC):
    def __init__(self, name: str, category: str) -> None:
        self.name = name
        self.category = category
        self.download_needed = False
        
    @abstractmethod 
    def install(self):
        pass
    
    @abstractmethod 
    def download(self, count: tuple) -> int:
        pass

class WinGet_Program(Program):
    def __init__(self, name: str, package_name: str, category: str) -> None:
        super().__init__(name, category)
        self.winget_api_url = "https://winget.run/api/v2"
        self.session = requests.Session()
        self.package_name = package_name

    def install(self, count: tuple):
        pty = winpty.PtyProcess.spawn(f"winget install -e --id {self.package_name}")
        erro = 0
        seq = ["-", "\\", "|", "/"]
        seq_idx = 0
        pbar = None
        current_mbs = (-1,-1)
        first_bar = True
        #print(f"\033[?25l   \033[36m[{count[0]}/{count[1]}] - {self.name}\033[m")
        print(f"   \033[36m[{count[0]}/{count[1]}] - {self.name}\033[m")
        while pty.isalive():
            try:
                data = pty.read()
                if data:
                    mb1, mb2 = get_size(data)
                    
                    if mb1 == -1 and mb2 == -1 and current_mbs == (-1,-1):
                        print(f"\r  \033[35m{seq[(seq_idx+1)%len(seq)]}", end="\033[m")
                        seq_idx += 1
                        
                    elif mb1 != -1 and mb2 != -1:
                        current_mbs = (mb1, mb2)
                        if pbar is None:
                            print("\r      \r", end=("" if first_bar else "\n"))
                            pbar = tqdm(total=mb2,  bar_format='{l_bar}\033[35m{bar}\033[m| {n_fmt}/{total_fmt} MB | {remaining}')
                        
                        if current_mbs[0] <= current_mbs[1]:
                            pbar.update(mb1 - pbar.n)
                            sys.stdout.flush()
                            
                        if current_mbs[0] >= current_mbs[1]:
                            current_mbs = (-1,-1)
                            pbar = None

            except KeyboardInterrupt:
                if pbar is not None:
                    pbar.close()
                erro = -1
                break
            except EOFError:
                if pbar is not None:
                    pbar.close()
                break
        
        
        pty.close()
        if (pty.exitstatus and not erro): erro = 1

        print("\r                   ", end="\r\033[m", flush=True)
        
        if erro == 0:
            print(f'\033[32;1m{self.name} installed successfully\033[m\n')
        elif erro == -1:
            print('\033[33;1mAborting\033[m\n')
        elif erro == 1:
            print(f'\033[31;1mAn error while installing {self.name}\033[m\n')
            
        return erro

    def download(self, count: tuple):
        pty = winpty.PtyProcess.spawn(f"winget download -e --id {self.package_name} -d {download_path}")
        erro = 0
        output = ""
        seq = ["-", "\\", "|", "/"]
        seq_idx = 0
        pbar = None
        current_mbs = (-1,-1)
        first_bar = True
        #print(f"\033[?25l   \033[36m[{count[0]}/{count[1]}] - {self.name}\033[m")
        print(f"   \033[36m[{count[0]}/{count[1]}] - {self.name}\033[m")
        while pty.isalive():
            try:
                data = pty.read()
                if data:
                    mb1, mb2 = get_size(data)
                    
                    if mb1 == -1 and mb2 == -1 and current_mbs == (-1,-1):
                        print(f"\r  \033[35m{seq[(seq_idx+1)%len(seq)]}", end="\033[m")
                        seq_idx += 1
                        
                    elif mb1 != -1 and mb2 != -1:
                        current_mbs = (mb1, mb2)
                        if pbar is None:
                            print("\r      \r", end=("" if first_bar else "\n"))
                            pbar = tqdm(total=mb2,  bar_format='{l_bar}\033[35m{bar}\033[m| {n_fmt}/{total_fmt} MB | {remaining}', leave=False)
                        
                        if current_mbs[0] <= current_mbs[1]:
                            pbar.update(mb1 - pbar.n)
                            sys.stdout.flush()
                            
                        if current_mbs[0] >= current_mbs[1]:
                            current_mbs = (-1,-1)
                            pbar = None
                        
                    output = data  
            except KeyboardInterrupt:
                if pbar is not None:
                    pbar.close()
                erro = -1
                break
            except EOFError:
                if pbar is not None:
                    pbar.close()
                break
        
        
        pty.close()
        if (pty.exitstatus and not erro): erro = 1

        print("\r                   ", end="\r\033[m", flush=True)
        
        if erro == 0:
            installer_path = os.path.normpath(output.split(": ")[-1]).split("\r\n")[0]
            yaml_path = ".".join(installer_path.split(".")[:-1])+".yaml"
            st = time.time()
            while not os.path.exists(yaml_path) and time.time() - st < 2: pass
            if os.path.exists(yaml_path):
                os.remove(yaml_path)
            print(f'\033[32;1m{self.name} downloaded successfully\033[m\n')
        
        elif erro == -1:
            print('\033[33;1mAborting\033[m\n')
        elif erro == 1:
            print(f'\033[31;1mAn error while downloading {self.name}\033[m\n')
            
        return erro
        
        

        
        
        