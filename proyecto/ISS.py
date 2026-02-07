import re
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import calendar
import os

# Clase para gestionar las tareas
class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def add_task(self, name, time, date):
        if any(task[0].lower() == name.lower() for task in self.tasks):
            messagebox.showwarning("Duplicate task", f"Task with the name '{name}' already exists.")
            return

        self.tasks.append((name, time, date))
        self.save_tasks()
        print(f"Task '{name}' added on {date} successfully.")

    def show_tasks(self):
        if not self.tasks:
            messagebox.showinfo("Tasks", "No tasks registered.")
        else:
            tasks = "\n".join([f"{i+1}. {name} - {time} on {date}" for i, (name, time, date) in enumerate(self.tasks)])
            messagebox.showinfo("Tasks", f"Tasks:\n{tasks}")

    def delete_task(self, name):
        for i, (task_name, _, _) in enumerate(self.tasks):
            if task_name.lower() == name.lower():
                del self.tasks[i]
                self.save_tasks()
                messagebox.showinfo("Delete task", f"Task '{name}' deleted successfully.")
                return
        messagebox.showwarning("Delete task", f"Task '{name}' not found.")

    def delete_all_tasks(self):
        if not self.tasks:
            messagebox.showinfo("Info", "No tasks to delete.")
        else:
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all tasks?")
            if confirm:
                self.tasks.clear()
                self.save_tasks()
                messagebox.showinfo("Delete all tasks", "All tasks have been successfully deleted.")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks registered.")
        else:
            print("List of tasks:")
            for i, (name, time, date) in enumerate(self.tasks, start=1):
                print(f"{i}. {name} - {time} on {date}")

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.tasks = json.load(f)

    def tasks_for_date(self, date):
        return [task for task in self.tasks if task[2] == date]

    def search_task(self, name):
        for i, (task_name, time, date) in enumerate(self.tasks):
            if task_name.lower() == name.lower():
                return i, (task_name, time, date)
        return None, None
    
