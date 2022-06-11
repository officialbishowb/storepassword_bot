from datetime import datetime
import os
class Log:
    
        
        
        
    def __init__(self, symbol, log_message):
        self.symbol = symbol
        self.log_message = log_message
        self.log_date = str(datetime.now())
        self.filename = "error_log.txt"
    
    
    def save_logs(self):
        if not os.path.exists(self.name):
            f = open(self.name, "x")
            f.close()
        with open(self.name, "a") as f:
            f.write(f"{self.log_date}: {self.symbol} - {self.log_message}\n")
        return True
    
    
    def delete_logs(self):
        with open(self.name, "w") as f:
            pass
        return True
            
        
        
    