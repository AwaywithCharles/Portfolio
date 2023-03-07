"""
Title: High Templar
Author: Charles Bostwick
Website: www.AwaywithCharles.com
GitHub: https://github.com/AwaywithCharles
License: MIT

This program allows you to change the MAC address of your network interface on Windows 11. 
In the future I will add support for other operating systems, making it cross-platform.

I create this program as a way to learn some different aspects of Python programming.
I also wanted to create a program that I could use to change the MAC address
of my network interface to test and use on my Home Lab.

To use this program, you must have Python 3 and the following packages installed:
- tkinter
- netifaces

To install these packages, you can use pip, which is the package installer for Python. To enable pip on Windows 11:

1. Open a command prompt window by typing "cmd" into the Windows search bar and selecting the Command Prompt app.
2. Type "python" into the command prompt and press Enter. This should open the Python interpreter.
3. Type "import ensurepip" and press Enter. This will enable pip on your system.
4. Type "exit()" and press Enter to exit the Python interpreter.

You also need to setup the PATH environment variable to include the path to your Python installation's "Scripts" folder. To do this:
Open the Start Menu and search for "Environment Variables".
Click on "Edit the system environment variables".
Click on the "Environment Variables" button in the "Advanced" tab.
Under "System variables", find the "Path" variable and click "Edit".
Click "New" and add the path to your Python installation's "Scripts" folder (e.g., "C:\Python39\Scripts").
Click "OK" on all windows to save the changes.
Open a new command prompt and type "pip" to verify that pip is installed and working.

Once pip is enabled, you can install the required packages by typing the following commands into the command prompt:
- "pip install tkinter"
- "pip install netifaces"

To run the High Templar MAC Changer program, navigate to the directory where the program is saved and run the following command in the command prompt:
- "python HighTemplarMACChanger.py"

Usage:
1. Select the network interface you want to change the MAC address of from the drop-down menu.
2. The original MAC address of the interface will be displayed in the "Original MAC address" field.
3. To change the MAC address to a new address, enter the new address in the "New MAC address" field and click the "Change MAC" button.
4. To randomize the MAC address, click the "Randomize MAC" button.

Note: This program requires administrative privileges to change the MAC address.
"""
import tkinter as tk
import tkinter.messagebox as mbox
import os
import netifaces as ni
import random

