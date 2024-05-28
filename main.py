import time 
from watchdog.observers import Observer  
from watchdog.events import FileSystemEventHandler 
import logging 
from datetime import datetime 
import os 
import shutil 

#Se define la clase watcher que es la que estará observando los cambios en el directorio
class Watcher:
    DIRECTORY_TO_WATCH = "/home/diego/Music/"

    def __init__(self):
        self.observer = Observer() 

    def run(self): 
        event_handler = Handler() 
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True) 
        self.observer.start()
        try: 
            while True: 
                time.sleep(5)
        except KeyboardInterrupt: 
            self.observer.stop() 
        self.observer.join() 


#Se define el manejador de eventos Handler 
class Handler(FileSystemEventHandler): 
    SYNC_DIRECTORY = "/mnt/external_drive_sync/Music_Sync/"

    @staticmethod 
    def on_any_event(event):
        if event.is_directory:
            return None

        #Obtener el tiempo actual
        timestamp = datetime.now().strftime('%y-%m-%d %H:%M:S')
        #Nombre del archivo o directorio afectado
        file_name = os.path.basename(event.src_path)


        if event.event_type == 'created':
            logging.info(f"{timestamp} - Created - {file_name} {event.src_path}")
            Handler.sync_file(event.src_path)
        elif event.event_type == 'modified':
            logging.info(f"{timestamp} - Modified - {file_name} - {event.src_path}")
            Handler.sync_file(event.src_path)
        elif event.event_type == 'deleted':
            logging.info(f"{timestamp} - Deleted - {file_name} - {event.src_path}")
            Handler.delete_file(event.src_path)

    @staticmethod
    def sync_file(src_path):
        try: 
            dest_path = os.path.join(Handler.SYNC_DIRECTORY, os.path.relpath(src_path, Watcher.DIRECTORY_TO_WATCH))
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            logging.info(f"File synced successfully from {src_path} to {dest_path}")
        except FileNotFoundError:
            logging.error(f"File not found error while syncing {src_path} to {dest_path}", exc_info=True)
        except PermissionError:
            logging.error(f"Permission error while syncing {src_path} to {dest_path}", exc_info=True)
        except Exception as e:
            logging.error(f"Unexpected error while syncing {src_path} to {dest_path}: {e}", exc_info=True)

            
    @staticmethod 
    def delete_file(src_path):
        try: 
            dest_path = os.path.join(Handler.SYNC_DIRECTORY, os.path.relpath(src_path, Watcher.DIRECTORY_TO_WATCH))
            if os.path.exists(dest_path):
                os.remove(dest_path)
                logging.info(f"File deleted successfully: {dest_path}")
            else:
                logging.warning(f"File to delete not found: {dest_path}")
        except FileNotFoundError:
            logging.error(f"File not found error while deleting {dest_path}", exc_info=True)
        except PermissionError:
            logging.error(f"Permission error while deleting {dest_path}", exc_info=True)
        except Exception as e:
            logging.error(f"Unexpected error while deleting {dest_path}: {e}", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig(
        filename='/tmp/monitor_de_directorio.log', 
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ) 
    w = Watcher()
    w.run()
