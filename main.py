#-----------------------------This is Portfolio Project 5 of 100 Days of Code on Udemy ---------------------------#
#----------------------------- Created on 2/15/2022 by Gavra J Buckman --------------------------------------------#
#--------All code is mine.  I certify that I did not copy or plagiarize anyone else's work------------------------#
# Requirement is to create a typing speed testing using Tkinter


# ---------------------------- IMPORT STATEMENTS ------------------------------- #
import random
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font

# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = 'Helvetica'
TEXT_FONT_SIZE = 20
TOP_FRAME_FONT = (FONT_NAME, 10)
TEXT_FONT = (FONT_NAME, TEXT_FONT_SIZE)
RESULTS_FONT_SIZE = 15
WHITE = '#FFFFFF'
NEON_GREEN = '#39FF14'
BLUE = '#0000FF'
RED = '#FF0000'
HIGHLIGHT_TAG = 'hl'
CORRECT_TAG = 'correct'
INCORRECT_TAG = 'error'
SPACE_REX = '\s'
NUM_REX = '\d+\.?\d*\s'
LINE_WIDTH = 44
SECONDS = 60

# ---------------------------- FUNCTIONS ------------------------------- #



# ---------------------------- CLASSES ------------------------------- #
# Top level application, or root
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Typing Speed Test')
        self.geometry('600x500')
        self.resizable(False, False)

        self.stat_frame = None
        self.text_frame = None
        self.results_frame = None
        self.word_lines = ''
        self.timer = None
        self.statistics = None
        self.best_cpm = '0'

        # Open the file containing the 5000 most common words in English language and read each line into a list
        with open(file="words.csv") as file:
            self.words = file.read().splitlines()

        # Create and display the typing test widgets
        self.create_typing_test()

    def create_typing_test(self):
        # Shuffle the word list so they are in a different order each time the test begins
        random.shuffle(self.words)

        # Create a string with the words to be used as input data for the text box
        word_string = ' '.join(self.words)
        # Create lines to be used for scrolling in text box based on the width of the text box
        index_of_space = 0
        first_index = 0
        length = len(word_string)
        for i in range(0, length, LINE_WIDTH):
            # Check if this is the last line, if so just add the rest of the text to the end of the string
            if length - i < LINE_WIDTH:
                self.word_lines += word_string[first_index:]
            else:
                index_of_space = word_string[0:first_index + LINE_WIDTH].rindex(' ')
                self.word_lines += word_string[first_index:index_of_space] + '\n'
                first_index = index_of_space + 1

        # Create initial frames
        self.stat_frame = StatFrame(self)
        self.stat_frame.pack(side=tk.TOP)
        self.text_frame = TextFrame(self)
        self.text_frame.pack()

    def start_timer(self, event):
        if self.timer is None:
            self.statistics = Statistics()
            self.countdown(SECONDS)

    def reset(self):
        # Check if there are already frames created, if so destroy them
        if self.stat_frame is not None:
            self.stat_frame.destroy()

        if self.text_frame is not None:
            self.text_frame.destroy()

        if self.results_frame is not None:
            self.results_frame.destroy()

        # Initialize statistics and word text
        self.statistics = None
        self.word_lines = ''

        # Cancel the timer
        if self.timer is not None:
            self.after_cancel(self.timer)
            self.timer = None
        self.create_typing_test()

    def countdown(self, count):
        # Populate all of the statistics in the stats frame with the ongoing stats
        self.stat_frame.time_value.config(text=count)
        self.statistics.calculate_stats(self.text_frame.typed_correct_list, self.text_frame.typed_incorrect_dict)
        self.stat_frame.wpm_value.config(text=self.statistics.wpm)
        self.stat_frame.cpm_value.config(text=self.statistics.num_correct_chars)

        if count > 0:
            self.timer = self.after(1000, self.countdown, count - 1)
        else:
            self.text_frame.forget()
            self.results_frame = ResultsFrame(self)
            self.results_frame.pack()
            self.best_cpm = max(int(self.best_cpm), self.statistics.num_correct_chars)


