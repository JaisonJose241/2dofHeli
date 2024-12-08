'''
# Credits: Jaison J,
#          e-Yantra, IIT Bombay
# CDate:   7-Dec-2024
'''

# library required
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, TextBox
from twodofhelimodel import dynamicsCalc

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

    x, y1, y2 = [], [], []
    PerrorList, YerrorList = [], []
    time_val = 0
    Perror, Yerror = 0, 0
    
    # Enable interactive mode
    plt.ion()

    # Create the figure and axis
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_axes([0.2, 0.65, 0.7, 0.3])

    # Plot initialization
    line, = ax.plot([], [], color='b')  # Create an empty line
    errorLineP, = ax.plot([], [], color='r')  # Create an empty line
    ax.set_xlim(0, 5)  # Initial x-axis range
    ax.set_ylim(0, 100)  # range (0-100%)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Error (m)")
    ax.set_title("Pitch Error vs Time")

    ax2 = fig.add_axes([0.2, 0.15, 0.7, 0.3])
    line2, = ax2.plot([], [], color='b')  # Create an empty line
    errorLineY, = ax2.plot([], [], color='r')  # Create an empty line
    ax2.set_xlim(0, 5)  # Initial x-axis range
    ax2.set_ylim(0, 100)  # range (0-100%)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Error (m)")
    ax2.set_title("Yaw Error vs Time")

    # Add a button to the plot
    ax_button = plt.axes([0.92, 0.92, 0.05, 0.04])  # Position of the button: [left, bottom, width, height]
    button = Button(ax_button, 'Exit')  # Label of the button

    # Add TextBox widgets for user input PITCH
    setpointTBPitch = plt.axes([0.083, 0.85, 0.05, 0.03])  # Position of the first text box
    setpoint_TBPitch = TextBox(setpointTBPitch, 'Setpoint: ', initial="0")

    # PID for Pitch
    PTBPitch = plt.axes([0.083, 0.75, 0.05, 0.03])  # Position of the first text box
    P_TBPitch = TextBox(PTBPitch, 'P: ', initial="0")
    ITBPitch = plt.axes([0.083, 0.7, 0.05, 0.03])  # Position of the first text box
    I_TBPitch = TextBox(ITBPitch, 'I: ', initial="0")
    DTBPitch = plt.axes([0.083, 0.65, 0.05, 0.03])  # Position of the first text box
    D_TBPitch = TextBox(DTBPitch, 'D: ', initial="0")

    # Add TextBox widgets for user input YAW
    setpointTBYaw = plt.axes([0.083, 0.35, 0.05, 0.03])  # Position of the first text box
    setpoint_TBYaw = TextBox(setpointTBYaw, 'Setpoint: ', initial="0")

    # PID for Yaw
    PTBYaw = plt.axes([0.083, 0.25, 0.05, 0.03])  # Position of the first text box
    P_TBYaw = TextBox(PTBYaw, 'P: ', initial="0")
    ITBYaw = plt.axes([0.083, 0.2, 0.05, 0.03])  # Position of the first text box
    I_TBYaw = TextBox(ITBYaw, 'I: ', initial="0")
    DTBYaw = plt.axes([0.083, 0.15, 0.05, 0.03])  # Position of the first text box
    D_TBYaw = TextBox(DTBYaw, 'D: ', initial="0")

    # Link to each UX
    button.on_clicked(exit_plot)
    

    while True:

        # check for invalid content
        try:
            setpointPitch = int(setpoint_TBPitch.text)
            P_TBPitchVal  = int(P_TBPitch.text)
            I_TBPitchVal  = int(I_TBPitch.text)
            D_TBPitchVal  = int(D_TBPitch.text)
        except:
            setpointPitch = 0
            P_TBPitchVal  = 0
            I_TBPitchVal  = 0
            D_TBPitchVal  = 0

        try:
            setpointYaw = int(setpoint_TBYaw.text)
            P_TBYawVal  = int(P_TBYaw.text)
            I_TBYawVal  = int(I_TBYaw.text)
            D_TBYawVal  = int(D_TBYaw.text)
        except:
            setpointYaw = 0
            P_TBYawVal  = 0
            I_TBYawVal  = 0
            D_TBYawVal  = 0

        # Update data
        x.append(time_val)
        y1.append(setpointPitch)
        y2.append(setpointYaw)

        # Adjust line data
        line.set_data(x, y1)
        line2.set_data(x, y2)

        # error line update
        PerrorList.append(Perror)
        YerrorList.append(Yerror)
        
        errorLineP.set_data(x, Perror)
        errorLineY.set_data(x, Yerror)

        # Dynamically adjust axis limits
        ax.set_xlim(left = max(0, time_val-2), right = time_val+0.1)
        ax2.set_xlim(left = max(0, time_val-2), right = time_val+0.1)

        # Redraw the canvas
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Wait before the next update
        time.sleep(0.1)
        time_val += 0.1

        # Update all values
        PIDgainsPitch = [P_TBPitchVal, I_TBPitchVal, D_TBPitchVal]
        PIDgainsYaw   = [P_TBYawVal, I_TBYawVal, D_TBYawVal]
        
        Perror, Yerror = dynamicsCalc(time_val, setpointPitch, setpointYaw, PIDgainsPitch, PIDgainsYaw)

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