class MACChanger:
    def __init__(self, master):
        self.master = master       

        # Title and background color of the window
        master.title("High Templar")
        master.configure(bg="black")
        
        # Set the width and height of the window
        window_width = 580
        window_height = 420

        # Get the width and height of the screen
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the geometry of the window
        master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Define the ASCII art and text to display above the drop down menu
        ascii_art = r"""
        _   _ _       _       _____                    _            
        | | | (_)     | |     |_   _|                  | |           
        | |_| |_  __ _| |__     | | ___ _ __ ___  _ __ | | __ _ _ __ 
        |  _  | |/ _` | '_ \    | |/ _ \ '_ ` _ \| '_ \| |/ _` | '__|
        | | | | | (_| | | | |   | |  __/ | | | | | |_) | | (_| | |   
        \_| |_/_|\__, |_| |_|   \_/\___|_| |_| |_| .__/|_|\__,_|_|   
                    __/ |                          | |                 
                   |___/                           |_|         
        """

        text = "High Templar: A MAC address changer for Windows 11"

        # Add labels for the ASCII art and text above the drop down menu
        self.ascii_art_label = tk.Label(master, text=ascii_art, fg="gold", bg="black", font="TkFixedFont")
        self.ascii_art_label.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky="w")

        self.title_label = tk.Label(master, text=text, fg="gold", bg="black", font=("TkDefaultFont", 14, "bold"))
        self.title_label.grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky="w")

        # Add labels and drop down menu for interface selection
        self.interfaces_label = tk.Label(master, text="Select an interface:", fg="gold", bg="black")
        self.interfaces_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.interfaces_var = tk.StringVar()
        self.interface_dropdown = tk.OptionMenu(master, self.interfaces_var, *self.get_interfaces(), command=self.update_mac_address)
        self.interface_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Add labels and entry fields for MAC addresses
        self.original_mac_label = tk.Label(master, text="Original MAC address:", fg="gold", bg="black")
        self.original_mac_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.original_mac_var = tk.StringVar()
        self.original_mac_entry = tk.Entry(master, textvariable=self.original_mac_var, state="readonly")
        self.original_mac_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.current_mac_label = tk.Label(master, text="Current MAC address:", fg="gold", bg="black")
        self.current_mac_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.current_mac_var = tk.StringVar()
        self.current_mac_entry = tk.Entry(master, textvariable=self.current_mac_var, state="readonly")
        self.current_mac_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.new_mac_label = tk.Label(master, text="New MAC address:", fg="gold", bg="black")
        self.new_mac_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.new_mac_var = tk.StringVar()
        self.new_mac_entry = tk.Entry(master, textvariable=self.new_mac_var)
        self.new_mac_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Add buttons to change and randomize the MAC address
        self.change_button = tk.Button(master, text="Change MAC", fg="gold", bg="black", command=self.change_mac)
        self.change_button.grid(row=7, column=0, padx=5, pady=5, sticky="e")

        self.randomize_button = tk.Button(master, text="Randomize MAC", fg="gold", bg="black", command=self.randomize_mac)
        self.randomize_button.grid(row=6, column=0, padx=5, pady=5, sticky="e")

        self.get_all_mac_button = tk.Button(master, text="Get MAC address", fg="gold", bg="black", command=self.get_all_mac_addresses)
        self.get_all_mac_button.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        # Initialize the interface and MAC address variables
        self.interface = None
        self.original_mac = None
        self.current_mac = None
        self.new_mac = None

        # Set the interface and MAC address variables to the default values
        if ni.gateways()['default']:
            self.interface = ni.gateways()['default'][ni.AF_INET][1]
        self.original_mac = self.get_mac_address()
        self.current_mac = self.original_mac
        self.new_mac = self.generate_random_mac()

        # Set the MAC address variables to their respective values
        self.set_mac_addresses()
        
        # Add a button to revert the MAC address to its original value
        self.revert_button = tk.Button(master, text="Revert to original MAC", fg="gold", bg="black", command=self.revert_mac)
        self.revert_button.grid(row=7, column=0, padx=5, pady=5, sticky="w")

    def get_interfaces(self):
        # Get a list of available network interfaces
        interfaces = ni.interfaces()
        # Define a dictionary to map interface names to labels
        interface_labels = {"eth0": "Ethernet 1", "eth1": "Ethernet 2", "wlan0": "Wireless"}
        # Replace interface names with labels if they exist in the dictionary
        labeled_interfaces = [interface_labels.get(interface, interface) for interface in interfaces]
        return labeled_interfaces

    def get_mac_address(self):
        # Get the MAC address of the selected network interface
        if os.name == "nt":
            for line in os.popen("ipconfig /all"):
                if self.interface in line:
                    # Return the MAC address without any separators
                    return line.split()[-1].replace("-", "")
        else:
            return ni.ifaddresses(self.interface)[ni.AF_LINK][0]['addr']
        
    def update_mac_address(self, *args):
        # Update the current MAC address variable and set the MAC address fields to their respective values
        self.interface = self.interfaces_var.get()
        self.original_mac = self.get_mac_address()
        self.current_mac = self.original_mac
        self.new_mac = self.generate_random_mac()
        self.set_mac_addresses()

    def generate_random_mac(self):
        # Generate a random MAC address and return it as a string
        mac = [random.randint(0x00, 0xff) for _ in range(6)]
        mac[0] = mac[0] & 0xfc  # Set the "locally administered" bit
        # Convert the MAC address to a string and format it with colons
        return ":".join(["{:02x}".format(x) for x in mac])

    def randomize_mac(self):
        # Generate a random MAC address and assign it to self.new_mac
        self.new_mac = self.generate_random_mac()
        self.new_mac_var.set(self.new_mac)

    def set_mac_addresses(self):
        # Set the values of the MAC address fields based on the values of self.original_mac, self.current_mac, and self.new_mac
        self.original_mac_var.set(self.original_mac)
        self.current_mac_var.set(self.current_mac)
        self.new_mac_var.set(self.new_mac)

    def change_mac(self):
        # Change the MAC address of the selected network interface to the value in self.new_mac
        if os.name == "nt":
            # Use the Windows "netsh" command to change the MAC address
            os.system("netsh interface set interface \"" + self.interface + "\" newmac \"" + self.new_mac + "\"")
        else:
            # Use the Linux "ifconfig" command to change the MAC address
            os.system("ifconfig " + self.interface + " hw ether " + self.new_mac)

        # Update the current MAC address variable and set the MAC address fields to their respective values
        self.current_mac = self.new_mac
        self.set_mac_addresses()

    def get_all_mac_addresses(self):
    # Get all the MAC addresses for the current computer/user
        interfaces = ni.interfaces()
        for interface in interfaces:
            all_macs = ni.ifaddresses(interface)
            if ni.AF_LINK in all_macs:
                mac_address = all_macs[ni.AF_LINK][0]['addr']
                if interface == self.interface:
                    # Update the original and current MAC addresses with the value of the currently selected interface
                    self.original_mac = mac_address
                    self.current_mac = mac_address
                print(f"{interface}: {mac_address}")
        # Update the MAC address fields to their respective values
        self.set_mac_addresses()
    
    def revert_mac(self):
        # Revert the MAC address to its original value
        self.new_mac = self.original_mac
        self.change_mac()

if __name__ == "__main__":
    root = tk.Tk()
    app = MACChanger(root)
    root.mainloop()
