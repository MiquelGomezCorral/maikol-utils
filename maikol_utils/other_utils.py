import dataclasses
from argparse import Namespace

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


# =================================================
#                   DATACASS FUNCTIONS
# =================================================
def args_to_dataclass(args: Namespace, data_class: type):
    """From the args namespace, fillup a dataclass.

    It will change all the fields that have ben added to the args.
    If a field is not added in the args will be ignored.
    Fields in the args that are not in the Config this will be ignored.

    Args:
        args (Namespace): Parsed arguments. 
        data_class (type): Dataclass or any dataclass type from dataclasses.

    Returns:
        Configuration: Configuration with args values.
    """
    fields = {f.name for f in dataclasses.fields(data_class)}
    filtered = {k: v for k, v in vars(args).items() if k in fields and v is not None}
    return data_class(**filtered)