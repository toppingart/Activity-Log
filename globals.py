from pymongo import MongoClient
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import sys


def initialize(): 
    global root, client, db
    root = Tk()
    root.title("Activity Log")
    root.geometry("700x400")

   # root['bg'] = 'white'

    client = MongoClient('mongodb://localhost:27017') # connects to a specific port

    # open the database
    db = client["sheets"]

