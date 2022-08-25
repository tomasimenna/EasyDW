import time, datetime, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from dbm_handler import dbm_handler
from settings_manager import create_settings_db

active_table_threads = []
active_db_threads = []
active_sch_threads = []

class EventHandler(FileSystemEventHandler):

    def __init__(self, server_to_connect, maindir_path):
        self.server_to_connect = server_to_connect
        self.maindir_path = maindir_path

    def on_modified(self, event):
        
        parentfolder = os.path.basename(os.path.dirname(event.src_path))
        parentpath = os.path.dirname(event.src_path)
        gparentpath = os.path.dirname(parentpath)
        ggparentpath = os.path.dirname(gparentpath)
        isfile = False if os.path.splitext(os.path.basename(event.src_path))[1] == '' else True

        valid = True if (parentpath == self.maindir_path and isfile == False) or gparentpath == self.maindir_path or (isfile == True and ggparentpath == self.maindir_path) else False
        isfile = isfile == True and True if valid == True else False
        isschema = True if gparentpath == self.maindir_path and isfile == False else False
        isdatabase = True if parentpath == self.maindir_path and valid == True else False
        hasschema = parentfolder if isfile == True and ggparentpath == self.maindir_path else 'dbo'
        # ----------------------------------------------------------------
        
        if os.path.splitext(os.path.basename(event.src_path))[0] == 'New folder' and isfile == False:
            pass
        
        elif isdatabase == True:
            def Worker():
                if event.src_path in active_db_threads:
                    pass
                else:
                    active_db_threads.append(event.src_path)
                    time.sleep(2)
                    dbm_handler(event = event, task = 'create database', server_to_connect = self.server_to_connect)
                    active_db_threads.remove(event.src_path)
            t = threading.Thread(target = Worker)
            t.start()

        elif isschema == True:
            def Worker():
                if event.src_path in active_sch_threads:
                    pass
                else:
                    active_sch_threads.append(event.src_path)
                    time.sleep(2)
                    dbm_handler(event = event, task = 'create schema', server_to_connect = self.server_to_connect)
                    active_sch_threads.remove(event.src_path)
            t = threading.Thread(target = Worker)
            t.start()

        elif isfile == True:
            def Worker():
                if event.src_path in active_table_threads:
                    pass
                else:
                    active_table_threads.append(event.src_path)
                    time.sleep(2)
                    dbm_handler(event = event, task = 'create table', server_to_connect = self.server_to_connect, hasschema = hasschema)
                    active_table_threads.remove(event.src_path)
            t = threading.Thread(target = Worker)
            t.start()

        else:
            pass

    def on_deleted(self, event):

        parentfolder = os.path.basename(os.path.dirname(event.src_path))
        parentpath = os.path.dirname(event.src_path)
        gparentpath = os.path.dirname(parentpath)
        ggparentpath = os.path.dirname(gparentpath)
        isfile = False if os.path.splitext(os.path.basename(event.src_path))[1] == '' else True

        valid = True if (parentpath == self.maindir_path and isfile == False) or gparentpath == self.maindir_path or (isfile == True and ggparentpath == self.maindir_path) else False
        isfile = isfile == True and True if valid == True else False
        isschema = True if gparentpath == self.maindir_path and isfile == False else False
        isdatabase = True if parentpath == self.maindir_path and valid == True else False
        hasschema = parentfolder if isfile == True and ggparentpath == self.maindir_path else 'dbo'
        # ----------------------------------------------------------------

        if isdatabase == True:
            t = threading.Thread(target = dbm_handler, args = (event, 'drop database', self.server_to_connect))
            t.start()

        elif isschema == True:
            t = threading.Thread(target = dbm_handler, args = (event, 'drop schema', self.server_to_connect))
            t.start()

        elif isfile == True:
            t = threading.Thread(target = dbm_handler, args = (event, 'drop table', self.server_to_connect, hasschema))
            t.start()
        
        else:
            pass        

def start_monitoring(path_to_monitor, server_to_connect):
    global observer
    create_settings_db(server_to_connect = server_to_connect)
    event_handler=EventHandler(server_to_connect = server_to_connect, maindir_path = path_to_monitor)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_monitor, recursive=True)
    observer.start()
    print(f'''{str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))}: Monitoring started''')

    try:
        while(True):
           time.sleep(1)
           
    except KeyboardInterrupt:
            observer.stop()
            observer.join()

def stop_monitoring():
    observer.stop()
    observer.join()