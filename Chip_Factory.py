import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# To store references to the textboxes
textboxes = []
ddlChip = None  # Will hold the reference to the ddlChip combobox
result_label = None  # Label to display the result

def targetChipDDL():
    global ddlChip

    # Create label for selecting chip value
    Chip = tk.Label(root, text="Target Chip Level:")
    Chip.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    # Create a Combobox (drop-down)
    ddlChip = ttk.Combobox(root)
    ddlChip['values'] = ("1", "2", "3", "4", "5", "6")
    ddlChip.current(0)  # Set the default value to 1
    ddlChip.grid(row=0, column=1, padx=5, pady=5)

    # Bind the selection event to create additional textboxes
    ddlChip.bind("<<ComboboxSelected>>", lambda event: add_calculate_button(create_comboboxes(int(ddlChip.get()) - 1)))

def create_comboboxes(num):
    global textboxes
    textboxes.clear()  # Clear the previous list of textboxes

    # Clear any existing widgets in the combobox_frame
    for widget in combobox_frame.winfo_children():
        widget.destroy()

    # Create instruction label
    instruction_label = tk.Label(combobox_frame, text="Enter the number of existing chips at each level:")
    instruction_label.grid(row=0, column=0, columnspan=2, padx=5, pady=(10, 5))

    # Create num textboxes with labels
    for i in range(num):
        # Create a label for the textbox
        chip_label = tk.Label(combobox_frame, text=f"Level {i+1} Chips:")
        chip_label.grid(row=i+1, column=0, padx=5, pady=5, sticky='w')

        # Create a textbox to the right of the label
        chip_text_box = tk.Entry(combobox_frame, width=10)
        chip_text_box.grid(row=i+1, column=1, padx=5, pady=5)
        
        # Store a reference to the textbox
        textboxes.append(chip_text_box)

    # Return the number of rows created (for placing the calculate button)
    return num

def add_calculate_button(num_rows):
    # Remove any existing widgets in the button_frame
    for widget in button_frame.winfo_children():
        widget.destroy()

    # Create and place the calculate button
    calculate_chips = tk.Button(button_frame, text="Calculate", command=calculate_action)
    calculate_chips.grid(row=0, column=0, padx=5, pady=10)

    # Create a label to display the result
    global result_label
    result_label = tk.Label(button_frame, text="", fg="blue", font=("Helvetica", 12))
    result_label.grid(row=1, column=0, padx=5, pady=5)

def calculate_action():
    try:
        # Grab the value selected in the Combobox (ddlChip)
        selected_value = int(ddlChip.get())
        target_level = selected_value

        # Initialize the list to store the number of required chips at each level
        required_chips = [0] * (target_level + 1)  # Indexing from 0 to target_level
        user_chips = [0] * (target_level + 1)      # Indexing from 0 to target_level

        # Populate user_chips with the player's existing chips
        # textboxes correspond to levels 1 to target_level - 1
        for i, textbox in enumerate(textboxes):
            textbox_value = textbox.get()
            chip_count = int(textbox_value) if textbox_value.isdigit() else 0
            user_chips[i + 1] = chip_count  # i + 1 because levels start from 1

        # Assume player has 0 chips at the target level if not specified
        user_chips[target_level] = 0

        # Set required chips at the target level to 1
        required_chips[target_level] = max(0, 1 - user_chips[target_level])

        # Calculate required chips for each level from target_level down to 1
        for level in range(target_level - 1, 0, -1):
            # Chips needed at this level to produce the required higher-level chips
            needed = required_chips[level + 1] * 2
            # Subtract the player's existing chips at this level
            required_chips[level] = max(0, needed - user_chips[level])

        # The number of +1 chips needed is the required_chips at level 1
        total_plus_one_chips_needed = required_chips[1]

        # Output the result in the GUI
        result_text = f"You need {total_plus_one_chips_needed} +1 chips to create a +{target_level} chip."
        result_label.config(text=result_text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Main window
root = tk.Tk()
root.title("Chip Factory")

# Frame to hold dynamically generated textboxes
combobox_frame = tk.Frame(root)
combobox_frame.grid(row=1, column=0, columnspan=2, pady=10)

# Frame to hold the calculate button and result label
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=2)

# Call function to create initial Combobox
targetChipDDL()

# Start the Tkinter event loop
root.mainloop()