# Class to hold all widgets in the top frame that show ongoing typing statistics
class StatFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Create all the labels
        self.best_text = ttk.Label(self, text="Your Best: ", font=TOP_FRAME_FONT)
        self.best_value = ttk.Label(self, )
        self.cpm_text = ttk.Label(self, text="Corrected CPM: ", font=TOP_FRAME_FONT)
        self.wpm_text = ttk.Label(self, text="WPM: ", font=TOP_FRAME_FONT)
        self.time_text = ttk.Label(self, text='Time left: ', font=TOP_FRAME_FONT)
        self.best_value = ttk.Label(self, text=parent.best_cpm, font=TOP_FRAME_FONT, width=4, background=WHITE)
        self.wpm_value = ttk.Label(self, text='?', font=TOP_FRAME_FONT, width=6, background=WHITE)
        self.cpm_value = ttk.Label(self, text='?', font=TOP_FRAME_FONT, background=WHITE, width=4)
        self.time_value = ttk.Label(self, text='', font=TOP_FRAME_FONT, width=3, background=WHITE)

        # Pack labels on grid
        self.best_text.pack(padx=5, side=tk.LEFT)
        self.best_value.pack(padx=5, side=tk.LEFT)
        self.cpm_text.pack(padx=5, side=tk.LEFT)
        self.cpm_value.pack(padx=5, side=tk.LEFT)
        self.wpm_text.pack(padx=5, side=tk.LEFT)
        self.wpm_value.pack(padx=5, side=tk.LEFT)
        self.time_text.pack(padx=5, side=tk.LEFT)
        self.time_value.pack(padx=5, side=tk.LEFT)

        # Create Reset button
        self.reset_btn = ttk.Button(self, text='Reset', command=self.parent.reset)
        self.reset_btn.pack(padx=5, side=tk.LEFT)

# Class to hold the actual typing test frame and widgets
class TextFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.typed_correct_list = []
        self.typed_incorrect_dict = {}
        text_font = font.Font(family=FONT_NAME, size=TEXT_FONT_SIZE)

        # Create the entry box the user will type in
        self.typed_words = tk.StringVar()
        self.typing_entry = tk.Entry(self, textvariable=self.typed_words, font=text_font, justify=tk.CENTER)
        self.typing_entry.grid(row=1, column=0, sticky=tk.EW, pady=10)

        # Create the words text box
        self.wordbox = tk.Text(self, width=36, height=2.5, borderwidth=0, relief=tk.FLAT, wrap=tk.WORD, font=text_font,
                               spacing2=5, spacing1=10, padx=5, pady=5, takefocus=0)

        # Get the first word in the string and derive the index of the last character to use in creating highlight tag
        first_word = self.parent.word_lines[:self.parent.word_lines.find(' ')]
        findex = '1.0'
        lindex = '1.'+str(len(first_word))
        #print(f"Last index is {lindex}")

        # Insert the text string and add to the grid
        self.wordbox.insert('1.0', self.parent.word_lines)
        self.wordbox.grid(row=0, column=0, sticky=tk.EW)

        # Create the tag to highlight the first word and configure the tag
        self.wordbox.tag_add(HIGHLIGHT_TAG, findex, lindex)
        self.wordbox.tag_configure(HIGHLIGHT_TAG, foreground=WHITE, background=NEON_GREEN)
        #print(self.wordbox.get(findex, f"{HIGHLIGHT_TAG}.last"))

        # When the user types the space key, check for the spelling accuracy and move to the next word
        self.typing_entry.bind('<space>', self.check_word)
        # When user clicks in the entry widget and then presses the first key, start the timer
        self.typing_entry.bind('<FocusIn><Key>', self.parent.start_timer)

    # Function that checks the last typed word against the master word list to determine accuracy and store whether \
    # The word was spelled correctly or incorrectly
    def check_word(self, event):
        # Get the last word typed
        last_word = self.typed_words.get().split()[-1]

        # Get the currently highlighted word from the textbox
        current_highlighted_word = self.wordbox.get(f"{HIGHLIGHT_TAG}.first", f"{HIGHLIGHT_TAG}.last")

        # Compare the two words to see if spelling is correct. If correct, add to the correct list and call function
        # to change the current word and tag the previous word with correct tag.  If incorrect, add to the incorrect
        # dictionary and tag with incorrect tag
        if last_word.lower() == current_highlighted_word.lower():
            self.change_current_word(last_word, CORRECT_TAG, BLUE)
            self.typed_correct_list.append(last_word)
        else:
            self.change_current_word(last_word, INCORRECT_TAG, RED)
            self.typed_incorrect_dict[last_word] = current_highlighted_word

    # This function moves the highlight to the next word
    def change_current_word(self, last_word, tag, color):
        # Derive all of the indexes, current and next
        current_findex = self.wordbox.index(f"{HIGHLIGHT_TAG}.first")
        current_lindex = self.wordbox.index(f"{HIGHLIGHT_TAG}.last")
        new_findex = current_lindex + '+1c'
        new_lindex = self.wordbox.search(pattern=SPACE_REX, index=new_findex, regexp=True)

        # Untag the word that is currently highlighted and highlight the new word
        self.wordbox.tag_remove(HIGHLIGHT_TAG, current_findex, current_lindex)
        self.wordbox.tag_add(HIGHLIGHT_TAG, new_findex, new_lindex)

        # Add a tag to color the old word based on whether it was correct or incorrect
        self.wordbox.tag_add(tag, current_findex, current_lindex)
        self.wordbox.tag_configure(tag, foreground=color)

        # Show the new line if necessary
        self.wordbox.see(new_findex+'+1l')

        # Empty the typing entry box
        self.typed_words.set('')


