import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class StudentSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dish Food Pantry Scheduler")
        
        # Set a minimum window size
        self.root.minsize(600, 400)

        # Initialize the student list
        self.students = []

        # Use a notebook for tabbed interface
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both')

        # Create a frame for the "Add Student" tab
        add_student_frame = ttk.Frame(notebook, padding="10")
        notebook.add(add_student_frame, text='Add Student')

        # Widgets for the "Add Student" tab
        ttk.Label(add_student_frame, text="Student Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.student_name_entry = ttk.Entry(add_student_frame, width=20)
        self.student_name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(add_student_frame, text="Hours per week:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.hours_entry = ttk.Entry(add_student_frame, width=5)
        self.hours_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        add_student_button = ttk.Button(add_student_frame, text="Add Student", command=self.add_student)
        add_student_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Create a frame for the "Schedule" tab
        schedule_frame = ttk.Frame(notebook, padding="10")
        notebook.add(schedule_frame, text='Schedule')

        # Button to generate schedule
        generate_button = ttk.Button(schedule_frame, text="Generate Schedule", command=self.generate_schedule)
        generate_button.pack(side='top', pady=10)

        # Placeholder for schedule display area
        self.schedule_display = ttk.Label(schedule_frame, text="Schedule will appear here", anchor="center", justify=tk.CENTER)
        self.schedule_display.pack(side='top', fill='both', expand=True)

        # Configure the grid layout for the "Add Student" tab
        add_student_frame.columnconfigure(1, weight=1)
        add_student_frame.rowconfigure(3, weight=1)

    def add_student(self):
        # Retrieve entered student information
        name = self.student_name_entry.get()
        hours = self.hours_entry.get()
        
        # Validate the inputs
        try:
            hours = float(hours)
            if hours <= 0:
                raise ValueError("Hours must be greater than zero.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return
        
        if not name:
            messagebox.showerror("Invalid Input", "Please enter a name for the student.")
            return
        
        # Get student availability
        availability = self.get_availability()

        # Store the student information
        self.students.append({'name': name, 'hours': hours, 'availability': availability})
        
        # Clear the entry fields for next input
        self.student_name_entry.delete(0, tk.END)
        self.hours_entry.delete(0, tk.END)

        messagebox.showinfo("Success", f"Student {name} added successfully.")

    def get_availability(self):
        # Function to handle input for each day of the week
        availability = {}
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            day_availability = []
            while True:
                time_range = simpledialog.askstring("Input", 
                                                    f"Enter {day}'s availability as 'start-end' in 24h format, or 'done' if finished:",
                                                    parent=self.root)
                if not time_range or time_range.lower() == 'done':
                    break
                try:
                    start_time, end_time = map(int, time_range.split('-'))
                    if 0 <= start_time < end_time <= 24:
                        day_availability.append((start_time, end_time))
                    else:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid time range as 'start-end' (e.g., '9-17').")
                    continue
            if day_availability:
                availability[day] = day_availability
        return availability

    def generate_schedule(self):
        # Example structure for office hours
        office_hours = {
            'Inventory Room': {'Monday': (8, 18), 'Tuesday': (8, 18), 'Wednesday': (8, 18), 'Thursday': (8, 18), 'Friday': (8, 18)},
            'Main Office': {'Monday': (11, 15), 'Tuesday': (11, 15), 'Wednesday': (11, 15), 'Thursday': (11, 15), 'Friday': (11, 15)},
            'G Building': {'Monday': (15, 19), 'Tuesday': (15, 19), 'Wednesday': (15, 19), 'Thursday': (15, 19), 'Friday': (15, 19)}
        }
        
        # Initialize the schedule with the required number of students
        schedule = {office: {day: [] for day in office_hours[office]} for office in office_hours}
        required_staff = {
            'Inventory Room': 2, 
            'Main Office': 1, 
            'G Building': 1
        }

        # Create a list of all possible shifts for convenience
        all_shifts = [(office, day) for office in office_hours for day in office_hours[office]]

        # Assign students to shifts
        for student in self.students:
            # Check each day for each student's availability
            for day, slots in student['availability'].items():
                # Attempt to fill the Main Office and G Building first
                for office in ['Main Office', 'G Building', 'Inventory Room']:
                    if len(schedule[office][day]) < required_staff[office]:
                        for slot in slots:
                            start = max(slot[0], office_hours[office][day][0])
                            end = min(slot[1], office_hours[office][day][1])
                            if start < end:
                                # Add the student to the shift
                                schedule[office][day].append({'name': student['name'], 'start': start, 'end': end})
                                break  # Move on to the next office or day
                        if len(schedule[office][day]) == required_staff[office]:
                            break  # This office is fully staffed for the day

        # Check if all shifts are filled and display a message if not
        for office, days in schedule.items():
            for day, staff in days.items():
                if len(staff) < required_staff[office]:
                    messagebox.showwarning("Scheduling Issue", 
                                           f"Not enough staff for {office} on {day}. Required: {required_staff[office]}, Scheduled: {len(staff)}")

        # Display the schedule
        schedule_str = ""
        for office, days in schedule.items():
            schedule_str += f"{office}:\n"
            for day, shifts in days.items():
                shift_str = ", ".join([f"{shift['name']} ({shift['start']} - {shift['end']})" for shift in shifts])
                schedule_str += f"  {day}: {shift_str}\n"
        
        self.schedule_display['text'] = schedule_str

def main():
    root = tk.Tk()
    app = StudentSchedulerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
