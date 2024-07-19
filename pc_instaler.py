from apps import WinGet_Program
import get_versions
from window import Window

win = Window()

win.add_program(WinGet_Program("Android Studio", "Google.AndroidStudio", "Programing"))
win.add_program(WinGet_Program("Arduino", "ArduinoSA.IDE.stable", "Programing"))
win.add_program(WinGet_Program("Clink", "chrisant996.Clink", "Programing"))
win.add_program(WinGet_Program("Docker CLI", "Docker.DockerCLI", "Programing"))
win.add_program(WinGet_Program("Docker Desktop", "Docker.DockerDesktop", "Programing"))
win.add_program(WinGet_Program("Git", "Git.Git", "Programing"))
win.add_program(WinGet_Program("MS Terminal", "Microsoft.WindowsTerminal", "Programing"))
win.add_program(WinGet_Program("Nano", "GNU.Nano", "Programing"))
win.add_program(WinGet_Program("NetBeans", "Apache.NetBeans", "Programing"))
win.add_program(WinGet_Program("Notepad++", "Notepad++.Notepad++", "Programing"))
win.add_program(WinGet_Program("Oh-My-Posh", "JanDeDobbeleer.OhMyPosh", "Programing"))
win.add_program(WinGet_Program("PuTTY", "PuTTY.PuTTY", "Programing"))
win.add_program(WinGet_Program("PyCharm", "JetBrains.PyCharm.Community.EAP", "Programing"))
win.add_program(WinGet_Program("Python 2", "Python.Python.2", "Programing"))
for version in get_versions.python_versions():
    win.add_program(WinGet_Program(f"Python {version}", f"Python.Python.{'.'.join(version.split('.')[:2])}", "Programing"))
win.add_program(WinGet_Program("Visual Studio", "Microsoft.VisualStudio.2022.Community", "Programing"))
win.add_program(WinGet_Program("Visual Studio Code", "Microsoft.VisualStudioCode", "Programing"))
    
win.add_program(WinGet_Program("Discord", "Discord.Discord", "Social"))
win.add_program(WinGet_Program("Microsoft Teams", "Microsoft.Teams", "Social"))
win.add_program(WinGet_Program("Spotify", "Spotify.Spotify", "Social"))
win.add_program(WinGet_Program("Thunderbird", "Mozilla.Thunderbird", "Social"))
#win.add_program(WinGet_Program("WhatsApp", "9NKSQGP7F2NH", "Social"))
win.add_program(WinGet_Program("Zoom", "Zoom.Zoom", "Social"))

win.add_program(WinGet_Program("7-Zip", "7zip.7zip", "Tools"))
win.add_program(WinGet_Program("Acrobat Reader", "Adobe.Acrobat.Reader.64-bit", "Tools"))
win.add_program(WinGet_Program("Chocolatey", "Chocolatey.Chocolatey", "Tools"))
win.add_program(WinGet_Program("EarTrumpet", "File-New-Project.EarTrumpet", "Tools"))
win.add_program(WinGet_Program("Firefox", "Mozilla.Firefox", "Tools"))
win.add_program(WinGet_Program("GIMP", "GIMP.GIMP", "Tools"))
win.add_program(WinGet_Program("Google Chrome", "Google.Chrome", "Tools"))
win.add_program(WinGet_Program("Krita", "KDE.Krita", "Tools"))
win.add_program(WinGet_Program("LibreOffice", "TheDocumentFoundation.LibreOffice", "Tools"))
win.add_program(WinGet_Program("Ollama", "Ollama.Ollama", "Tools"))
win.add_program(WinGet_Program("PowerToys", "Microsoft.PowerToys", "Tools"))
win.add_program(WinGet_Program("qBittorrent ", "qBittorrent.qBittorrent ", "Tools"))
win.add_program(WinGet_Program("Rufus", "Rufus.Rufus", "Tools"))
win.add_program(WinGet_Program("Unchecky", "Unchecky.Unchecky", "Tools"))
win.add_program(WinGet_Program("VirtualBox", "Oracle.VirtualBox", "Tools"))
win.add_program(WinGet_Program("VLC", "VideoLAN.VLC", "Tools"))
win.add_program(WinGet_Program("VNC Viewer", "RealVNC.VNCViewer", "Tools"))
win.add_program(WinGet_Program("Wget2", "GNU.Wget2", "Tools"))
win.add_program(WinGet_Program("WinRar", "RARLab.WinRAR", "Tools"))
win.add_program(WinGet_Program("Wireshark", "WiresharkFoundation.Wireshark", "Tools"))
win.add_program(WinGet_Program("Xournal++", "Xournal++.Xournal++", "Tools"))

win.add_program(WinGet_Program("Citra", "CitraEmu.Citra", "Games"))
win.add_program(WinGet_Program("Epic Games", "EpicGames.EpicGamesLauncher", "Games"))
win.add_program(WinGet_Program("Google Play", "Google.PlayGames.Beta", "Games"))
win.add_program(WinGet_Program("Hydra Laucher", "HydraLauncher.Hydra", "Games"))
win.add_program(WinGet_Program("PPSSPP", "PPSSPPTeam.PPSSPP", "Games"))
win.add_program(WinGet_Program("Steam", "Valve.Steam", "Games"))

win.start()