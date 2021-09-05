import os
import time


class FileMonitor():

    def __init__(self, name: str, type: str, data):
        self.name = name
        self.type = type
        self.data = data
        print("\n" + self.name)
        for i in data:
            print(i + "\t" + data[i])
    
    def start(self):
        print("Monitor: {name} has been started",self.name)
        monitor_func = getattr(self.FileMonitor,self.type)
        monitor_func()
    
    def move(self):
        
        dst_dir = self.data['destination']
        src = self.data['source']
        
        moved = False

        while not moved:
            # Checks if the file exists in the source dir
            if os.path.isfile(src):
                # Moves file to destination
                os.rename(src, dst_dir + r"\\" + os.path.basename(src))
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
