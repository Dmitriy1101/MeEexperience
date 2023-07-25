import subprocess as sbp
import pip
pkgs = eval(str(sbp.run("python3.exe -m pip list -o --format=json", shell=True,
                         stdout=sbp.PIPE).stdout, encoding='utf-8'))
for pkg in pkgs:
    sbp.run("python3.exe -m pip install --upgrade " + pkg['name'], shell=True)
    
