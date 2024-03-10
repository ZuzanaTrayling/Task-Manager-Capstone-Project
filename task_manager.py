# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import datetime, date

# Define the datetime string format
DATETIME_STRING_FORMAT= "%Y-%m-%d" 

# Function to register a new user
def register_user(username_password):
    """Register a new user."""
    # Ask for new username and password
    new_username = input("New Username: ")
    # Check if the username already exists
    if new_username in username_password.keys():
        print("Username already exists. Please choose a different password.")
        return
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    # If passwords match, add the new user to the username_password dictionary
    if new_password == confirm_password:
        print("New user added")
        # Append the new user to the user file
        with open("user.txt", "a") as out_file:
            out_file.write(f"\n{new_username};{new_password}")
    else:
        print("Passwords do not match")

# Function to add a new task
def add_task(task_list):
    """Add a new task."""
    task_username = input("Name of person assigned to task: ")
    #Get task details: assigned user, title, description, due date
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            # Convert due date string to datetime object
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Get current date
    curr_date = date.today()
    # Create a new task dictionary with task details
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    # Append the new task to the task list
    task_list.append(new_task)
    # Write the updated task list to the task file
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# Function to view all tasks
def view_all(task_list):
    """View all tasks."""
    # Iterate through each task in the task list
    for t in task_list:
        # Display task details: title, assigned user, assigned date, due date, description
        
        disp_str = f"\nTask:\t\t  {t['title']}\n"
        disp_str += f"Assigned to:\t  {t['username']}\n"
        disp_str += f"Date Assigned:\t  {t ['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date:\t  {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: {t['description']}\n"
        print(disp_str)
        print("-"*50)

def view_my_tasks(curr_user, task_list):
    """View tasks assigned to the current user."""
    print(f"Tasks assigned to {curr_user}:")
    
    # Display all tasks assigned to the current user with corresponding numbers
    for i, task in enumerate(task_list):
        if task['username'] == curr_user:
            print(f"{i + 1}. Title: {task['title']}")
    
    
    # Prompt the user to select a task or return to the main menu
    while True:
        selection = input("Enter the number of the task you want to select (enter -1 to return to the main menu): ")
        
        if selection == '-1':
            return  # Return to the main menu if -1 is entered
        elif not selection.isdigit() or int(selection) < 1 or int(selection) > len(task_list):
            print("Invalid input. Please enter a valid task number.")
            continue
        else:
            selected_task_index = int(selection) - 1
            selected_task = task_list[selected_task_index]
            
            # Check if the selected task has been completed
            if selected_task['completed']:
                print("This task has already been completed and cannot be edited.")
            else:
                # Prompt the user to mark the task as complete or edit the task
                action = input("Select an action: \n1. Mark as complete\n2. Edit task\nEnter your choice: ")
                
                if action == '1':
                    # Mark the task as complete
                    task_list[selected_task_index]['completed'] = True
                    print("Task marked as complete.")
                elif action == '2':
                    # Edit the task (username or due date)
                    new_username = input("Enter the new username (press Enter to keep it unchanged): ")
                    new_due_date = input("Enter the new due date (YYYY-MM-DD format, press Enter to keep it unchanged): ")
                    
                    # Update task details if provided
                    if new_username:
                        task_list[selected_task_index]['username'] = new_username
                    if new_due_date:
                        try:
                            new_due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                            task_list[selected_task_index]['due_date'] = new_due_date
                        except ValueError:
                            print("Invalid datetime format. Task due date not updated.")
                    print("Task updated.")
                else:
                    print("Invalid selection. Please enter either '1' or '2'.")

