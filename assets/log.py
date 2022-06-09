class Log:
    def log(self, message):
        with open("log.info", "a") as log_file:
            log_file.write(message + "\n")