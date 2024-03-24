import os

# Get the current working directory
base_dir = os.getcwd()

# List all scripts in the src directory
scripts_dir = os.path.join(base_dir, "src")
scripts = [f for f in os.listdir(scripts_dir) if f.endswith('.py')]

# Create a menu for the user to select a script
print("Please select a script to run:")
for i, script in enumerate(scripts, 1):
    print(f"{i}. {script}")

# Get user's choice
user_choice = int(input("Enter your choice: ")) - 1

# Run the selected script
os.system(f"python {os.path.join(scripts_dir, scripts[user_choice])}")