# Function to generate reports
def generate_reports(task_list, username_password):
    """Generate reports."""
    # Calculate various statistics based on task completion and deadlines
    num_tasks = len(task_list)
    num_completed_tasks = sum(1 for t in task_list if t['completed'])
    num_incomplete_tasks = num_tasks - num_completed_tasks
    num_overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'] < datetime.now())

    total_users = len(username_password)
    total_assigned_tasks = sum(1 for t in task_list if t['username'] != 'admin')
    total_completed_user_tasks = sum(1 for t in task_list if t['completed'] and t['username'] != 'admin')

    incomplete_percentage = (num_incomplete_tasks / num_tasks) * 100 if num_tasks != 0 else 0
    overdue_percentage = (num_overdue_tasks / num_tasks) * 100 if num_tasks != 0 else 0

    # Write task overview statistics to task_overview.txt file
    with open("task_overview.txt", "w") as task_report:
        task_report.write(f"Total number of tasks: {num_tasks}\n")
        task_report.write(f"Total number of completed tasks: {num_completed_tasks}\n")
        task_report.write(f"Total number of uncompleted tasks: {num_incomplete_tasks}\n")
        task_report.write(f"Total number of overdue tasks: {num_overdue_tasks}\n")
        task_report.write(f"Percentage of tasks incomplete: {incomplete_percentage:.2f}%\n")
        task_report.write(f"Percentage of tasks overdue: {overdue_percentage:.2f}%\n")

    # Write user overview statistics to user_overview.txt file
    with open("user_overview.txt", "w") as user_report:
        user_report.write(f"Total number of users: {total_users}\n")
        user_report.write(f"Total number of tasks: {num_tasks}\n")
        user_report.write("\n")
        user_report.write("User Task Assignment Statistics:\n")
        for username in username_password:
            if username != 'admin':
                user_assigned_tasks = sum(1 for t in task_list if t['username'] == username)
                user_completed_tasks = sum(1 for t in task_list if t['username'] == username and t['completed'])
                user_incomplete_tasks = user_assigned_tasks - user_completed_tasks
                user_overdue_tasks = sum(1 for t in task_list if t['username'] == username and not t['completed'] and t['due_date'] < datetime.now())

                user_completed_percentage = (user_completed_tasks / user_assigned_tasks) * 100 if user_assigned_tasks != 0 else 0
                user_incomplete_percentage = (user_incomplete_tasks / user_assigned_tasks) * 100 if user_assigned_tasks != 0 else 0
                user_overdue_percentage = (user_overdue_tasks / user_assigned_tasks) * 100 if user_assigned_tasks != 0 else 0

                user_report.write(f"\nUsername: {username}\n")
                user_report.write(f"Total tasks assigned: {user_assigned_tasks}\n")
                user_report.write(f"Percentage of tasks completed: {user_completed_percentage:.2f}%\n")
                user_report.write(f"Percentage of tasks incomplete: {user_incomplete_percentage:.2f}%\n")
                user_report.write(f"Percentage of tasks overdue: {user_overdue_percentage:.2f}%\n")

    # Display Generate reports
    print("-"*80)
    print("Task Overview:")
    print(f"Total number of tasks: {num_tasks}")
    print(f"Total number of completed tasks: {num_completed_tasks}")
    print(f"Total number of uncompleted tasks: {num_incomplete_tasks}")
    print(f"Total number of overdue tasks: {num_overdue_tasks}")
    print(f"Percentage of tasks incomplete: {incomplete_percentage:.2f}%")
    print(f"Percentage of tasks overdue: {overdue_percentage:.2f}%")
    print("-"*80)         

