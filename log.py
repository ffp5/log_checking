import json
import sys
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext

class LoggingTool:
    def __init__(self, filename):
        self.filename = filename
        self.log = []

    def parse_log(self):
        """Parse log file and save it to self.log"""
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    self.log.append(json.loads(line))
        except FileNotFoundError:
            print('File not found')

    def get_log(self):
        """Return log"""
        return self.log
    
    def processing_log(self, prio: int):
        """Process logs to get the ones with greater or equal priority than prio"""
        result = []
        for elem in self.log:
            priority = int(elem['PRIORITY'])
            if priority <= prio:
                result.append(f'ERROR of Priority= {priority}; type: {elem["MESSAGE"]}')
        return result
    
    def sort_by(self, sort_differenciator: str):
            """Sort the log by the given parameter and display additional information for each log entry"""
            result = []
            if sort_differenciator == 'priority':
                sorted_logs = sorted(self.log, key=lambda x: int(x['PRIORITY']))
            elif sort_differenciator == 'date':
                sorted_logs = sorted(self.log, key=lambda x: datetime.fromtimestamp(int(x['__REALTIME_TIMESTAMP'])/1000000))
            
            # Display additional information for each log entry
            for log_entry in sorted_logs:
                result.append(f"_SYSTEMD_UNIT: {log_entry.get('_SYSTEMD_UNIT', 'N/A')}")
                result.append(f"__REALTIME_TIMESTAMP: {log_entry.get('__REALTIME_TIMESTAMP', 'N/A')}")
                result.append(f"__MONOTONIC_TIMESTAMP: {log_entry.get('__MONOTONIC_TIMESTAMP', 'N/A')}")
                result.append(f"__BOOT_ID: {log_entry.get('__BOOT_ID', 'N/A')}")
                result.append(f"PROCESS_NAME: {log_entry.get('PROCESS_NAME', 'N/A')}")
                result.append(f"THREAD_NAME: {log_entry.get('THREAD_NAME', 'N/A')}")
                result.append(f"CODE_LINE: {log_entry.get('CODE_LINE', 'N/A')}")
                result.append(f"CODE_FILE: {log_entry.get('CODE_FILE', 'N/A')}")
                result.append(f"CODE_FUNC: {log_entry.get('CODE_FUNC', 'N/A')}")
                result.append(f"PRIORITY: {log_entry.get('PRIORITY', 'N/A')}")
                result.append(f"MESSAGE: {log_entry.get('MESSAGE', 'N/A')}")
                result.append("\n")

            return result

class LoggingToolGUI(tk.Tk):
    def __init__(self, file_path):
        super().__init__()

        self.title("Logging Tool GUI")

        self.log_file = LoggingTool(file_path)
        self.log_file.parse_log()

        self.create_gui()

    def create_gui(self):
        ttk.Label(self, text="Select Priority:").pack(pady=10)
        prio_combobox = ttk.Combobox(self, values=list(range(1, 8)))
        prio_combobox.pack(pady=10)
        prio_combobox.set(3)  # Default priority because it is ERROR

        ttk.Button(self, text="Display Logs", command=lambda: self.display_logs(prio_combobox.get())).pack(pady=10)
        
        ttk.Button(self, text="Sort by Priority", command=lambda: self.sort_and_display_logs('priority')).pack(pady=10)
        ttk.Button(self, text="Sort by Date", command=lambda: self.sort_and_display_logs('date')).pack(pady=10)

        self.log_display = scrolledtext.ScrolledText(self, width=80, height=20)
        self.log_display.pack(pady=10)

        self.mainloop()

    def display_logs(self, prio):
        logs = self.log_file.processing_log(int(prio))
        self.update_log_display(logs)

    def sort_and_display_logs(self, sort_by):
        sorted_logs = self.log_file.sort_by(sort_by)
        self.update_log_display(sorted_logs)

    def update_log_display(self, logs):
        self.log_display.delete(1.0, tk.END)  # Clear the current display
        for log_entry in logs:
            self.log_display.insert(tk.END, log_entry + '\n')

def main():
    file_path = sys.argv[1]
    
    # Run the GUI
    LoggingToolGUI(file_path)

if __name__ == '__main__':
    main()
