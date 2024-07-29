import tkinter as tk
from tkinter import messagebox
import random

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        # Get the position correctly
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()

class DragDropListbox(tk.Listbox):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.bind('<Button-1>', self.set_current)
        self.bind('<B1-Motion>', self.shift_selection)
        self.curIndex = None

    def set_current(self, event):
        self.curIndex = self.nearest(event.y)

    def shift_selection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i

class PlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Planner App")
        self.root.geometry("400x500")
        self.users = {}
        self.current_user = None
        self.tasks = []
        self.task_list = None
        self.motivational_messages = [
            "You can do it!",
            "Stay focused and you'll achieve your goals!",
            "Every small step counts towards big achievements!",
            "Believe in yourself and all that you are!",
            "Your only limit is you!",
            "Success is the sum of small efforts repeated day in and day out."
        ]
        self.motivation_label = None
        self.after_id = None  # Store the .after() call ID
        self.login_screen()

    def login_screen(self):
        self.clear_screen()
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(expand=True)
        tk.Label(self.login_frame, text="Login/Signup", font=("Arial", 24)).pack(pady=10)
        tk.Label(self.login_frame, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)
        tk.Label(self.login_frame, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self.login_frame, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.login_frame, text="Signup", command=self.signup).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users and self.users[username] == password:
            self.current_user = username
            self.welcome_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            if username not in self.users:
                self.users[username] = password
                messagebox.showinfo("Success", "Signup successful! Please login.")
            else:
                messagebox.showerror("Error", "Username already exists.")
        else:
            messagebox.showerror("Error", "Username and password are required.")

    def welcome_screen(self):
        self.clear_screen()
        self.welcome_frame = tk.Frame(self.root)
        self.welcome_frame.pack(expand=True)
        tk.Label(self.welcome_frame, text="Welcome!", font=("Arial", 24, "bold")).pack(pady=10)
        tk.Label(self.welcome_frame, text="You can make yourself more productive with our planner.\n"
                                          "Also you can motivate yourself through the competition with your friends!",
                 font=("Arial", 14), wraplength=350, justify="center").pack(pady=10)
        tk.Button(self.welcome_frame, text="Continue", command=self.main_screen).pack(pady=5)

    def main_screen(self):
        self.clear_screen()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        tk.Label(self.main_frame, text="My Planner", font=("Arial", 24)).pack(pady=10)
        self.motivation_label = tk.Label(self.main_frame, text="", font=("Arial", 12, "italic"), wraplength=350)
        self.motivation_label.pack(pady=10)
        
        self.add_task_button = tk.Button(self.main_frame, text="Add Task", command=self.add_task_screen)
        self.add_task_button.pack(pady=5)
        ToolTip(self.add_task_button, "Click to add a new task to your planner")
        
        self.task_list = DragDropListbox(self.main_frame, width=50)
        self.task_list.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.task_list.bind('<Double-1>', self.show_task_details)
        ToolTip(self.task_list, "Drag and drop to reorder tasks")
        
        self.sort_name_button = tk.Button(self.main_frame, text="Sort by Name", command=lambda: self.sort_tasks("name"))
        self.sort_name_button.pack(pady=5, side=tk.LEFT)
        ToolTip(self.sort_name_button, "Sort tasks alphabetically by name")
        
        self.sort_date_button = tk.Button(self.main_frame, text="Sort by Date", command=lambda: self.sort_tasks("date"))
        self.sort_date_button.pack(pady=5, side=tk.LEFT)
        ToolTip(self.sort_date_button, "Sort tasks by due date")
        
        for task in self.tasks:
            self.task_list.insert(tk.END, task['name'])
        
        self.update_motivation_message()
        self.new_features_label = tk.Label(self.main_frame, text="New Features: You can now receive motivational messages!", font=("Arial", 10), fg="blue")
        self.new_features_label.pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(pady=5)

    def update_motivation_message(self):
        if self.motivation_label:
            message = random.choice(self.motivational_messages)
            self.motivation_label.config(text=message)
            self.after_id = self.root.after(30000, self.update_motivation_message)  # Store the ID

    def cancel_after(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def add_task_screen(self):
        self.clear_screen()
        self.add_frame = tk.Frame(self.root)
        self.add_frame.pack(expand=True)
        tk.Label(self.add_frame, text="Add New Task", font=("Arial", 24)).pack(pady=10)
        tk.Label(self.add_frame, text="Task Name: (e.g., Buy groceries)").pack(pady=5)
        self.task_name_entry = tk.Entry(self.add_frame, width=40)
        self.task_name_entry.pack(pady=5)
        tk.Label(self.add_frame, text="Description: (e.g., Buy milk, eggs, and bread)").pack(pady=5)
        self.task_desc_entry = tk.Text(self.add_frame, height=5, width=40)
        self.task_desc_entry.pack(pady=5)
        tk.Label(self.add_frame, text="Due Date: (e.g., 2024-07-30)").pack(pady=5)
        self.task_date_entry = tk.Entry(self.add_frame, width=40)
        self.task_date_entry.pack(pady=5)
        tk.Button(self.add_frame, text="Add Task", command=self.add_task).pack(pady=5)
        tk.Button(self.add_frame, text="Cancel", command=self.main_screen).pack(pady=5)

    def add_task(self):
        task_name = self.task_name_entry.get()
        task_desc = self.task_desc_entry.get("1.0", tk.END).strip()
        task_date = self.task_date_entry.get()
        if task_name and task_date:
            task = {'name': task_name, 'desc': task_desc, 'date': task_date}
            self.tasks.append(task)
            self.main_screen()
        else:
            messagebox.showerror("Error", "Task name and due date are required.")

    def show_task_details(self, event):
        if not self.task_list.curselection():
            messagebox.showerror("Error", "No task selected.")
            return
        selected_index = self.task_list.curselection()[0]
        selected_task = self.tasks[selected_index]
        self.clear_screen()
        self.details_frame = tk.Frame(self.root)
        self.details_frame.pack(expand=True)
        tk.Label(self.details_frame, text="Task Details", font=("Arial", 24)).pack(pady=10)
        tk.Label(self.details_frame, text=f"Name: {selected_task['name']}").pack(pady=5)
        tk.Label(self.details_frame, text=f"Due Date: {selected_task['date']}").pack(pady=5)
        tk.Label(self.details_frame, text="Description:").pack(pady=5)
        tk.Label(self.details_frame, text=f"{selected_task['desc']}").pack(pady=5)
        tk.Button(self.details_frame, text="Back", command=self.main_screen).pack(pady=5)
        tk.Button(self.details_frame, text="Delete Task", command=lambda: self.delete_task(selected_index)).pack(pady=5)
        tk.Button(self.details_frame, text="Edit Task", command=lambda: self.edit_task_screen(selected_index)).pack(pady=5)

    def edit_task_screen(self, index):
        self.clear_screen()
        selected_task = self.tasks[index]
        self.edit_frame = tk.Frame(self.root)
        self.edit_frame.pack(expand=True)
        tk.Label(self.edit_frame, text="Edit Task", font=("Arial", 24)).pack(pady=10)
        tk.Label(self.edit_frame, text="Task Name:").pack(pady=5)
        self.edit_task_name_entry = tk.Entry(self.edit_frame, width=40)
        self.edit_task_name_entry.insert(0, selected_task['name'])
        self.edit_task_name_entry.pack(pady=5)
        tk.Label(self.edit_frame, text="Description:").pack(pady=5)
        self.edit_task_desc_entry = tk.Text(self.edit_frame, height=5, width=40)
        self.edit_task_desc_entry.insert(tk.END, selected_task['desc'])
        self.edit_task_desc_entry.pack(pady=5)
        tk.Label(self.edit_frame, text="Due Date:").pack(pady=5)
        self.edit_task_date_entry = tk.Entry(self.edit_frame, width=40)
        self.edit_task_date_entry.insert(0, selected_task['date'])
        self.edit_task_date_entry.pack(pady=5)
        tk.Button(self.edit_frame, text="Save Changes", command=lambda: self.save_task_changes(index)).pack(pady=5)
        tk.Button(self.edit_frame, text="Cancel", command=self.main_screen).pack(pady=5)

    def save_task_changes(self, index):
        task_name = self.edit_task_name_entry.get()
        task_desc = self.edit_task_desc_entry.get("1.0", tk.END).strip()
        task_date = self.edit_task_date_entry.get()
        if task_name and task_date:
            self.tasks[index] = {'name': task_name, 'desc': task_desc, 'date': task_date}
            self.main_screen()
        else:
            messagebox.showerror("Error", "Task name and due date are required.")

    def delete_task(self, index):
        task = self.tasks[index]
        confirm = messagebox.askyesno("Delete Task", f"Are you sure you want to delete the task '{task['name']}'? This action cannot be undone.")
        if confirm:
            self.tasks.pop(index)
            self.main_screen()

    def sort_tasks(self, key):
        self.tasks.sort(key=lambda x: x[key])
        self.update_task_list()

    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for task in self.tasks:
            self.task_list.insert(tk.END, task['name'])

    def logout(self):
        self.current_user = None
        self.login_screen()

    def clear_screen(self):
        self.cancel_after()  # Cancel the .after() call
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlannerApp(root)
    root.mainloop()