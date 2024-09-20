import tkinter as tk
from tkinter import messagebox, filedialog
from plyer import notification
import time
import threading
import datetime
import os

class NotificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Notification App")
        
        # Title Label and Entry
        tk.Label(root, text="Notification Title:").grid(row=0, column=0, padx=10, pady=10)
        self.title_entry = tk.Entry(root, width=50)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Message Label and Entry
        tk.Label(root, text="Notification Message:").grid(row=1, column=0, padx=10, pady=10)
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Interval Label and Entry
        tk.Label(root, text="Notification Interval (minutes):").grid(row=2, column=0, padx=10, pady=10)
        self.interval_entry = tk.Entry(root, width=50)
        self.interval_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Start Time Label and Entry
        tk.Label(root, text="Start Time (HH:MM, 24-hour format):").grid(row=3, column=0, padx=10, pady=10)
        self.start_time_entry = tk.Entry(root, width=50)
        self.start_time_entry.grid(row=3, column=1, padx=10, pady=10)
        
        # Sound Label and Button
        tk.Label(root, text="Select Notification Sound:").grid(row=4, column=0, padx=10, pady=10)
        self.sound_button = tk.Button(root, text="Choose Sound", command=self.choose_sound)
        self.sound_button.grid(row=4, column=1, padx=10, pady=10)
        self.sound_path = None
        
        # Preview Button
        self.preview_button = tk.Button(root, text="Preview Notification", command=self.preview_notification)
        self.preview_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Start Button
        self.start_button = tk.Button(root, text="Start Notifications", command=self.start_notifications)
        self.start_button.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Stop Button
        self.stop_button = tk.Button(root, text="Stop Notifications", command=self.stop_notifications, state=tk.DISABLED)
        self.stop_button.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Status Label
        self.status_label = tk.Label(root, text="Status: Idle", fg="red")
        self.status_label.grid(row=8, column=0, columnspan=2, pady=10)
        
        # Notification History Text
        self.history_text = tk.Text(root, height=10, width=70)
        self.history_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10)
        self.history_text.insert(tk.END, "Notification History:\n")
        self.history_text.config(state=tk.DISABLED)
        
        self.notification_thread = None
        self.running = False
    
    def choose_sound(self):
        self.sound_path = filedialog.askopenfilename(title="Select a Sound File", filetypes=[("Audio Files", "*.wav *.mp3")])
        if self.sound_path:
            self.sound_button.config(text=os.path.basename(self.sound_path))
    
    def preview_notification(self):
        title = self.title_entry.get()
        message = self.message_entry.get()
        if not title or not message:
            messagebox.showerror("Missing Information", "Please fill in both title and message.")
            return
        notification.notify(
            title=title,
            message=message,
            app_name='NotificationApp',
            timeout=10
        )
    
    def start_notifications(self):
        title = self.title_entry.get()
        message = self.message_entry.get()
        try:
            interval = int(self.interval_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the interval.")
            return
        
        start_time = self.start_time_entry.get()
        try:
            start_hour, start_minute = map(int, start_time.split(':'))
            start_datetime = datetime.datetime.combine(datetime.date.today(), datetime.time(start_hour, start_minute))
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter a valid start time in HH:MM format.")
            return
        
        if datetime.datetime.now() > start_datetime:
            start_datetime += datetime.timedelta(days=1)
        
        if not title or not message:
            messagebox.showerror("Missing Information", "Please fill in both title and message.")
            return
        
        self.status_label.config(text="Status: Running", fg="green")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.running = True
        
        # Start the notification thread
        self.notification_thread = threading.Thread(target=self.send_notifications, args=(title, message, interval, start_datetime))
        self.notification_thread.daemon = True
        self.notification_thread.start()
    
    def stop_notifications(self):
        self.running = False
        self.status_label.config(text="Status: Idle", fg="red")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def send_notifications(self, title, message, interval, start_datetime):
        while self.running:
            now = datetime.datetime.now()
            if now >= start_datetime:
                notification.notify(
                    title=title,
                    message=message,
                    app_name='NotificationApp',
                    timeout=10,
                    sound=self.sound_path
                )
                self.add_to_history(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Title: {title}, Message: {message}")
                start_datetime += datetime.timedelta(minutes=interval)
            time.sleep(10)  # Check every 10 seconds to see if it's time to send a notification
    
    def add_to_history(self, text):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, text + "\n")
        self.history_text.config(state=tk.DISABLED)
        self.history_text.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = NotificationApp(root)
    root.mainloop()
