import multiprocessing
import configparser
import file_monitor


class OverSeer():

    def __init__(self, cfg_path: str):
        self.monitors = []
        self.parse_cfg(cfg_path)
        self.create_queues()

    def parse_cfg(self, cfg_path):
        config = configparser.ConfigParser()
        config.read(cfg_path)
        for monitor in config.sections():
            # Create a new monitor instance based on the config file
            monitor_data = {}
            # Creates a monitor data dict to pass required data to the FileMonitor object
            for i in config[monitor]: 
                monitor_data[i] = config[monitor][i]
            # Drops the monitor type from the data as that has been written to the object already
            del monitor_data['monitor_type']
            # Add the monitor to the list of monitors
            self.monitors.append(file_monitor.FileMonitor(name=monitor, type=config[monitor]['monitor_type'], data=monitor_data))

    def create_queues(self):
        self.queue = multiprocessing.JoinableQueue()
        self.status = multiprocessing.Queue()
        
        # Start monitors
        print(f"Creating {len(self.monitors)} monitors")
        
        monitor_processes = [file_monitor.MonitorProcess(self.queue, self.status)
                             for i in range(0,len(self.monitors))]
        
        for process in monitor_processes:
            process.start()
    
        for monitor in self.monitors:
            self.queue.put(file_monitor.FileMonitor(monitor.name, monitor.type, monitor.data))            

        for process in monitor_processes:
            self.queue.put(None)
        
        self.queue.join()
        

if __name__ == '__main__':
    overseer = OverSeer(cfg_path=r"file_monitor_cfg.ini")
