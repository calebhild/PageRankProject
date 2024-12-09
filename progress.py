import sys
import time
'''Comments are placed to the right of each line.'''
class Progress:
    def __init__(self, total, title="Progress", width=80, update_frequency=10):
        """Initialize the Progress bar
        
        Parameters:
        total (int) -- Maximum value of the counter (total steps)
        title (str) -- Information to be displayed alongside the progress bar
        width (int) -- Width of the display progress bar
        update_frequency (int) -- Frequency of updates to avoid excessive writing
        """
        self.counter = 0                                 # Initialize progress counter to 0
        self.total = total                               # Total value for the counter to reach
        self.title = title                               # Custom title for the progress bar
        self.width = width                               # Width for the progress bar
        self.update_frequency = update_frequency         # How often to update the progress bar
        self.start_time = time.time()                    # Track the start time

    def __iadd__(self, value):
        """Increase the current counter by a specified value
        
        Parameters:
        value (int) -- Value to increment the progress counter by
        """
        self.counter += value                             # Increase the counter
        return self

    def show(self):
        """Display the progress bar in its current state
        
        This method shows the progress percentage and elapsed time, as well as a graphical
        representation of the progress bar.
        """
        # Only update the progress bar every `update_frequency` steps
        if self.counter % self.update_frequency != 0:     # Skip updates for non-multiples of frequency
            return                                        # Skip updating the progress bar if we're not at the specified frequency
        
        sec = time.time() - self.start_time               # Calculate elapsed time since the start
        percent = 100 * self.counter / self.total         # Calculate completion percentage
        
        # Create the title string with the progress information
        title = f'{self.title} ({percent:.0f}% {sec//60:02.0f}:{sec%60:02.0f}) '
        
        # Ensure the title fits within the progress bar width
        if len(title) >= self.width:
            raise ValueError("Progress bar does not fit width. Shorten title or increase width.")
        
        # Calculate the width of the progress bar and its current completion
        bar_width = self.width - len(title) - 3
        full_width = int(bar_width * self.counter / self.total)
        empty_width = bar_width - full_width
        
        # Output the progress bar to the console
        sys.stdout.write('\r' + title + '[' + full_width * '#' + empty_width * '.' + ']')
        sys.stdout.flush()                                 # Ensure immediate output to the console

    def finish(self):
        """Finish the progress bar and clear the line"""
        sys.stdout.write('\r' + self.width * ' ' + '\r')   # Clear the line after completion
        sys.stdout.flush()

# Example usage
prog = Progress(100, "Running task", update_frequency=10)  # Update progress bar every 10 steps
for step in range(100):
    time.sleep(0.1)                                        # Simulate a task with a delay
    prog += 1                                              # Increment progress
    prog.show()                                            # Update progress bar display
prog.finish()                                              # Finish and clear progress bar line
