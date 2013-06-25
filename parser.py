# Description
#   Parses plaintext trivia question files into SQLite database
#
# Dependencies:
#   python >= 2.6.1
#   sqlite3 >= 3.6.12
#
# Configuration:
#   dbfile = <output_database>
#   questionfile = <input_text_file>
#
# Author:
#   Josh Vazquez
#
# Version:
#   0.2.0

# This parser expects a plaintext question file with the following format:
# /<category>/<answer1>/<answer2>/.../<answern>//<title>
#
# Example:
# /Art/Mona Lisa/La Gioconda//What is possibly the most famous painting in the world?
#
# Alternate acceptable answers follow the primary answer before the question title

import string, sqlite3

# Variables
dbfile = "questions00_v2.db"
questionfile = "spicytrivia00.txt"
questions = []
questioninfo = {}
conn = sqlite3.connect(dbfile)
conn.text_factory = str # prevent 8-bit string error

# Prepare database

c = conn.cursor()

# Create table structure
c.execute('''CREATE TABLE questions (category text, title text)''')
c.execute('''CREATE TABLE answers (id integer, answer text)''')

# Parse
with open(questionfile, 'r') as f:
  for line in f:
    splitTitle = string.split(line, "//", 1) # separates title from the rest
    title = splitTitle[1].rstrip('\r\n') # title is last element
    splitCategory = string.split(splitTitle[0], "/") # separates category from all answers
    category = splitCategory[1] # category is second element
    answers = splitCategory[2:] # to end of list
    c.execute("INSERT INTO questions VALUES (?, ?)", (category, title))
    lastid = c.lastrowid
    for a in answers:
      c.execute("INSERT INTO answers VALUES (?, ?)", (lastid, a))

conn.commit()
conn.close()

print "Parsing complete."