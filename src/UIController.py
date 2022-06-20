import tkinter as tk
from multiprocessing.pool import ThreadPool
from tkinter import ttk
import HostFinder as hF


# todo: think about refactoring this file
# todo: add style sheet
# todo: add some kind of auto-copy feature for the list after clicking on item?

# ---------------------------------------------------------------------------------------------------------
# methods
# ---------------------------------------------------------------------------------------------------------

def get_range_from_entry():
    try:
        result = parse_range(range_entry.get())
        run_search(int(result[0]), int(result[1]))
    except Exception as e:
        print(e.with_traceback(None))


# todo: parse whole ip address
def parse_range(string):
    result = string.split("-")
    return result


def update_listbox(content):
    for item in content:
        listbox.insert(0, item)


# todo: threading does not work, UI get blocked
def run_search(address_lower, address_upper):
    pool = ThreadPool(processes=1)
    ping_async_result = pool.apply_async(hF.find_hosts_by_pinging, (address_lower, address_upper))
    pool = ThreadPool(processes=2)
    tcp_async_result = pool.apply_async(hF.find_hosts_by_scanning_ports, (address_lower, address_upper, 22, 445))

    by_tcp = tcp_async_result.get()
    by_ping = ping_async_result.get()

    a = set(by_tcp)
    b = set(by_ping)
    c = a.union(b)

    update_listbox(c)


# ---------------------------------------------------------------------------------------------------------
# program
# ---------------------------------------------------------------------------------------------------------

# root window
root = tk.Tk()
root.geometry("600x400")
root.title('Simple IP Scanner')

# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.columnconfigure(2, weight=1)

# range label
range_label = ttk.Label(root, text="Enter range:")
range_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

# range entry
range_entry = ttk.Entry(root)
range_entry.grid(column=1, row=0, sticky="nsew", padx=5, pady=5)

# Scan button
scan_button = ttk.Button(root, text="Scan", command=get_range_from_entry)
scan_button.grid(column=2, row=0, sticky=tk.E, padx=5, pady=5)

# List with ip addresses
listbox = tk.Listbox(
    root,
    height=16,
    selectmode='browse',
)

listbox.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=5, pady=5)

root.mainloop()
