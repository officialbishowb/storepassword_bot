from datetime import datetime
import os
class Log:
    
    """Selfmade log class to log errors and other stuff
    """
    
    def __init__(self):
        self.filepath = "assets/error_log.txt"
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.makefile()
    
    
    def append(self,log_type,log_message):
        if not os.path.exists(self.filepath):
            self.makefile()
        with open(self.filepath, "a") as f:
            f.write(f"{self.current_time}: {log_type} - {log_message}\n")
        return True
    
    
    def clear(self):
        if not os.path.exists(self.filepath):
            self.makefile()
            pass
        with open(self.filepath, "w") as f:
            f.write("")
        return True
    
    
    def makefile(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                f.write("File created at: " + self.current_time + "\n")
            
            
    def fileIsEmpty(self):
        return os.stat(self.filepath).st_size == 0
            
        
        
    