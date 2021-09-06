import os
import time
import multiprocessing

class MonitorProcess(multiprocessing.Process):
    
    def __init__(self, monitor_queue:multiprocessing.JoinableQueue(), status_queue:multiprocessing.Queue()):
        multiprocessing.Process.__init__(self)
        self.monitor_queue = monitor_queue
        self.status_queue = status_queue
        
    def run(self):
        proc_name = self.name
        while True:
            next_monitor = self.monitor_queue.get()
            if next_monitor is None:
                print (f"{proc_name} Exiting")
                self.monitor_queue.task_done()
                break
            print(f"{proc_name}: moving on to {next_monitor}")
            status = next_monitor()
            self.monitor_queue.task_done()
            self.status_queue.put(status)
        return
    

class FileMonitor():

    def __init__(self, name: str, type: str, data):
        self.name = name
        self.type = type
        self.data = data

    def start(self):
        
        print("Monitor: {name} has been started",self.name)
        monitor_func = getattr(self.FileMonitor,self.type)
        monitor_func()
    
    def move(self):
        
        src = self.data['source']
        dst = self.data['destination'] + r"\\" + os.path.basename(src)
        
        moved = False

        while not moved:
            # Checks if the file exists in the source dir
            if os.path.isfile(src):
                # Moves file to destination
                os.rename(src, dst)
                moved = True
            else:
                time.sleep(1)

    def rename(self):
        
        new_name = self.data['new_name']
        
        renamed = False

        while not renamed:
            # Checks if the file exists in the source dir
            if os.path.isfile(self.src):
                # TODO Add rename code
                renamed = True
            else:
                time.sleep(1)