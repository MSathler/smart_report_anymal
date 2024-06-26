import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from report_xml_html import XML_TO_HTML

class Watcher:
    def __init__(self, directory_to_watch):
        self.observer = Observer()
        self.directory_to_watch = directory_to_watch

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print(f"Received created event - {event.src_path}.")
            if len(event.src_path.split('report.xml')) != 1:
                print('é xml')
                try:
                    XML_TO_HTML(event.src_path)
                except:
                    print(f'Erro ao converter o arquivo {event.src_path} para HTML')
        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print(f"Received modified event - {event.src_path}.")
            if len(event.src_path.split('report.xml')) != 1:
                print('é xml')
                try:
                    XML_TO_HTML(event.src_path)
                except:
                    print(f'Erro ao converter o arquivo {event.src_path} para HTML')

        elif event.event_type == 'deleted':
            # Taken any action here when a file is deleted.
            print(f"Received deleted event - {event.src_path}.")

if __name__ == '__main__':
    w = Watcher("/root/reports")
    w.run()