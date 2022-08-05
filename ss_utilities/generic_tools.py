"""
A module of generic, reusable tools.

- Jamie Taylor <jamie.taylor@sheffield.ac.uk>
- First Authored: 2015-01-16

"""

from datetime import datetime
import os
import sys
from typing import Optional, List, Dict
import pytz
from calendar import monthrange
import numpy as np

class GenericException(Exception):
    """A generic exception for anticipated errors."""
    def __init__(self, msg, msg_id=None, filename=None, err=None):
        if msg_id is not None:
            self.msg = "%s: %s" % (msg_id, msg)
        else:
            self.msg = msg
        if err is not None:
            self.msg += "\n    %s" % repr(err)
        if filename:
            logger = GenericErrorLogger(filename)
            logger.write_to_log(self.msg)
    def __str__(self):
        return self.msg

class GenericErrorLogger:
    """Basic error logging to a file (optional)."""
    def __init__(self, filename):
        self.logfile = filename

    def write_to_log(self, msg):
        """
        Log the error message to the logfile along with a datestamp and the name of the script
        (in case of shared logfiles).

        Parameters
        ----------
        `msg` : string
            Message to be recorded in *self.logfile*.
        """
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        scriptname = os.path.basename(__file__)
        fid = open(self.logfile, "a")
        fid.write(timestamp + " " + scriptname + ": " + str(msg) + "\n")
        fid.close()
        return

def send_email(
        smtp_config: Dict,
        message: str,
        recipient: str,
        carbon_copy: Optional[str] = None,
        subject: Optional[str] = None,
        reply_to: Optional[str] = None,
        attachments: Optional[List[str]] = None,
        html: bool = False) -> None:
    """
    Send an email alert using smtplib.
    """
    import smtplib, ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = smtp_config["email"]
    msg["To"] = recipient
    if carbon_copy is not None:
        msg["Cc"] = carbon_copy
    if reply_to is not None:
        msg["Reply-To"] = reply_to
    body = MIMEText(message, "html") if html else MIMEText(message, "plain")
    msg.attach(body)
    if attachments is not None:
        for att in attachments:
            with open(att, "rb") as f:
                filename = os.path.split(att)[1]
                attachment = MIMEApplication(f.read(), "subtype")
                attachment["Content-Disposition"] = f'attachment; filename="{filename}";'
                msg.attach(attachment)
    # Create a secure SSL context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with smtplib.SMTP_SSL(smtp_config["server"], smtp_config["port"], context=context) as server:
        server.login(smtp_config["email"], smtp_config["password"])
        server.send_message(msg)
    return

def to_unixtime(datetime_, timezone_=None):
    """
    DEPRECATED! Use https://github.com/SheffieldSolar/sp2ts instead.
    Convert a python datetime object, *datetime_*, into unixtime int

    Parameters
    ----------
    `datetime_` : datetime.datetime
        Datetime to be converted
    `timezone_` : string
        The timezone of the input date from Olson timezone database. If *datetime_* is timezone
        aware then this can be ignored.
    Returns
    -------
    float
        Unixtime i.e. seconds since epoch
    Notes
    -----
    unixtime == seconds since epoch (Jan 01 1970 00:00:00 UTC)\n
    See Also
    --------
    :func:`UKPVLiveTestCase.test_to_unixtime`
    """
    raise Exception("The `to_unixtime()` method is no longer supported here, use "
                    "https://github.com/SheffieldSolar/sp2ts instead.")
    if not timezone_ and not datetime_.tzinfo:
        raise GenericException(msg_id="ukpv_live.to_unixtime", msg=("EITHER datetime_ must contain "
                                                                    "tzinfo OR timezone_must be "
                                                                    "passed."))
    if timezone_ and not datetime_.tzinfo:
        utc_datetime = pytz.timezone(timezone_).localize(datetime_).astimezone(pytz.utc)
    else:
        utc_datetime = datetime_.astimezone(pytz.utc)
    unixtime = int((utc_datetime - datetime(1970, 1, 1, 0, 0, 0, 0, pytz.utc)).total_seconds())
    return unixtime

def from_unixtime(unixtime_, timezone_="UTC"):
    """
    DEPRECATED! Use https://github.com/SheffieldSolar/sp2ts instead.
    Convert a unixtime int, *unixtime_*, into python datetime object

    Parameters
    ----------
    `unixtime_` : int
        Unixtime i.e. seconds since epoch
    `timezone_` : string
        The timezone of the output date from Olson timezone database. Defaults to utc.
    Returns
    -------
    datetime.datetime
        Python datetime object (timezone aware)
    Notes
    -----
    unixtime == seconds since epoch (Jan 01 1970 00:00:00 UTC)\n
    Unit test: UKPVLiveTestCase.test_to_unixtime
    """
    raise Exception("The `from_unixtime()` method is no longer supported here, use "
                    "https://github.com/SheffieldSolar/sp2ts instead.")
    return datetime.fromtimestamp(unixtime_, tz=pytz.timezone(timezone_))

