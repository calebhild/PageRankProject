import sys
import time

class Progress:
    def __init__(self, total, title="Progress", width=80):
        """Initialise the Progress bar
        
        Parameters:
        total (int) -- Maximum value of the counter (total steps)
        title (str) -- Information to be displayed alongside the progress bar
        width (int) -- Width of the display progress bar
        """
        self.counter = 0                                                                     # Initialise progress counter to 0
        self.total = total                                                                   # Total value for the counter to reach
        self.title = title                                                                   # Custom title for the progress bar
        self.width = width                                                                   # Width for the progress bar
        self.start_time = time.time()                                                        # Record the start time for elapsed time tracking

    def __iadd__(self, value):
        """Increase the current counter by a specified value
        
        Parameters:
        value (int) -- Value to increment the progress counter by
        """
        self.counter += value                                                                # Increase the counter
        return self

    def show(self):
        """Display the progress bar in its current state
        
        This method shows the progress percentage and elapsed time, as well as a graphical
        representation of the progress bar.
        """
        sec = time.time() - self.start_time                                                  # Elapsed time since the start of the task
        percent = 100 * self.counter / self.total                                            # Calculate completion percentage
        
        # Create the title string with the progress information
        title = f'{self.title} ({percent:.0f}% {sec//60:02.0f}:{sec%60:02.0f}) '
        
                                                                                             # Ensure the title fits within the progress bar width
        if len(title) >= self.width:
            raise ValueError("Progress bar does not fit width. Shorten title or increase width.")
        
                                                                                             # Calculate the width of the progress bar and its current completion
        bar_width = self.width - (len(title)) - 3
        full_width = int(bar_width * self.counter / self.total)
        empty_width = bar_width - full_width
        
                                                                                             # Output the progress bar to the console
        sys.stdout.write('\r' + title + '[' + full_width * '#' + empty_width * '.' + ']')
        sys.stdout.flush()                                                                   # Ensure immediate output to the console

    def finish(self):
        """Finish the progress bar and clear the line"""
        sys.stdout.write('\r' + self.width * ' ' + '\r')                                     # Clear the line after completion
        sys.stdout.flush()

                                                                                             # Example usage
prog = Progress(100, "Running task")                                                         # Initialize progress bar for 100 steps
for step in range(100):
    time.sleep(0.1)                                                                          # Simulate a task with a delay
    prog += 1                                                                                # Increment progress
    prog.show()                                                                              # Update progress bar display
prog.finish()                                                                                # Finish and clear progress bar line