# Clase para la interfaz del calendario
class CalendarUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar tasks")
        self.root.geometry("600x300")
        self.task_manager = TaskManager()
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.day_buttons = {}
        self.day_windows = {}
        self.day_window = None

        # Crear estilos personalizados para los botones de los días
        self.style = ttk.Style()
        self.style.configure("Task.TButton", background="pink")
        self.style.configure("NoTask.TButton", background="SystemButtonFace")
        #root.configure(bg="yellow")
        # Crear una etiqueta para el mes y año
        self.month_year_label = ttk.Label(self.root, font=("helvetica", 12, "bold"))
        self.month_year_label.grid(row=0, column=0, columnspan=7, pady=5)

        # Crear una etiqueta para mostrar el día actual
        self.today_label = ttk.Label(self.root, font=("helvetica", 7, "bold"), foreground="black", anchor="w")
        self.today_label.grid(row=0, column=0, columnspan=3, pady=5, padx=5, sticky="w")
        self.update_today_label()

        self.create_calendar()
        self.update_month_year_label()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Configuración de redimensionamiento automático
        self.setup_resizing()

    def setup_resizing(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        for row in range(3, 8):
            self.root.grid_rowconfigure(row, weight=1)
        for i in range(7):
            self.root.grid_columnconfigure(i, weight=1)

    def create_calendar(self):
        prev_year_button = ttk.Button(self.root, text="<< Year", command=self.previous_year)
        prev_year_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        next_year_button = ttk.Button(self.root, text="Year >>", command=self.next_year)
        next_year_button.grid(row=1, column=6, padx=5, pady=5, sticky="nsew")

        prev_month_button = ttk.Button(self.root, text="<< Month", command=self.previous_month)
        prev_month_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        next_month_button = ttk.Button(self.root, text="Month >>", command=self.next_month)
        next_month_button.grid(row=1, column=5, padx=5, pady=5, sticky="nsew")

        for col, day in enumerate(self.days_of_week):
            label = ttk.Label(self.root, text=day, font=("helvetica", 10, "bold"), anchor='center')
            label.grid(row=2, column=col, padx=5, pady=5, sticky="nsew")

        month_days = calendar.monthcalendar(self.year, self.month)
        for row, week in enumerate(month_days, start=3):
            for col, day in enumerate(week):
                if day == 0:
                    label = ttk.Label(self.root, text="")
                    label.grid(row=row, column=col, sticky="nsew")
                else:
                    button = ttk.Button(self.root, text=str(day), command=lambda day=day: self.open_task_menu(day))
                    button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                    self.day_buttons[day] = button
                    self.update_day_button_color(day)

    def open_task_menu(self, day):
        if day in self.day_windows and self.day_windows[day].winfo_exists():
            return
        if self.day_window != None:
            self.day_window.destroy()
        self.day_window = tk.Toplevel(self.root)
        self.day_window.title(f"Options for the day {day}")
        self.day_window.geometry("400x275")

        self.day_windows[day] = self.day_window

        def execute_option(option):
            if option == 1:
                name = simpledialog.askstring("Add task", "Name of the task:")
                time = self.get_valid_time()
                if name and time:
                    date = f"{self.year}-{self.month:02d}-{day:02d}"
                    self.task_manager.add_task(name, time, date)
                    self.update_day_button_color(day)
            elif option == 2:
                self.task_manager.show_tasks()
            elif option == 3:
                name = simpledialog.askstring("Delete task", "Name of task to delete:")
                if name:
                    self.task_manager.delete_task(name)
                    self.update_day_button_color(day)
            elif option == 4:
                self.task_manager.list_tasks()
            elif option == 5:
                self.task_manager.delete_all_tasks()
                self.update_calendar()
            elif option == 6:
                search_name = simpledialog.askstring("Search task", "Enter the name of the task:")
                if search_name:
                    index, task_details = self.task_manager.search_task(search_name)
                    if task_details:
                        messagebox.showinfo(
                            "Search Result",
                            f"Task found:\nIndex: {index + 1}\nName: {task_details[0]}\nTime: {task_details[1]}\nDate: {task_details[2]}",
                        )
                    else:
                        messagebox.showwarning("Search Result", "Task not found.")
            elif option == 7:
                self.day_windows[day] = None
                self.day_window.destroy()

        options = {
            "1": "Add task",
            "2": "Show tasks",
            "3": "Delete task",
            "4": "List tasks",
            "5": "Delete all tasks",
            "6": "Search task",
            "7": "Exit"
        }

        for key, text in options.items():
            button = tk.Button(self.day_window, text=text, command=lambda opt=int(key): execute_option(opt))
            button.pack(pady=5)

    def update_day_button_color(self, day):
        date = f"{self.year}-{self.month:02d}-{day:02d}"
        tasks = self.task_manager.tasks_for_date(date)
        if tasks:
            self.day_buttons[day].config(style="Task.TButton")
        else:
            self.day_buttons[day].config(style="NoTask.TButton")

    def get_valid_time(self):
        while True:
            time = simpledialog.askstring("Add task", "Enter task time (HH:MM):")
            if time and re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", time):
                return time
            else:
                messagebox.showwarning("Invalid time", "Enter time in HH:MM format.")

    def update_month_year_label(self):
        self.month_year_label.config(text=f"{calendar.month_name[self.month]} {self.year}")

    def update_today_label(self):
        today = datetime.now().strftime("Today is %A, %d %B %Y")
        self.today_label.config(text=today)
        self.setup_resizing()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.update_calendar()

    def previous_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.update_calendar()

    def next_year(self):
        self.year += 1
        self.update_calendar()

    def previous_year(self):
        self.year -= 1
        self.update_calendar()

    def update_calendar(self):
        for button in self.day_buttons.values():
            button.destroy()
        self.day_buttons.clear()
        self.create_calendar()
        self.update_month_year_label()

    def on_close(self):
        self.task_manager.save_tasks()
        self.root.destroy()
    
# Crear y ejecutar la interfaz gráfica
def main():
    root = tk.Tk()
    app = CalendarUI(root)
    root.state("zoomed")
    root.mainloop()

if __name__ == "__main__":
    main()
