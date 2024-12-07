'''
# Credits: Jaison J,
#          e-Yantra, IIT Bombay
# CDate:   7-Dec-2024
'''

# library required
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, TextBox

# global values
close_flag = 0
value_from_slider = 0

# Function to exit plot
def exit_plot(event):
    global close_flag
    close_flag = 1

# Function to update the plot based on slider value
def update(val):
    global value_from_slider
    value_from_slider = val


# Main loop
def plotData():
    global value_from_slider, close_flag
    x, y = [], []
    time_val = 0
    
    # Enable interactive mode
    plt.ion()

    # Create the figure and axis
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_axes([0.2, 0.65, 0.7, 0.3])

    # Plot initialization
    line, = ax.plot([], [], color='b')  # Create an empty line
    ax.set_xlim(0, 5)  # Initial x-axis range
    ax.set_ylim(0, 100)  # CPU percentage range (0-100%)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Error (m)")
    ax.set_title("Pitch Error Timeflow")

    ax2 = fig.add_axes([0.2, 0.15, 0.7, 0.3])
    line2, = ax2.plot([], [], color='b')  # Create an empty line
    ax2.set_xlim(0, 5)  # Initial x-axis range
    ax2.set_ylim(0, 100)  # CPU percentage range (0-100%)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Error (m)")
    ax2.set_title("Yaw Error Timeflow")

    # Add a button to the plot
    ax_button = plt.axes([0.92, 0.92, 0.05, 0.04])  # Position of the button: [left, bottom, width, height]
    button = Button(ax_button, 'Exit')  # Label of the button

    # Add TextBox widgets for user input PITCH
    setpointTBPitch = plt.axes([0.083, 0.85, 0.05, 0.03])  # Position of the first text box
    setpoint_TBPitch = TextBox(setpointTBPitch, 'Setpoint: ', initial="0")

    # Add TextBox widgets for user input YAW
    setpointTBYaw = plt.axes([0.083, 0.45, 0.05, 0.03])  # Position of the first text box
    setpoint_TBYaw = TextBox(setpointTBYaw, 'Setpoint: ', initial="0")

    # Link to each UX
    button.on_clicked(exit_plot)
    

    while True:
        try:
            setpointPitch = int(setpoint_TBPitch.text)
            setpointYaw = int(setpoint_TBPitch.text)
        except:
            setpointPitch = 0
            setpointYaw = 0

        # Update data
        x.append(time_val)
        y.append(setpointPitch)

        # Adjust line data
        line.set_data(x, y)
        line2.set_data(x, y)

        # Dynamically adjust axis limits
        ax.set_xlim(left = max(0, time_val-1), right = time_val+0.1)
        ax2.set_xlim(left = max(0, time_val-1), right = time_val+0.1)

        # Redraw the canvas
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Wait before the next update
        time.sleep(0.1)
        time_val += 0.1

        # If exit button is pressed
        if close_flag:
            print("Exiting...")
            plt.close(fig)
            break


if __name__ == "__main__":
    try:
        plotData()
    except Exception as error:
        print("Error occured: ", error)
    finally:
        print("Exited")