# Class to show the results at the end of the typing test
class ResultsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        text_font = font.Font(family=FONT_NAME, size=RESULTS_FONT_SIZE)

        # Create two text widgets - one holds the scores and the other holds the mistakes
        self.score_text = tk.Text(self, width=36, height=4, borderwidth=0, relief=tk.FLAT, wrap=tk.WORD, font=text_font,
                               padx=5, pady=10, takefocus=0)
        self.mistake_text = tk.Text(self, width=36, height=8, borderwidth=0, relief=tk.FLAT, wrap=tk.WORD,
                                    font=text_font, padx=5, pady=10, takefocus=0)

        # Insert the stats into the text box
        self.score_text.insert('1.0', self.parent.statistics.print_stats())
        # Add a tag to color the numbers
        # The IntVar holds the length of the matched pattern from the search
        num_chars = tk.IntVar()
        start_index = '1.0'
        num_searches = 3
        while num_searches > 0:
            # Find the index of the next number in the string
            index1 = self.score_text.search(NUM_REX, start_index, forwards=True, count=num_chars, regexp=True)
            if len(index1) > 0:
                # Derive the end index based on the count of number of characters found
                end_index = f"{index1}+{num_chars.get()}c"
                # Add the tag to that range of characters
                self.score_text.tag_add(CORRECT_TAG, index1, end_index)
                start_index = end_index
            num_searches -= 1

        # Configure the tag with special font and color to make it stand out
        self.score_text.tag_configure(CORRECT_TAG, foreground=BLUE, relief=tk.RAISED, font=('Impact', 20, 'bold'))
        # Insert the mistakes into the text box
        self.mistake_text.insert('1.0', self.parent.statistics.print_mistakes())
        self.score_text.pack()
        self.mistake_text.pack()


class Statistics:
    def __init__(self):
        self.num_correct_chars = 0
        self.num_incorrect_chars = 0
        self.incorrect_words = {}
        self.wpm = 0.0
        self.num_correct_words = 0
        self.num_incorrect_words = 0
        self.total_words = 0

    def calculate_stats(self, correct_words, incorrect_words):
        self.num_correct_chars = len(''.join(correct_words))
        self.num_incorrect_chars = len(''.join(incorrect_words))
        self.incorrect_words = incorrect_words
        self.wpm = "{:.2f}".format(self.num_correct_chars / 5)
        self.num_correct_words = len(correct_words)
        self.num_incorrect_words = len(incorrect_words)
        self.total_words = self.num_incorrect_words + self.num_correct_words

    def print_stats(self):
        if self.total_words == 0:
            return "You didn't type anything. Please click the Reset Button to try again."

        accuracy_percentage = "{:.2f}".format(self.num_correct_words / self.total_words * 100)
        return f"Your score: {self.num_correct_chars} CPM (that is {self.wpm} WPM)\n" \
               f"Your accuracy percentage is:" \
               f" {accuracy_percentage} %"

    def print_mistakes(self):
        num_words = self.num_correct_words + self.num_incorrect_words
        mistakes = ''
        if self.num_incorrect_words == 0 and self.total_words != 0:
            return "Congratulations! You made zero mistakes!"

        for d in self.incorrect_words:
            mistakes += f'Instead of "{self.incorrect_words[d]}", you typed "{d}"\n'

        return f"You actually typed {self.num_correct_chars + self.num_incorrect_chars} CPM " \
               f"but you made {self.num_incorrect_words} mistake(s) out of {num_words}, " \
               f"which was not counted in the corrected score.\n\n" \
               f"Your mistake was: \n" \
               f"{mistakes}\n" \
               f"I advise you to take a 2 minute break now."


# ---------------------------- UI SETUP ------------------------------- #
if __name__ == "__main__":
    root = App()
    root.mainloop()