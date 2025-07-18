"""Module with all the Time traking utils functions."""

import time
import json
from typing import Tuple, Optional, TextIO

from .print_utils import print_separator, print_warn

# =================================================
#                   HELPER FUNCTIONS
# =================================================
    
def parse_seconds_to_minutes(sec: float) -> str:
    """
    Parses a duration in seconds into a formatted string with hours, minutes, and seconds.

    Args:
        sec (float): Number of seconds.

    Returns:
        str: Formatted time string (e.g., '01 hrs, 05 mins, 30.1234 sec').
    """
    hours = int(sec // 3600)
    minutes = int((sec % 3600) // 60)
    seconds = int(sec % 60)
    decimals = int((sec % 1) * 10000)

    if hours > 0:
        return f"{hours:02} hrs, {minutes:02} mins, {seconds:02}.{decimals:04} sec"
    elif minutes > 0:
        return f"{minutes:02} mins, {seconds:02}.{decimals:04} sec"
    else:
        return f"{seconds:02}.{decimals:04} sec"


def print_time(sec: float, n_files: Optional[int] = None, space: bool = False, prefix: str = "", sufix: str = "", out_file: Optional[TextIO] = None) -> None:
    """Given a certain number of seconds, parse it to Formatted time string (e.g., '01 hrs, 05 mins, 30.1234 sec').
    If not enough seconds for hours, just '05 mins, 30.1234 sec'.
    If neither enogh seconds for minuts, just parse '30.1234 sec'.
    Optionally you can add a 'number of files' to get avg metrics as well as extra config for better printing. 
    Optionally you can pass a file to print everyting there.

    Args:
        sec (float): Number of seconds
        n_files (Optional[int], optional): Number of files to add an avg. Defaults to None.
        space (bool, optional): To add a space before the print. Defaults to False.
        prefix (str, optional): To add a prefix before the print. Defaults to "".
        sufix (str, optional): To add a sufix after the print. Defaults to "".
        out_file (Optional[TextIO], optional): To print the line somewere that's not the std bash (keed None for bash). Defaults to None.
    """
    if space:
        print("")
    
    if not prefix.endswith(" "):
        prefix = f"{prefix} "
    
    if n_files is not None:
        message = f"{prefix} - {n_files:4} files in: {parse_seconds_to_minutes(sec)}{sufix}.\n"
        message += f" -  Per document: {parse_seconds_to_minutes(sec / n_files)}"
    else:
        message = f"{prefix}Time: {parse_seconds_to_minutes(sec)}{sufix}."

    if out_file:
        print(message, file=out_file)
    else:
        print(message)
    
# =================================================
#                   TIME TRACKER
# =================================================
        
class TimeTracker:
    """
    Class for tracking the time of a process. It allows to track the time of different points in the process and save them in a json file.
    It also allows to track the time of different laps in the process.
    """
    def __init__(self, name: str, start_track_now: bool = False ):
        self.name = name
        self.hist: dict[str, Tuple[float, float]] = dict()
        self.started: bool = False
        self.last_time: float = -1.0
        
        self.lap_hist = dict()
        self.lap_runing: bool = False
        self.lap_number: int = 0
        
        if start_track_now:
            self.start(verbose=False)
            
        print_separator(f"⏳ TIME TRACKER '{name}' INITIALIZED{'. STARTING NOW' if start_track_now else ''}! ⏳")
    
    def start(self, verbose: bool = True, space: bool = True):
        """
        Starts traking the time
        """
        self.started = True
        self.track("START", verbose=verbose, space=space)
        
    
    def track(self, tag: str, verbose: bool = True, space: bool = False, mute_warning: bool = False) -> float:
        """
        Track the time of a certain point and add it a tag. Return time since las track
        """
        if not self.started and not mute_warning:
            print_warn("WARNING: Traking without startng, will call start.")
            self.start()
            
        t = time.time()
        diff = t - self.last_time if self.last_time > 0 else 0
        
        if self.lap_runing:
            if tag in self.lap_hist:
                tag = f"{tag}_{self.lap_number}"
            self.lap_hist[tag] = (t, diff)
        else:
            if tag in self.hist:
                tag = f"{tag}_"
            self.hist[tag] = (t, diff)
        
        if verbose: 
            print_tag = tag if not self.lap_runing else f"{tag} lap {self.lap_number}"
            print_time(diff, prefix=f"⏳ {print_tag}", sufix=" ⏳", space=space)
            
        self.last_time = t
        return diff
    
    # ============================================================================
    #                              LAPS MANAGEMENT
    # ============================================================================
    def start_lap(self, N: int = None, verbose: bool = False, mute_warning: bool = False) -> int:
        """Starts a new lap with its oun metrics and returns the number of the current started lap

        Args:
            N (int, optional): Total number of potential laps. Defaults to None.
            verbose (bool, optional): Print the number of the lap. Defaults to False.
            mute_warning (bool, optional): Show or not warnings. Defaults to False.

        Returns:
            int: Number of the current started lap.
        """
        self.lap_runing = True
        self.lap_number += 1
        if len(self.lap_hist) > 0 and not mute_warning:
            print_warn("WARNING: Starting lap without finishing previous. The records will be overritten.")
            
        t = time.time()    
        self.lap_hist["START_LAP"] = (t, 0)
        self.last_time = t
        
        if verbose:
            print(f"⏳ Starting lap num {self.lap_number}{f'/{N} ' if N is not None else ''}⏳!")
            
        return self.lap_number
        
    def finish_lap(self):
        """Finish lap and add the point trak to the list
        """
        self.lap_runing = False
        
        t = time.time()
        self.lap_hist["FINISH_LAP"] = (t, t-self.lap_hist["START_LAP"][0])
        
        # Update possible previous times
        for tag, (t, diff) in self.lap_hist.items():
            if tag in self.hist:
                _, prev_diff = self.hist[tag]
                self.hist[tag] = (t, prev_diff + diff)
            else:
                self.hist[tag] = (t, diff)
                
                
        self.lap_hist = dict()
        
    # ============================================================================
    #                              STIMATE TIME
    # ============================================================================
    def stimate_lap_time(self, N: int, mute_warning: bool = False):
        """Stimate the time to finish N laps after all the alread finished laps

        Args:
            N (int): Total number of laps (including those already done)
            mute_warning (bool, optional): Whether or not mute the waning about not running laps. Defaults to False.
        """
        if not self.lap_runing and not mute_warning:
            print_warn("WARNING: Stimating lap without starting it. Returning...")
            return
            
        t_f_end = time.time()
        eta = (N - self.lap_number) * (t_f_end - self.hist["START"][0]) / self.lap_number
        print_time(
            t_f_end - self.lap_hist["START_LAP"][0], 
            prefix="Total ", 
            sufix=f". ETA: {parse_seconds_to_minutes(eta)}"
        )
    
    # ============================================================================
    #                              METRICS MANAGEMENT
    # ============================================================================
        
    def get_metrics(self, n: int = None, initial_tag: str = "START") -> dict:
        """
        Return a dict with all the metrics with the form: tag: (time, diff) 
        Added Normalized if n of samples is passed with the form: tag: (time, diff, diff/n) 
        
        initial_tag change it in case it hasn't been set as 'START' for the first track
        """
        t = time.time()
        if len(self.hist) > 0: 
            if initial_tag not in self.hist:
                print_warn(f"WARNING: Passed initial tag '{initial_tag}' not found in history. Setting to first.")
                initial_tag = next(iter(self.hist)) # Getting the firts added tag
            self.hist["TOTAL"] = (t, t - self.hist[initial_tag][0])
            
        else:
            print_warn("WARNING: Getting metrics with 0 tracked points. This will return an empty dict.")
        
        if n is not None:
            res_hist =  {
                tag: (time, diff, diff/n) for tag, (time, diff) in self.hist.items()
            }
        else:
            res_hist = self.hist.copy()
        
        if "START_LAP" in res_hist:
            res_hist.pop("START_LAP")
        return res_hist
        
    def save_metric(self, save_path: str, n: int = None) -> dict:
        """Compute metrics, save them into a file and return them 

        Args:
            save_path (str): Save path for the metrics
            n (int, optional): 'Number of files' processed to get and avg. Defaults to None.

        Returns:
            dict: Computed metrics
        """
        metrics = self.get_metrics(n)
        
        with open(save_path, "w") as f:
            json.dump(metrics, f)
            
        return metrics
        
    def print_metrics(self, n: int = None, out_file: TextIO = None) -> dict:
        """Compute and print the metrics. Optionally into a file.

        Args:
            n (int, optional): 'Number of files' processed to get and avg. Defaults to None.
            out_file (TextIO, optional): File where printing should be done. Defaults to None.

        Returns:
            dict: Computed metrics
        """
        metrics = self.get_metrics(n)
        metrics.pop('START', None)
        print("")
        if n is not None:
            print(f"Processed {n} files in total\n", file=out_file)
        
        for tag, records in metrics.items():
            diff = records[1]
            
            print_time(diff, n_files=n, prefix=tag, out_file=out_file)
                    
        return metrics
        
