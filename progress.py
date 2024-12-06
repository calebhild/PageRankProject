import sys
import time

class Progress:
    """Progress bar object for the command line

    This class allows you to conveniently add progress bars to long-running
    calculations. It writes textual and graphical information about
    the progress to sys.stderr. It can be used in the following way:

    >>> prog = Progress(100, "Performing some long running task")
    >>> for step in some_long_calculation():
    >>>     prog += 1
    >>>     prog.show()
    >>> prog.finish()

    The progress bar displays the percentage of completion
    (counter/total) and the real-time taken by the calculation so far.
    """
    
    def __init__(self, total, title="Progress", width=80):
        """Initialize the Progress bar
        
        Parameters:
        total (int) -- Maximum value of the counter (total steps)
        title (str) -- Information to be displayed alongside the progress bar
        width (int) -- Width of the display progress bar
        """
        self.counter = 0  # Initialize progress counter to 0
        self.total = total  # Total value for the counter to reach
        self.title = title  # Custom title for the progress bar
        self.width = width  # Width for the progress bar
        self.start_time = time.time()  # Record the start time for elapsed time tracking

    def __iadd__(self, value):
        """Increase the current counter by a specified value
        
        Parameters:
        value (int) -- Value to increment the progress counter by
        """
        self.counter += value  # Increase the counter
        return self

    def show(self):
        """Display the progress bar in its current state
        
        This method shows the progress percentage and elapsed time, as well as a graphical
        representation of the progress bar.
        """
        sec = time.time() - self.start_time  # Elapsed time since the start of the task
        percent = 100 * self.counter / self.total  # Calculate completion percentage
        
        # Create the title string with the progress information
        title = f'{self.title} ({percent:.0f}% {sec//60:02.0f}:{sec%60:02.0f}) '
        
        # Check if the title fits within the progress bar width, raise an error if it doesn't
        if len(title) >= self.width:
            raise ValueError("Progress bar does not fit width. Shorten title or increase width.")
        
        # Calculate the width of the progress bar and its current completion
        bar_width = self.width - (len(title)) - 3
        full_width = int(bar_width * self.counter / self.total)
        empty_width = bar_width - full_width
        
        # Output the progress bar to the console
        sys.stdout.write('\r' + title + '[' + full_width * '#' + empty_width * '.' + ']')
        sys.stdout.flush()  # Ensure immediate output to the console

    def finish(self):
        """Finish the progress bar and clear the line"""
        sys.stdout.write('\r' + self.width * ' ' + '\r')  # Clear the line after completion
        sys.stdout.flush()
