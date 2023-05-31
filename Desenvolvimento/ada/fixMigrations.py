import os
import sys

print(sys.argv[1])

if(sys.argv[1] == 'deleteDB'):
    os.remove(os.getcwd() + '\\db.sqlite3')
    print("DB removido")

active = True

listApps = ["area","attribution","attribution_preference", "_class", "course", "exchange", "staff", "timetable", "user"]

if(active):
    for app in listApps:
        directory = os.getcwd() + '\\'+app+'\migrations'
        listFiles = os.listdir(directory)
        listFiles.remove('__init__.py')
        for filename in listFiles:
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                # print("Removed ", filename)
        print("Todos os arquivos de migração foram removidos de ", app)
