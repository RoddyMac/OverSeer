import multiprocessing
import configparser
import file_monitor


class OverSeer():

    def __init__(self, cfg_path: str):
        self.monitors = []
        self.parse_cfg(cfg_path)
        print("Processes created!")
        self.create_pool()

    # * Seems to be functioning as expected, reading in the config file correctly
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

    # TODO Fix from here down
    def start_monitors(self, monitor_id : int):
        if __name__ == '__main__':
            self.monitors[monitor_id].start()
    
    def create_pool(self):
        
        # * It appears that this line is working as expected
        pool = multiprocessing.Pool(processes=len(self.monitors))
        
        """
        ? Not very sure why this doesn't work, something about starting while the other  
        ? process is still in bootstrap phase?
        """
        pool.map(self.start_monitors, range(0,self.monitors.count))

overseer = OverSeer(cfg_path=r"file_monitor_cfg.ini")
