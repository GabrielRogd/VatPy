import os


def fetch_python_scripts(directory):
    return [f for f in os.listdir(directory) if f.endswith('.py')]


def user_choice_menu(scripts):
    while True:
        print("\nPlease select a script to run:")
        for i, script in enumerate(scripts, 1):
            print(f"{i}. {script}")
        user_choice = input("Enter your choice: ")
        if user_choice.isdigit() and 0 < int(user_choice) <= len(scripts):
            return int(user_choice) - 1
        else:
            print(f"\nInvalid input. Please choose between 1 and {i}.")


def execute_script(directory, script_name):
    os.system(f"python3 {os.path.join(directory, script_name)}")


base_dir = os.getcwd()
scripts_dir = os.path.join(base_dir, "src")

while True:
    scripts = fetch_python_scripts(scripts_dir)
    user_choice = user_choice_menu(scripts)
    execute_script(scripts_dir, scripts[user_choice])