def myround(number, base=5):
    """Round to the nearest *base*."""
    return int(base * round(float(number)/base))

def query_yes_no(question, default="yes"):
    """
    Ask a yes/no question via raw_input() and return the answer as boolean.

    Parameters
    ----------
    `question` : string
        The question presented to the user.
    `default` : string
        The presumed answer if the user just hits <Enter>. It must be "yes" (the default), "no" or
        None (meaning an answer is required of the user).
    Returns
    -------
    boolean
        Return value is True for "yes" or False for "no".
    Notes
    -----
    See http://stackoverflow.com/a/3041990
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        if (sys.version_info > (3, 0)):
            choice = input().lower()
        else:
            choice = raw_input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def print_progress(iteration, total, prefix="", suffix="", decimals=2, bar_length=100):
    """
    Call in a loop to create terminal progress bar.

    Parameters
    ----------
    `iteration` : int
        current iteration (required)
    `total` : int
        total iterations (required)
    `prefix` : string
        prefix string (optional)
    `suffix` : string
        suffix string (optional)
    `decimals` : int
        number of decimals in percent complete (optional)
    `bar_length` : int
        character length of bar (optional)
    Notes
    -----
    Taken from `Stack Overflow <http://stackoverflow.com/a/34325723>`_.
    """
    filled_length = int(round(bar_length * iteration / float(total)))
    percents = round(100.00 * (iteration / float(total)), decimals)
    progress_bar = "#" * filled_length + "-" * (bar_length - filled_length)
    sys.stdout.write("\r%s |%s| %s%s %s" % (prefix, progress_bar, percents, "%", suffix))
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write("\n")
        sys.stdout.flush()

def monthdelta(dt, delta):
    """Add or subtract *delta* months from the datetime *dt*."""
    y, m, d, h, mi, s = dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
    new_m = (m + delta) % 12
    new_y = y + (m + delta - 1) // 12
    if not new_m: new_m = 12
    new_d = min(d, monthrange(y, m)[1])
    return dt.replace(day=new_d, month=new_m, year=new_y)

def haversine_np(lat1, lon1, lat2, lon2, units="km"):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    All args must be of equal length!
    All input lat/lon are assumed to be decimal degrees!

    Parameters
    ----------
    `lat1` : np.array
        Latitudes of reference point(s) as either Numpy array of dtype float or single float.
    `lon1` : np.array
        Longitudes of reference point(s) as either Numpy array of dtype float or single float.
    `lat2` : np.array
        Latitudes of point(s) of interest as either Numpy array of dtype float or single float.
    `lon2` : np.array
        Longitudes of point(s) of interest as either Numpy array of dtype float or single float.
    `units` : str
        One of: 'km' (default), 'm', 'mi'.
    """
    avg_earth_radius_km = 6371.0088
    unit_conversion = {
        "km": 1,
        "m": 1000,
        "mi": 0.621371192,
    }
    avg_earth_radius = avg_earth_radius_km * unit_conversion[units]
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2.0 * np.arcsin(np.sqrt(a))
    hav_dist = avg_earth_radius * c
    return hav_dist

def ascii_bar_chart(data, title="ASCII Bar Chart", maxwidth=100, show_values=True, barchar="#"):
    title_pad_l = " " * ((maxwidth - len(title)) // 2)
    title_pad_r = " " * (maxwidth - len(title) - len(title_pad_l))
    output = "{0}\n{1}{2}{3}\n{0}\n".format("-" * maxwidth, title_pad_l, title, title_pad_r)
    max_label_width = max([len(r[0]) for r in data]) if show_values else 0
    max_val = max([r[1] for r in data])
    right_space = 10 + len("{}".format(max_val))
    bar_inc = max_val / float(maxwidth - max_label_width - right_space)
    for label, value in data:
        val_label = " {}".format(value) if show_values else ""
        bars = barchar * int(np.floor(float(value) / bar_inc))
        bars = "[{}]".format(bars) if value > 0. else ""
        left_pad = " " * (max_label_width - len(label) + 2)
        output += "{}{} | {}{}\n".format(left_pad, label, bars, val_label)
    output += "{}\n".format("-" * maxwidth)
    return output