def display_statistics(task_list, username_password):
    """Display statistics."""
    # Check if task_overview.txt and user_overview.txt files exist, if not, generate reports
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports(task_list, username_password)

    # Read and display task overview statistics
    with open("task_overview.txt", "r") as task_report:
        task_stats = task_report.read()
        print("Task Overview:")
        print(task_stats)

    # Read and display user overview statistics
    with open("user_overview.txt", "r") as user_report:
        user_stats = user_report.read()
        print("\nUser Overview:")
        print(user_stats)

    # Calculate various statistics based on task completion and deadlines
    num_tasks = len(task_list)
    num_completed_tasks = sum(1 for t in task_list if t['completed'])
    num_incomplete_tasks = num_tasks - num_completed_tasks
    num_overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'] < datetime.now())

    total_users = len(username_password)
    total_assigned_tasks = sum(1 for t in task_list if t['username'] != 'admin')
    total_completed_user_tasks = sum(1 for t in task_list if t['completed'] and t['username'] != 'admin')

    incomplete_percentage = (num_incomplete_tasks / num_tasks) * 100 if num_tasks != 0 else 0
    overdue_percentage = (num_overdue_tasks / num_tasks) * 100 if num_tasks != 0 else 0

    # Display task overview statistics
    print("-"*50)
    print("Task Overview:")
    print(f"Total number of tasks: {num_tasks}")
    print(f"Total number of completed tasks: {num_completed_tasks}")
    print(f"Total number of uncompleted tasks: {num_incomplete_tasks}")
    print(f"Total number of overdue tasks: {num_overdue_tasks}")
    print(f"Percentage of tasks incomplete: {incomplete_percentage:.2f}%")
    print(f"Percentage of tasks overdue: {overdue_percentage:.2f}%")
    print("-"*50)

    # Display user overview statistics
    print("User Overview:")
    print(f"Total number of users: {total_users}")
    print(f"Total number of tasks: {num_tasks}")
    print("User Task Assignment Statistics:")
    for username in username_password:
        if username != 'admin':
            user_assigned_tasks = sum(1 for t in task_list if t['username'] == username)
            user_completed_tasks = sum(1 for t in task_list if t['username'] == username and t['completed'])
            user_incomplete_tasks = user_assigned_tasks - user_completed_tasks
            user_overdue_tasks = sum(1 for t in task_list if t['username'] == username and not t['completed'] and t['due_date'] < datetime.now())

            user_completed_percentage = (user_completed_tasks / user_assigned_tasks) * 100 if user_assigned_tasks != 0 else 0
            user_incomplete_percentage = (user_incomplete_tasks / user_assigned_tasks) * 100 if user_assigned_tasks != 0 else 0
            user_overdue_percentage = (user_overdue_tasks / user_assigned_tasks) * 100 if user_assigned_tasks != 0 else 0

            print(f"\nUsername: {username}")
            print(f"Total tasks assigned: {user_assigned_tasks}")
            print(f"Percentage of tasks completed: {user_completed_percentage:.2f}%")
            print(f"Percentage of tasks incomplete: {user_incomplete_percentage:.2f}%")
            print(f"Percentage of tasks overdue: {user_overdue_percentage:.2f}%")
            print("-"*50)

# Main function
def main():
    # Initialize an empty task list
    task_list = []
    # Read task data from tasks.txt file and populate the task list
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)

    # Check if user file exists, if not, create it with default admin user
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    # Read user data from user.txt file and populate the username_password dictionary
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    # Flag to check if user is logged in
    logged_in = False
    while not logged_in:
        print("LOGIN")
        # Prompt for username and password
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        # Validate username and password
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True

    # Main menu loop
    while True:
        print()
        # Display different menu options based on user type
        if curr_user == 'admin':
            menu = input('''Select one of the following Options below:
r  -  Registering a user
a  -  Adding a task
va -  View all tasks
vm -  View my tasks
ds -  Display statistics
gr -  Generate reports
e  -  Exit
: ''').lower()
          
         
        else:
            menu = input('''Select one of the following Options below:
vm - View my tasks
e  - Exit
: ''').lower()

        # Perform actions based on selected menu option
        if curr_user == 'admin':
            if menu == 'r':
                register_user(username_password)
            elif menu == 'a':
                add_task(task_list)
            elif menu == 'va':
                view_all(task_list)
            elif menu == 'vm':
                view_my_tasks(curr_user, task_list)
            elif menu == 'ds':
                display_statistics(task_list, username_password)
            elif menu == 'gr':
                generate_reports(task_list, username_password)
            elif menu == 'e':
                print('Goodbye!!!')
                break
            else:
                print("Invalid option")
        else:
            if menu == 'vm':
                view_my_tasks(curr_user, task_list)
            elif menu == 'e':
                print('Goodbye!!!')
                break
            else:
                print("Invalid option")

# Execute the main function if this script is run directly
if __name__ == "__main__":
    main()