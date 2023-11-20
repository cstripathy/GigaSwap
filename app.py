import subprocess

def get_current_swap_info():
    try:
        result = subprocess.run(['free', '-h'], capture_output=True, text=True)
        print("Current Swap Information:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error getting current swap information: {e}")

def increase_swap(size_in_gb):
    try:
        # Display current swap information
        get_current_swap_info()

        # Confirm with the user before proceeding
        confirmation = input(f"\nDo you want to change swap memory to {size_in_gb}GB? (yes/no): ").lower()
        if confirmation != 'yes':
            print("Operation aborted. No changes made.")
            return

        # Calculate the swap size in MB
        swap_size = size_in_gb * 1024

        # Turn off all swap processes
        subprocess.run(['sudo', 'swapoff', '-a'])

        # Resize the swap file
        subprocess.run(['sudo', 'fallocate', '-l', f'{swap_size}M', '/swapfile'])

        # Set up the swap area
        subprocess.run(['sudo', 'mkswap', '/swapfile'])

        # Activate the swap
        subprocess.run(['sudo', 'swapon', '/swapfile'])

        # Update the fstab file to make the changes permanent
        with open('/etc/fstab', 'a') as file:
            file.write('/swapfile none swap sw 0 0\n')

        print(f"\nSwap memory changed to {size_in_gb}GB successfully.")

        # Display new swap information
        get_current_swap_info()

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Enter the desired size of swap memory in GB
swap_size_gb = 8  # Change this value to the desired size

increase_swap(swap_size_gb)
