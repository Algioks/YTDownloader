import tkinter as tk
from tkinter import filedialog, messagebox
from v3BE import Downloader

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("YouTube Downloader")

        # url input
        self.url_label = tk.Label(master, text="Enter URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        # output folder selection
        self.output_label = tk.Label(master, text="Select output folder:")
        self.output_label.pack()
        self.output_entry = tk.Entry(master, width=50)
        self.output_entry.pack()
        self.folder_button = tk.Button(master, text="Select folder", command=self.select_folder)
        self.folder_button.pack()

        # download button
        self.download_button = tk.Button(master, text="Download", command=self.download)
        self.download_button.pack()

        # cancel button
        self.cancel_button = tk.Button(master, text="Cancel", command=self.cancel_download, state=tk.DISABLED)
        self.cancel_button.pack()

        # status console
        self.status_console = tk.Text(master, height=10, width=50)
        self.status_console.pack()
        self.update_status("Welcome to YouTube Downloader!", "info")

    def select_folder(self):
        """Select the output folder"""
        folder_path = filedialog.askdirectory()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, folder_path)

    def download(self):
        """Start the download process"""
        url = self.url_entry.get().strip()
        output_folder = self.output_entry.get().strip()

        if not url:
            self.update_status("Please enter a valid YouTube URL", "error")
            return

        if not output_folder:
            self.update_status("Please select an output folder", "error")
            return

        self.downloader = Downloader(url, output_folder)
        self.download_button.configure(state=tk.DISABLED)
        self.folder_button.configure(state=tk.DISABLED)
        self.cancel_button.configure(state=tk.NORMAL)
        self.update_status("Download started...", "info")
        self.downloader.start_download()

    def cancel_download(self):
        """Cancel the ongoing download"""
        self.update_status("Download cancelled.", "info")
        self.cancel_button.configure(state=tk.DISABLED)
        self.folder_button.configure(state=tk.NORMAL)
        self.download_button.configure(state=tk.NORMAL)
        self.downloader.cancel_download()

    def update_status(self, message, status_type):
        """Update the status console with the given message and status type"""
        if status_type == "info":
            tag = "INFO"
            color = "black"
        elif status_type == "error":
            tag = "ERROR"
            color = "red"
        else:
            tag = "STATUS"
            color = "green"
        self.status_console.configure(state=tk.NORMAL)
        self.status_console.insert(tk.END, f"[{tag}] {message}\n", color)
        self.status_console.configure(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
