# SherlockSearch class
# this is just an amalgamation of all of the sherlock-project
class SherlockSearch:
    def __init__(self):
        self.sherlockInstance = None

    def search(self, query, progress_callback=None):
        print("searching using sherlock")
        # query custom sherlock and returns dict of:
        # { "name": "website name", "url": "url to user"}
        results = search(query, progress_callback)
        print(results)
        return results


"""Sherlock Notify Module

This module defines the objects for notifying the caller about the
results of queries.
"""
# from sherlock.result import QueryStatus
from colorama import Fore, Style
import webbrowser

# Global variable to count the number of results.
globvar = 0


class QueryNotify:
    """Query Notify Object.

    Base class that describes methods available to notify the results of
    a query.
    It is intended that other classes inherit from this base class and
    override the methods to implement specific functionality.
    """

    def __init__(self, result=None):
        """Create Query Notify Object.

        Contains information about a specific method of notifying the results
        of a query.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.

        Return Value:
        Nothing.
        """

        self.result = result

        # return

    def start(self, message=None):
        """Notify Start.

        Notify method for start of query.  This method will be called before
        any queries are performed.  This method will typically be
        overridden by higher level classes that will inherit from it.

        Keyword Arguments:
        self                   -- This object.
        message                -- Object that is used to give context to start
                                  of query.
                                  Default is None.

        Return Value:
        Nothing.
        """

        # return

    def update(self, result):
        """Notify Update.

        Notify method for query result.  This method will typically be
        overridden by higher level classes that will inherit from it.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.

        Return Value:
        Nothing.
        """

        self.result = result

        # return

    def finish(self, message=None):
        """Notify Finish.

        Notify method for finish of query.  This method will be called after
        all queries have been performed.  This method will typically be
        overridden by higher level classes that will inherit from it.

        Keyword Arguments:
        self                   -- This object.
        message                -- Object that is used to give context to start
                                  of query.
                                  Default is None.

        Return Value:
        Nothing.
        """

        # return

    def __str__(self):
        """Convert Object To String.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        Nicely formatted string to get information about this object.
        """
        return str(self.result)


class QueryNotifyPrint(QueryNotify):
    """Query Notify Print Object.

    Query notify class that prints results.
    """

    def __init__(self, result=None, verbose=False, print_all=False, browse=False):
        """Create Query Notify Print Object.

        Contains information about a specific method of notifying the results
        of a query.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.
        verbose                -- Boolean indicating whether to give verbose output.
        print_all              -- Boolean indicating whether to only print all sites, including not found.
        browse                 -- Boolean indicating whether to open found sites in a web browser.

        Return Value:
        Nothing.
        """

        super().__init__(result)
        self.verbose = verbose
        self.print_all = print_all
        self.browse = browse

        return

    def start(self, message):
        """Notify Start.

        Will print the title to the standard output.

        Keyword Arguments:
        self                   -- This object.
        message                -- String containing username that the series
                                  of queries are about.

        Return Value:
        Nothing.
        """

        title = "Checking username"

        print(Style.BRIGHT + Fore.GREEN + "[" +
              Fore.YELLOW + "*" +
              Fore.GREEN + f"] {title}" +
              Fore.WHITE + f" {message}" +
              Fore.GREEN + " on:")
        # An empty line between first line and the result(more clear output)
        print('\r')

        return

    def countResults(self):
        """This function counts the number of results. Every time the function is called,
        the number of results is increasing.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        The number of results by the time we call the function.
        """
        global globvar
        globvar += 1
        return globvar

    def update(self, result):
        """Notify Update.

        Will print the query result to the standard output.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.

        Return Value:
        Nothing.
        """
        self.result = result

        response_time_text = ""
        if self.result.query_time is not None and self.verbose is True:
            response_time_text = f" [{round(self.result.query_time * 1000)}ms]"

        # Output to the terminal is desired.
        if result.status == QueryStatus.CLAIMED:
            self.countResults()
            print(Style.BRIGHT + Fore.WHITE + "[" +
                  Fore.GREEN + "+" +
                  Fore.WHITE + "]" +
                  response_time_text +
                  Fore.GREEN +
                  f" {self.result.site_name}: " +
                  Style.RESET_ALL +
                  f"{self.result.site_url_user}")
            if self.browse:
                webbrowser.open(self.result.site_url_user, 2)

        elif result.status == QueryStatus.AVAILABLE:
            if self.print_all:
                print(Style.BRIGHT + Fore.WHITE + "[" +
                      Fore.RED + "-" +
                      Fore.WHITE + "]" +
                      response_time_text +
                      Fore.GREEN + f" {self.result.site_name}:" +
                      Fore.YELLOW + " Not Found!")

        elif result.status == QueryStatus.UNKNOWN:
            if self.print_all:
                print(Style.BRIGHT + Fore.WHITE + "[" +
                      Fore.RED + "-" +
                      Fore.WHITE + "]" +
                      Fore.GREEN + f" {self.result.site_name}:" +
                      Fore.RED + f" {self.result.context}" +
                      Fore.YELLOW + " ")

        elif result.status == QueryStatus.ILLEGAL:
            if self.print_all:
                msg = "Illegal Username Format For This Site!"
                print(Style.BRIGHT + Fore.WHITE + "[" +
                      Fore.RED + "-" +
                      Fore.WHITE + "]" +
                      Fore.GREEN + f" {self.result.site_name}:" +
                      Fore.YELLOW + f" {msg}")

        elif result.status == QueryStatus.WAF:
            if self.print_all:
                print(Style.BRIGHT + Fore.WHITE + "[" +
                      Fore.RED + "-" +
                      Fore.WHITE + "]" +
                      Fore.GREEN + f" {self.result.site_name}:" +
                      Fore.RED + " Blocked by bot detection" +
                      Fore.YELLOW + " (proxy may help)")

        else:
            # It should be impossible to ever get here...
            raise ValueError(
                f"Unknown Query Status '{result.status}' for site '{self.result.site_name}'"
            )

        return

    def finish(self, message="The processing has been finished."):
        """Notify Start.
        Will print the last line to the standard output.
        Keyword Arguments:
        self                   -- This object.
        message                -- The 2 last phrases.
        Return Value:
        Nothing.
        """
        NumberOfResults = self.countResults() - 1

        print(Style.BRIGHT + Fore.GREEN + "[" +
              Fore.YELLOW + "*" +
              Fore.GREEN + "] Search completed with" +
              Fore.WHITE + f" {NumberOfResults} " +
              Fore.GREEN + "results" + Style.RESET_ALL
              )

    def __str__(self):
        """Convert Object To String.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        Nicely formatted string to get information about this object.
        """
        return str(self.result)


"""Sherlock Result Module

This module defines various objects for recording the results of queries.
"""
from enum import Enum


class QueryStatus(Enum):
    """Query Status Enumeration.

    Describes status of query about a given username.
    """
    CLAIMED = "Claimed"  # Username Detected
    AVAILABLE = "Available"  # Username Not Detected
    UNKNOWN = "Unknown"  # Error Occurred While Trying To Detect Username
    ILLEGAL = "Illegal"  # Username Not Allowable For This Site
    WAF = "WAF"  # Request blocked by WAF (i.e. Cloudflare)

    def __str__(self):
        """Convert Object To String.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        Nicely formatted string to get information about this object.
        """
        return self.value


class QueryResult():
    """Query Result Object.

    Describes result of query about a given username.
    """

    def __init__(self, username, site_name, site_url_user, status,
                 query_time=None, context=None):
        """Create Query Result Object.

        Contains information about a specific method of detecting usernames on
        a given type of web sites.

        Keyword Arguments:
        self                   -- This object.
        username               -- String indicating username that query result
                                  was about.
        site_name              -- String which identifies site.
        site_url_user          -- String containing URL for username on site.
                                  NOTE:  The site may or may not exist:  this
                                         just indicates what the name would
                                         be, if it existed.
        status                 -- Enumeration of type QueryStatus() indicating
                                  the status of the query.
        query_time             -- Time (in seconds) required to perform query.
                                  Default of None.
        context                -- String indicating any additional context
                                  about the query.  For example, if there was
                                  an error, this might indicate the type of
                                  error that occurred.
                                  Default of None.

        Return Value:
        Nothing.
        """

        self.username = username
        self.site_name = site_name
        self.site_url_user = site_url_user
        self.status = status
        self.query_time = query_time
        self.context = context

        return

    def __str__(self):
        """Convert Object To String.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        Nicely formatted string to get information about this object.
        """
        status = str(self.status)
        if self.context is not None:
            # There is extra context information available about the results.
            # Append it to the normal response text.
            status += f" ({self.context})"

        return status


"""Sherlock Sites Information Module

This module supports storing information about websites.
This is the raw data that will be used to search for usernames.
"""
import json
import requests
import secrets


class SiteInformation:
    def __init__(self, name, url_home, url_username_format, username_claimed,
                 information, is_nsfw, username_unclaimed=secrets.token_urlsafe(10)):
        """Create Site Information Object.

        Contains information about a specific website.

        Keyword Arguments:
        self                   -- This object.
        name                   -- String which identifies site.
        url_home               -- String containing URL for home of site.
        url_username_format    -- String containing URL for Username format
                                  on site.
                                  NOTE:  The string should contain the
                                         token "{}" where the username should
                                         be substituted.  For example, a string
                                         of "https://somesite.com/users/{}"
                                         indicates that the individual
                                         usernames would show up under the
                                         "https://somesite.com/users/" area of
                                         the website.
        username_claimed       -- String containing username which is known
                                  to be claimed on website.
        username_unclaimed     -- String containing username which is known
                                  to be unclaimed on website.
        information            -- Dictionary containing all known information
                                  about website.
                                  NOTE:  Custom information about how to
                                         actually detect the existence of the
                                         username will be included in this
                                         dictionary.  This information will
                                         be needed by the detection method,
                                         but it is only recorded in this
                                         object for future use.
        is_nsfw                -- Boolean indicating if site is Not Safe For Work.

        Return Value:
        Nothing.
        """

        self.name = name
        self.url_home = url_home
        self.url_username_format = url_username_format

        self.username_claimed = username_claimed
        self.username_unclaimed = secrets.token_urlsafe(32)
        self.information = information
        self.is_nsfw = is_nsfw

        return

    def __str__(self):
        """Convert Object To String.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        Nicely formatted string to get information about this object.
        """

        return f"{self.name} ({self.url_home})"


class SitesInformation:
    def __init__(self, data_file_path=None):
        """Create Sites Information Object.

        Contains information about all supported websites.

        Keyword Arguments:
        self                   -- This object.
        data_file_path         -- String which indicates path to data file.
                                  The file name must end in ".json".

                                  There are 3 possible formats:
                                   * Absolute File Format
                                     For example, "c:/stuff/data.json".
                                   * Relative File Format
                                     The current working directory is used
                                     as the context.
                                     For example, "data.json".
                                   * URL Format
                                     For example,
                                     "https://example.com/data.json", or
                                     "http://example.com/data.json".

                                  An exception will be thrown if the path
                                  to the data file is not in the expected
                                  format, or if there was any problem loading
                                  the file.

                                  If this option is not specified, then a
                                  default site list will be used.

        Return Value:
        Nothing.
        """

        if not data_file_path:
            # The default data file is the live data.json which is in the GitHub repo. The reason why we are using
            # this instead of the local one is so that the user has the most up-to-date data. This prevents
            # users from creating issue about false positives which has already been fixed or having outdated data
            data_file_path = "https://raw.githubusercontent.com/sherlock-project/sherlock/master/sherlock/resources/data.json"

        # Ensure that specified data file has correct extension.
        if not data_file_path.lower().endswith(".json"):
            raise FileNotFoundError(f"Incorrect JSON file extension for data file '{data_file_path}'.")

        # if "http://"  == data_file_path[:7].lower() or "https://" == data_file_path[:8].lower():
        if data_file_path.lower().startswith("http"):
            # Reference is to a URL.
            try:
                response = requests.get(url=data_file_path)
            except Exception as error:
                raise FileNotFoundError(
                    f"Problem while attempting to access data file URL '{data_file_path}':  {error}"
                )

            if response.status_code != 200:
                raise FileNotFoundError(f"Bad response while accessing "
                                        f"data file URL '{data_file_path}'."
                                        )
            try:
                site_data = response.json()
            except Exception as error:
                raise ValueError(
                    f"Problem parsing json contents at '{data_file_path}':  {error}."
                )

        else:
            # Reference is to a file.
            try:
                with open(data_file_path, "r", encoding="utf-8") as file:
                    try:
                        site_data = json.load(file)
                    except Exception as error:
                        raise ValueError(
                            f"Problem parsing json contents at '{data_file_path}':  {error}."
                        )

            except FileNotFoundError:
                raise FileNotFoundError(f"Problem while attempting to access "
                                        f"data file '{data_file_path}'."
                                        )

        site_data.pop('$schema', None)

        self.sites = {}

        # Add all site information from the json file to internal site list.
        for site_name in site_data:
            try:

                self.sites[site_name] = \
                    SiteInformation(site_name,
                                    site_data[site_name]["urlMain"],
                                    site_data[site_name]["url"],
                                    site_data[site_name]["username_claimed"],
                                    site_data[site_name],
                                    site_data[site_name].get("isNSFW", False)

                                    )
            except KeyError as error:
                raise ValueError(
                    f"Problem parsing json contents at '{data_file_path}':  Missing attribute {error}."
                )
            except TypeError:
                print(
                    f"Encountered TypeError parsing json contents for target '{site_name}' at {data_file_path}\nSkipping target.\n")

        return

    def remove_nsfw_sites(self, do_not_remove: list = []):
        """
        Remove NSFW sites from the sites, if isNSFW flag is true for site

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        None
        """
        sites = {}
        do_not_remove = [site.casefold() for site in do_not_remove]
        for site in self.sites:
            if self.sites[site].is_nsfw and site.casefold() not in do_not_remove:
                continue
            sites[site] = self.sites[site]
        self.sites = sites

    def site_name_list(self):
        """Get Site Name List.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        List of strings containing names of sites.
        """

        return sorted([site.name for site in self], key=str.lower)

    def __iter__(self):
        """Iterator For Object.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        Iterator for sites object.
        """

        for site_name in self.sites:
            yield self.sites[site_name]

    def __len__(self):
        """Length For Object.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        Length of sites object.
        """
        return len(self.sites)


"""
Sherlock: Find Usernames Across Social Networks Module

This module contains the main logic to search for usernames at social
networks.
"""

import csv
import signal
import pandas as pd
import os
import re
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from time import monotonic

import requests

# Removing __version__ here will trigger update message for users
# Do not remove until ready to trigger that message
# When removed, also remove all the noqa: E402 comments for linting


from requests_futures.sessions import FuturesSession  # noqa: E402
from torrequest import TorRequest  # noqa: E402
# from .result import QueryStatus                 # noqa: E402
# from .result import QueryResult                 # noqa: E402
# from .notify import QueryNotify                 # noqa: E402
# from .notify import QueryNotifyPrint            # noqa: E402
# from .sites import SitesInformation             # noqa: E402
from colorama import init  # noqa: E402
from argparse import ArgumentTypeError  # noqa: E402


class SherlockFuturesSession(FuturesSession):
    def request(self, method, url, hooks=None, *args, **kwargs):
        """Request URL.

        This extends the FuturesSession request method to calculate a response
        time metric to each request.

        It is taken (almost) directly from the following Stack Overflow answer:
        https://github.com/ross/requests-futures#working-in-the-background

        Keyword Arguments:
        self                   -- This object.
        method                 -- String containing method desired for request.
        url                    -- String containing URL for request.
        hooks                  -- Dictionary containing hooks to execute after
                                  request finishes.
        args                   -- Arguments.
        kwargs                 -- Keyword arguments.

        Return Value:
        Request object.
        """
        # Record the start time for the request.
        if hooks is None:
            hooks = {}
        start = monotonic()

        def response_time(resp, *args, **kwargs):
            """Response Time Hook.

            Keyword Arguments:
            resp                   -- Response object.
            args                   -- Arguments.
            kwargs                 -- Keyword arguments.

            Return Value:
            Nothing.
            """
            resp.elapsed = monotonic() - start

            return

        # Install hook to execute when response completes.
        # Make sure that the time measurement hook is first, so we will not
        # track any later hook's execution time.
        try:
            if isinstance(hooks["response"], list):
                hooks["response"].insert(0, response_time)
            elif isinstance(hooks["response"], tuple):
                # Convert tuple to list and insert time measurement hook first.
                hooks["response"] = list(hooks["response"])
                hooks["response"].insert(0, response_time)
            else:
                # Must have previously contained a single hook function,
                # so convert to list.
                hooks["response"] = [response_time, hooks["response"]]
        except KeyError:
            # No response hook was already defined, so install it ourselves.
            hooks["response"] = [response_time]

        return super(SherlockFuturesSession, self).request(
            method, url, hooks=hooks, *args, **kwargs
        )


def get_response(request_future, error_type, social_network):
    # Default for Response object if some failure occurs.
    response = None

    error_context = "General Unknown Error"
    exception_text = None
    try:
        response = request_future.result()
        if response.status_code:
            # Status code exists in response object
            error_context = None
    except requests.exceptions.HTTPError as errh:
        error_context = "HTTP Error"
        exception_text = str(errh)
    except requests.exceptions.ProxyError as errp:
        error_context = "Proxy Error"
        exception_text = str(errp)
    except requests.exceptions.ConnectionError as errc:
        error_context = "Error Connecting"
        exception_text = str(errc)
    except requests.exceptions.Timeout as errt:
        error_context = "Timeout Error"
        exception_text = str(errt)
    except requests.exceptions.RequestException as err:
        error_context = "Unknown Error"
        exception_text = str(err)

    return response, error_context, exception_text


def interpolate_string(input_object, username):
    if isinstance(input_object, str):
        return input_object.replace("{}", username)
    elif isinstance(input_object, dict):
        return {k: interpolate_string(v, username) for k, v in input_object.items()}
    elif isinstance(input_object, list):
        return [interpolate_string(i, username) for i in input_object]
    return input_object


def check_for_parameter(username):
    """checks if {?} exists in the username
    if exist it means that sherlock is looking for more multiple username"""
    return "{?}" in username


checksymbols = ["_", "-", "."]


def multiple_usernames(username):
    """replace the parameter with with symbols and return a list of usernames"""
    allUsernames = []
    for i in checksymbols:
        allUsernames.append(username.replace("{?}", i))
    return allUsernames


def sherlock(
        username,
        site_data,
        query_notify: QueryNotify,
        tor: bool = False,
        unique_tor: bool = False,
        proxy=None,
        timeout=60,
        progress_callback=None,
):
    """Run Sherlock Analysis.

    Checks for existence of username on various social media sites.

    Keyword Arguments:
    username               -- String indicating username that report
                              should be created against.
    site_data              -- Dictionary containing all of the site data.
    query_notify           -- Object with base type of QueryNotify().
                              This will be used to notify the caller about
                              query results.
    tor                    -- Boolean indicating whether to use a tor circuit for the requests.
    unique_tor             -- Boolean indicating whether to use a new tor circuit for each request.
    proxy                  -- String indicating the proxy URL
    timeout                -- Time in seconds to wait before timing out request.
                              Default is 60 seconds.

    Return Value:
    Dictionary containing results from report. Key of dictionary is the name
    of the social network site, and the value is another dictionary with
    the following keys:
        url_main:      URL of main site.
        url_user:      URL of user on site (if account exists).
        status:        QueryResult() object indicating results of test for
                       account existence.
        http_status:   HTTP status code of query which checked for existence on
                       site.
        response_text: Text that came back from request.  May be None if
                       there was an HTTP error when checking for existence.
    """

    # Notify caller that we are starting the query.
    query_notify.start(username)
    # Create session based on request methodology
    if tor or unique_tor:
        # Requests using Tor obfuscation
        try:
            underlying_request = TorRequest()
        except OSError:
            print("Tor not found in system path. Unable to continue.\n")
            sys.exit(query_notify.finish())

        underlying_session = underlying_request.session
    else:
        # Normal requests
        underlying_session = requests.session()
        underlying_request = requests.Request()

    # Limit number of workers to 20.
    # This is probably vastly overkill.
    if len(site_data) >= 20:
        max_workers = 20
    else:
        max_workers = len(site_data)

    # Create multi-threaded session for all requests.
    session = SherlockFuturesSession(
        max_workers=max_workers, session=underlying_session
    )

    # Results from analysis of all sites
    results_total = {}

    # First create futures for all requests. This allows for the requests to run in parallel
    for social_network, net_info in site_data.items():
        # Results from analysis of this specific site
        results_site = {"url_main": net_info.get("urlMain")}

        # Record URL of main site

        # A user agent is needed because some sites don't return the correct
        # information since they think that we are bots (Which we actually are...)
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
        }

        if "headers" in net_info:
            # Override/append any extra headers required by a given site.
            headers.update(net_info["headers"])

        # URL of user on site (if it exists)
        url = interpolate_string(net_info["url"], username.replace(' ', '%20'))

        # Don't make request if username is invalid for the site
        regex_check = net_info.get("regexCheck")
        if regex_check and re.search(regex_check, username) is None:
            # No need to do the check at the site: this username is not allowed.
            results_site["status"] = QueryResult(
                username, social_network, url, QueryStatus.ILLEGAL
            )
            results_site["url_user"] = ""
            results_site["http_status"] = ""
            results_site["response_text"] = ""
            query_notify.update(results_site["status"])
            if progress_callback:
                progress_callback(results_site["status"])
        else:
            # URL of user on site (if it exists)
            results_site["url_user"] = url
            url_probe = net_info.get("urlProbe")
            request_method = net_info.get("request_method")
            request_payload = net_info.get("request_payload")
            request = None

            if request_method is not None:
                if request_method == "GET":
                    request = session.get
                elif request_method == "HEAD":
                    request = session.head
                elif request_method == "POST":
                    request = session.post
                elif request_method == "PUT":
                    request = session.put
                else:
                    raise RuntimeError(f"Unsupported request_method for {url}")

            if request_payload is not None:
                request_payload = interpolate_string(request_payload, username)

            if url_probe is None:
                # Probe URL is normal one seen by people out on the web.
                url_probe = url
            else:
                # There is a special URL for probing existence separate
                # from where the user profile normally can be found.
                url_probe = interpolate_string(url_probe, username)

            if request is None:
                if net_info["errorType"] == "status_code":
                    # In most cases when we are detecting by status code,
                    # it is not necessary to get the entire body:  we can
                    # detect fine with just the HEAD response.
                    request = session.head
                else:
                    # Either this detect method needs the content associated
                    # with the GET response, or this specific website will
                    # not respond properly unless we request the whole page.
                    request = session.get

            if net_info["errorType"] == "response_url":
                # Site forwards request to a different URL if username not
                # found.  Disallow the redirect so we can capture the
                # http status from the original URL request.
                allow_redirects = False
            else:
                # Allow whatever redirect that the site wants to do.
                # The final result of the request will be what is available.
                allow_redirects = True

            # This future starts running the request in a new thread, doesn't block the main thread
            if proxy is not None:
                proxies = {"http": proxy, "https": proxy}
                future = request(
                    url=url_probe,
                    headers=headers,
                    proxies=proxies,
                    allow_redirects=allow_redirects,
                    timeout=timeout,
                    json=request_payload,
                )
            else:
                future = request(
                    url=url_probe,
                    headers=headers,
                    allow_redirects=allow_redirects,
                    timeout=timeout,
                    json=request_payload,
                )

            # Store future in data for access later
            net_info["request_future"] = future

            # Reset identify for tor (if needed)
            if unique_tor:
                underlying_request.reset_identity()

        # Add this site's results into final dictionary with all the other results.
        results_total[social_network] = results_site

    # Open the file containing account links
    # Core logic: If tor requests, make them here. If multi-threaded requests, wait for responses
    for social_network, net_info in site_data.items():
        # Retrieve results again
        results_site = results_total.get(social_network)

        # Retrieve other site information again
        url = results_site.get("url_user")
        status = results_site.get("status")
        if status is not None:
            # We have already determined the user doesn't exist here
            continue

        # Get the expected error type
        error_type = net_info["errorType"]

        # Retrieve future and ensure it has finished
        future = net_info["request_future"]
        r, error_text, exception_text = get_response(
            request_future=future, error_type=error_type, social_network=social_network
        )

        # Get response time for response of our request.
        try:
            response_time = r.elapsed
        except AttributeError:
            response_time = None

        # Attempt to get request information
        try:
            http_status = r.status_code
        except Exception:
            http_status = "?"
        try:
            response_text = r.text.encode(r.encoding or "UTF-8")
        except Exception:
            response_text = ""

        query_status = QueryStatus.UNKNOWN
        error_context = None

        # As WAFs advance and evolve, they will occasionally block Sherlock and
        # lead to false positives and negatives. Fingerprints should be added
        # here to filter results that fail to bypass WAFs. Fingerprints should
        # be highly targetted. Comment at the end of each fingerprint to
        # indicate target and date fingerprinted.
        WAFHitMsgs = [
            '.loading-spinner{visibility:hidden}body.no-js .challenge-running{display:none}body.dark{background-color:#222;color:#d9d9d9}body.dark a{color:#fff}body.dark a:hover{color:#ee730a;text-decoration:underline}body.dark .lds-ring div{border-color:#999 transparent transparent}body.dark .font-red{color:#b20f03}body.dark',
            # 2024-05-13 Cloudflare
            '{return l.onPageView}}),Object.defineProperty(r,"perimeterxIdentifiers",{enumerable:'
            # 2024-04-09 PerimeterX / Human Security
        ]

        if error_text is not None:
            error_context = error_text

        elif any(hitMsg in r.text for hitMsg in WAFHitMsgs):
            query_status = QueryStatus.WAF

        elif error_type == "message":
            # error_flag True denotes no error found in the HTML
            # error_flag False denotes error found in the HTML
            error_flag = True
            errors = net_info.get("errorMsg")
            # errors will hold the error message
            # it can be string or list
            # by isinstance method we can detect that
            # and handle the case for strings as normal procedure
            # and if its list we can iterate the errors
            if isinstance(errors, str):
                # Checks if the error message is in the HTML
                # if error is present we will set flag to False
                if errors in r.text:
                    error_flag = False
            else:
                # If it's list, it will iterate all the error message
                for error in errors:
                    if error in r.text:
                        error_flag = False
                        break
            if error_flag:
                query_status = QueryStatus.CLAIMED
            else:
                query_status = QueryStatus.AVAILABLE
        elif error_type == "status_code":
            error_codes = net_info.get("errorCode")
            query_status = QueryStatus.CLAIMED

            # Type consistency, allowing for both singlets and lists in manifest
            if isinstance(error_codes, int):
                error_codes = [error_codes]

            if error_codes is not None and r.status_code in error_codes:
                query_status = QueryStatus.AVAILABLE
            elif r.status_code >= 300 or r.status_code < 200:
                query_status = QueryStatus.AVAILABLE
        elif error_type == "response_url":
            # For this detection method, we have turned off the redirect.
            # So, there is no need to check the response URL: it will always
            # match the request.  Instead, we will ensure that the response
            # code indicates that the request was successful (i.e. no 404, or
            # forward to some odd redirect).
            if 200 <= r.status_code < 300:
                query_status = QueryStatus.CLAIMED
            else:
                query_status = QueryStatus.AVAILABLE
        else:
            # It should be impossible to ever get here...
            raise ValueError(
                f"Unknown Error Type '{error_type}' for " f"site '{social_network}'"
            )

        # Notify caller about results of query.
        result = QueryResult(
            username=username,
            site_name=social_network,
            site_url_user=url,
            status=query_status,
            query_time=response_time,
            context=error_context,
        )
        query_notify.update(result)
        if progress_callback:
            progress_callback(result)
        # Save status of request
        results_site["status"] = result

        # Save results from request
        results_site["http_status"] = http_status
        results_site["response_text"] = response_text

        # Add this site's results into final dictionary with all of the other results.
        results_total[social_network] = results_site

    return results_total


def timeout_check(value):
    float_value = float(value)

    if float_value <= 0:
        raise ArgumentTypeError(
            f"Invalid timeout value: {value}. Timeout must be a positive number."
        )

    return float_value


def handler(signal_received, frame):
    sys.exit(0)


def main(username):
    print("calling sherlock_util main")
    sites = SitesInformation(
        os.path.join(os.path.dirname(__file__), "resources/data.json")
    )

    site_data_all = {site.name: site.information for site in sites}
    query_notify = QueryNotifyPrint()
    print("STARTING")
    results = sherlock(
        username=username,
        site_data=site_data_all,
        query_notify=query_notify
    )

    found_sites = []
    for site in results:
        if (str(results[site]["status"]) == "Claimed"):
            finding = {
                "name": site,
                "url": results[site]["url_user"]
            }
            found_sites.append(finding)

    return found_sites


def search(username, progress_callback):
    print("calling sherlock_util main")
    sites = SitesInformation(
        os.path.join(os.path.dirname(__file__), "resources/data.json")
    )

    # sites = """{'1337x': {'errorMsg': ['<title>Error something went wrong.</title>', '<head><title>404 Not Found</title></head>'], 'errorType': 'message', 'regexCheck': '^[A-Za-z0-9]{4,12}$', 'url': 'https://www.1337x.to/user/{}/', 'urlMain': 'https://www.1337x.to/', 'username_claimed': 'FitGirl'}, '2Dimensions': {'errorType': 'status_code', 'url': 'https://2Dimensions.com/a/{}', 'urlMain': 'https://2Dimensions.com/', 'username_claimed': 'blue'}, '3dnews': {'errorMsg': 'Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'errorType': 'message', 'url': 'http://forum.3dnews.ru/member.php?username={}', 'urlMain': 'http://forum.3dnews.ru/', 'username_claimed': 'red'}, '7Cups': {'errorType': 'status_code', 'url': 'https://www.7cups.com/@{}', 'urlMain': 'https://www.7cups.com/', 'username_claimed': 'blue'}, '8tracks': {'errorMsg': 'This page has vanished', 'errorType': 'message', 'url': 'https://8tracks.com/{}', 'urlMain': 'https://8tracks.com/', 'username_claimed': 'blue'}, '9GAG': {'errorType': 'status_code', 'url': 'https://www.9gag.com/u/{}', 'urlMain': 'https://www.9gag.com/', 'username_claimed': 'blue'}, 'APClips': {'errorMsg': 'Amateur Porn Content Creators', 'errorType': 'message', 'isNSFW': True, 'url': 'https://apclips.com/{}', 'urlMain': 'https://apclips.com/', 'username_claimed': 'onlybbyraq'}, 'About.me': {'errorType': 'status_code', 'url': 'https://about.me/{}', 'urlMain': 'https://about.me/', 'username_claimed': 'blue'}, 'Academia.edu': {'errorType': 'status_code', 'regexCheck': '^[^.]*$', 'url': 'https://independent.academia.edu/{}', 'urlMain': 'https://www.academia.edu/', 'username_claimed': 'blue'}, 'AdmireMe.Vip': {'errorMsg': 'Page Not Found', 'errorType': 'message', 'isNSFW': True, 'url': 'https://admireme.vip/{}', 'urlMain': 'https://admireme.vip/', 'username_claimed': 'DemiDevil'}, 'Air Pilot Life': {'errorMsg': 'Oops! That page doesn’t exist or is private', 'errorType': 'message', 'url': 'https://airlinepilot.life/u/{}', 'urlMain': 'https://airlinepilot.life/', 'username_claimed': 'chris'}, 'Airbit': {'errorType': 'status_code', 'url': 'https://airbit.com/{}', 'urlMain': 'https://airbit.com/', 'username_claimed': 'airbit'}, 'Airliners': {'errorType': 'status_code', 'url': 'https://www.airliners.net/user/{}/profile/photos', 'urlMain': 'https://www.airliners.net/', 'username_claimed': 'yushinlin'}, 'Alik.cz': {'errorType': 'status_code', 'url': 'https://www.alik.cz/u/{}', 'urlMain': 'https://www.alik.cz/', 'username_claimed': 'julian'}, 'All Things Worn': {'errorMsg': 'Sell Used Panties', 'errorType': 'message', 'isNSFW': True, 'url': 'https://www.allthingsworn.com/profile/{}', 'urlMain': 'https://www.allthingsworn.com', 'username_claimed': 'pink'}, 'AllMyLinks': {'errorMsg': 'Not Found', 'errorType': 'message', 'regexCheck': '^[a-z0-9][a-z0-9-]{2,32}$', 'url': 'https://allmylinks.com/{}', 'urlMain': 'https://allmylinks.com/', 'username_claimed': 'blue'}, 'Amino': {'errorType': 'status_code', 'url': 'https://aminoapps.com/u/{}', 'urlMain': 'https://aminoapps.com', 'username_claimed': 'blue'}, 'AniWorld': {'errorMsg': 'Dieses Profil ist nicht verfügbar', 'errorType': 'message', 'url': 'https://aniworld.to/user/profil/{}', 'urlMain': 'https://aniworld.to/', 'username_claimed': 'blue'}, 'Anilist': {'errorType': 'status_code', 'regexCheck': '^[A-Za-z0-9]{2,20}$', 'request_method': 'POST', 'request_payload': {'query': 'query($name:String){User(name:$name){id}}', 'variables': {'name': '{}'}}, 'url': 'https://anilist.co/user/{}/', 'urlMain': 'https://anilist.co/', 'urlProbe': 'https://graphql.anilist.co/', 'username_claimed': 'Josh'}, 'Apple Developer': {'errorType': 'status_code', 'url': 'https://developer.apple.com/forums/profile/{}', 'urlMain': 'https://developer.apple.com', 'username_claimed': 'lio24d'}, 'Apple Discussions': {'errorMsg': 'The page you tried was not found. You may have used an outdated link or may have typed the address (URL) incorrectly.', 'errorType': 'message', 'url': 'https://discussions.apple.com/profile/{}', 'urlMain': 'https://discussions.apple.com', 'username_claimed': 'jason'}, 'Archive of Our Own': {'errorType': 'status_code', 'regexCheck': '^[^.]*?$', 'url': 'https://archiveofourown.org/users/{}', 'urlMain': 'https://archiveofourown.org/', 'username_claimed': 'test'}, 'Archive.org': {'__comment__': "'The resource could not be found' relates to archive downtime", 'errorMsg': ['could not fetch an account with user item identifier', 'The resource could not be found'], 'errorType': 'message', 'url': 'https://archive.org/details/@{}', 'urlMain': 'https://archive.org', 'urlProbe': 'https://archive.org/details/@{}?noscript=true', 'username_claimed': 'blue'}, 'ArtStation': {'errorType': 'status_code', 'url': 'https://www.artstation.com/{}', 'urlMain': 'https://www.artstation.com/', 'username_claimed': 'Blue'}, 'Asciinema': {'errorType': 'status_code', 'url': 'https://asciinema.org/~{}', 'urlMain': 'https://asciinema.org', 'username_claimed': 'red'}, 'Ask Fedora': {'errorType': 'status_code', 'url': 'https://ask.fedoraproject.org/u/{}', 'urlMain': 'https://ask.fedoraproject.org/', 'username_claimed': 'red'}, 'AskFM': {'errorMsg': 'Well, apparently not anymore.', 'errorType': 'message', 'regexCheck': '^[a-zA-Z0-9_]{3,40}$', 'url': 'https://ask.fm/{}', 'urlMain': 'https://ask.fm/', 'username_claimed': 'blue'}, 'Audiojungle': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9_]+$', 'url': 'https://audiojungle.net/user/{}', 'urlMain': 'https://audiojungle.net/', 'username_claimed': 'blue'}, 'Autofrage': {'errorType': 'status_code', 'url': 'https://www.autofrage.net/nutzer/{}', 'urlMain': 'https://www.autofrage.net/', 'username_claimed': 'autofrage'}, 'Avizo': {'errorType': 'response_url', 'errorUrl': 'https://www.avizo.cz/', 'url': 'https://www.avizo.cz/{}/', 'urlMain': 'https://www.avizo.cz/', 'username_claimed': 'blue'}, 'BLIP.fm': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9_]{1,30}$', 'url': 'https://blip.fm/{}', 'urlMain': 'https://blip.fm/', 'username_claimed': 'blue'}, 'BOOTH': {'errorType': 'response_url', 'errorUrl': 'https://booth.pm/', 'regexCheck': '^[a-zA-Z0-9@_-]$', 'url': 'https://{}.booth.pm/', 'urlMain': 'https://booth.pm/', 'username_claimed': 'blue'}, 'Bandcamp': {'errorType': 'status_code', 'url': 'https://www.bandcamp.com/{}', 'urlMain': 'https://www.bandcamp.com/', 'username_claimed': 'blue'}, 'Bazar.cz': {'errorType': 'response_url', 'errorUrl': 'https://www.bazar.cz/error404.aspx', 'url': 'https://www.bazar.cz/{}/', 'urlMain': 'https://www.bazar.cz/', 'username_claimed': 'pianina'}, 'Behance': {'errorType': 'status_code', 'url': 'https://www.behance.net/{}', 'urlMain': 'https://www.behance.net/', 'username_claimed': 'blue'}, 'Bezuzyteczna': {'errorType': 'status_code', 'url': 'https://bezuzyteczna.pl/uzytkownicy/{}', 'urlMain': 'https://bezuzyteczna.pl', 'username_claimed': 'Jackson'}, 'BiggerPockets': {'errorType': 'status_code', 'url': 'https://www.biggerpockets.com/users/{}', 'urlMain': 'https://www.biggerpockets.com/', 'username_claimed': 'blue'}, 'Bikemap': {'errorType': 'status_code', 'url': 'https://www.bikemap.net/en/u/{}/routes/created/', 'urlMain': 'https://www.bikemap.net/', 'username_claimed': 'bikemap'}, 'BioHacking': {'errorType': 'status_code', 'url': 'https://forum.dangerousthings.com/u/{}', 'urlMain': 'https://forum.dangerousthings.com/', 'username_claimed': 'blue'}, 'BitBucket': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9-_]{1,30}$', 'url': 'https://bitbucket.org/{}/', 'urlMain': 'https://bitbucket.org/', 'username_claimed': 'white'}, 'Bitwarden Forum': {'errorType': 'status_code', 'regexCheck': '^(?![.-])[a-zA-Z0-9_.-]{3,20}$', 'url': 'https://community.bitwarden.com/u/{}/summary', 'urlMain': 'https://bitwarden.com/', 'username_claimed': 'blue'}, 'Blipfoto': {'errorType': 'status_code', 'url': 'https://www.blipfoto.com/{}', 'urlMain': 'https://www.blipfoto.com/', 'username_claimed': 'blue'}, 'Blogger': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z][a-zA-Z0-9_-]*$', 'url': 'https://{}.blogspot.com', 'urlMain': 'https://www.blogger.com/', 'username_claimed': 'blue'}, 'BodyBuilding': {'errorType': 'response_url', 'errorUrl': 'https://bodyspace.bodybuilding.com/', 'url': 'https://bodyspace.bodybuilding.com/{}', 'urlMain': 'https://bodyspace.bodybuilding.com/', 'username_claimed': 'blue'}, 'BongaCams': {'errorType': 'status_code', 'isNSFW': True, 'url': 'https://pt.bongacams.com/profile/{}', 'urlMain': 'https://pt.bongacams.com', 'username_claimed': 'asuna-black'}, 'Bookcrossing': {'errorType': 'status_code', 'url': 'https://www.bookcrossing.com/mybookshelf/{}/', 'urlMain': 'https://www.bookcrossing.com/', 'username_claimed': 'blue'}, 'BraveCommunity': {'errorType': 'status_code', 'url': 'https://community.brave.com/u/{}/', 'urlMain': 'https://community.brave.com/', 'username_claimed': 'blue'}, 'BugCrowd': {'errorType': 'status_code', 'url': 'https://bugcrowd.com/{}', 'urlMain': 'https://bugcrowd.com/', 'username_claimed': 'ppfeister'}, 'BuyMeACoffee': {'errorType': 'status_code', 'regexCheck': '[a-zA-Z0-9]{3,15}', 'url': 'https://buymeacoff.ee/{}', 'urlMain': 'https://www.buymeacoffee.com/', 'urlProbe': 'https://www.buymeacoffee.com/{}', 'username_claimed': 'red'}, 'BuzzFeed': {'errorType': 'status_code', 'url': 'https://buzzfeed.com/{}', 'urlMain': 'https://buzzfeed.com/', 'username_claimed': 'blue'}, 'CGTrader': {'errorType': 'status_code', 'regexCheck': '^[^.]*?$', 'url': 'https://www.cgtrader.com/{}', 'urlMain': 'https://www.cgtrader.com', 'username_claimed': 'blue'}, 'CNET': {'errorType': 'status_code', 'regexCheck': '^[a-z].*$', 'url': 'https://www.cnet.com/profiles/{}/', 'urlMain': 'https://www.cnet.com/', 'username_claimed': 'melliott'}, 'CSSBattle': {'errorType': 'status_code', 'url': 'https://cssbattle.dev/player/{}', 'urlMain': 'https://cssbattle.dev', 'username_claimed': 'beo'}, 'CTAN': {'errorType': 'status_code', 'url': 'https://ctan.org/author/{}', 'urlMain': 'https://ctan.org/', 'username_claimed': 'briggs'}, 'Caddy Community': {'errorType': 'status_code', 'url': 'https://caddy.community/u/{}/summary', 'urlMain': 'https://caddy.community/', 'username_claimed': 'taako_magnusen'}, 'Car Talk Community': {'errorType': 'status_code', 'url': 'https://community.cartalk.com/u/{}/summary', 'urlMain': 'https://community.cartalk.com/', 'username_claimed': 'always_fixing'}, 'Carbonmade': {'errorType': 'response_url', 'errorUrl': 'https://carbonmade.com/fourohfour?domain={}.carbonmade.com', 'regexCheck': '^[a-zA-Z0-9@_-]$', 'url': 'https://{}.carbonmade.com', 'urlMain': 'https://carbonmade.com/', 'username_claimed': 'jenny'}, 'Career.habr': {'errorMsg': '<h1>Ошибка 404</h1>', 'errorType': 'message', 'url': 'https://career.habr.com/{}', 'urlMain': 'https://career.habr.com/', 'username_claimed': 'blue'}, 'Championat': {'errorType': 'status_code', 'url': 'https://www.championat.com/user/{}', 'urlMain': 'https://www.championat.com/', 'username_claimed': 'blue'}, 'Chaos': {'errorType': 'status_code', 'url': 'https://chaos.social/@{}', 'urlMain': 'https://chaos.social/', 'username_claimed': 'ordnung'}, 'Chatujme.cz': {'errorMsg': 'Neexistujicí profil', 'errorType': 'message', 'regexCheck': '^[a-zA-Z][a-zA-Z1-9_-]*$', 'url': 'https://profil.chatujme.cz/{}', 'urlMain': 'https://chatujme.cz/', 'username_claimed': 'david'}, 'ChaturBate': {'errorType': 'status_code', 'isNSFW': True, 'url': 'https://chaturbate.com/{}', 'urlMain': 'https://chaturbate.com', 'username_claimed': 'cute18cute'}, 'Chess': {'errorMsg': 'Username is valid', 'errorType': 'message', 'regexCheck': '^[a-z1-9]{3,25}$', 'url': 'https://www.chess.com/member/{}', 'urlMain': 'https://www.chess.com/', 'urlProbe': 'https://www.chess.com/callback/user/valid?username={}', 'username_claimed': 'blue'}, 'Choice Community': {'errorType': 'status_code', 'url': 'https://choice.community/u/{}/summary', 'urlMain': 'https://choice.community/', 'username_claimed': 'gordon'}, 'Clapper': {'errorType': 'status_code', 'url': 'https://clapperapp.com/{}', 'urlMain': 'https://clapperapp.com/', 'username_claimed': 'blue'}, 'CloudflareCommunity': {'errorType': 'status_code', 'url': 'https://community.cloudflare.com/u/{}', 'urlMain': 'https://community.cloudflare.com/', 'username_claimed': 'blue'}, 'Clozemaster': {'errorMsg': 'Oh no! Player not found.', 'errorType': 'message', 'url': 'https://www.clozemaster.com/players/{}', 'urlMain': 'https://www.clozemaster.com', 'username_claimed': 'green'}, 'Clubhouse': {'errorType': 'status_code', 'url': 'https://www.clubhouse.com/@{}', 'urlMain': 'https://www.clubhouse.com', 'username_claimed': 'waniathar'}, 'Code Snippet Wiki': {'errorMsg': 'This user has not filled out their profile page yet', 'errorType': 'message', 'url': 'https://codesnippets.fandom.com/wiki/User:{}', 'urlMain': 'https://codesnippets.fandom.com', 'username_claimed': 'bob'}, 'Codeberg': {'errorType': 'status_code', 'url': 'https://codeberg.org/{}', 'urlMain': 'https://codeberg.org/', 'username_claimed': 'blue'}, 'Codecademy': {'errorMsg': 'This profile could not be found', 'errorType': 'message', 'url': 'https://www.codecademy.com/profiles/{}', 'urlMain': 'https://www.codecademy.com/', 'username_claimed': 'blue'}, 'Codechef': {'errorType': 'response_url', 'errorUrl': 'https://www.codechef.com/', 'url': 'https://www.codechef.com/users/{}', 'urlMain': 'https://www.codechef.com/', 'username_claimed': 'blue'}, 'Codeforces': {'errorType': 'status_code', 'url': 'https://codeforces.com/profile/{}', 'urlMain': 'https://codeforces.com/', 'urlProbe': 'https://codeforces.com/api/user.info?handles={}', 'username_claimed': 'tourist'}, 'Codepen': {'errorType': 'status_code', 'url': 'https://codepen.io/{}', 'urlMain': 'https://codepen.io/', 'username_claimed': 'blue'}, 'Coders Rank': {'errorMsg': 'not a registered member', 'errorType': 'message', 'regexCheck': '^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$', 'url': 'https://profile.codersrank.io/user/{}/', 'urlMain': 'https://codersrank.io/', 'username_claimed': 'rootkit7628'}, 'Coderwall': {'errorType': 'status_code', 'url': 'https://coderwall.com/{}', 'urlMain': 'https://coderwall.com', 'username_claimed': 'hacker'}, 'Codewars': {'errorType': 'status_code', 'url': 'https://www.codewars.com/users/{}', 'urlMain': 'https://www.codewars.com', 'username_claimed': 'example'}, 'Coinvote': {'errorType': 'status_code', 'url': 'https://coinvote.cc/profile/{}', 'urlMain': 'https://coinvote.cc/', 'username_claimed': 'blue'}, 'ColourLovers': {'errorType': 'status_code', 'url': 'https://www.colourlovers.com/lover/{}', 'urlMain': 'https://www.colourlovers.com/', 'username_claimed': 'blue'}, 'Contently': {'errorType': 'response_url', 'errorUrl': 'https://contently.com', 'regexCheck': '^[a-zA-Z][a-zA-Z0-9_-]*$', 'url': 'https://{}.contently.com/', 'urlMain': 'https://contently.com/', 'username_claimed': 'jordanteicher'}, 'Coroflot': {'errorType': 'status_code', 'url': 'https://www.coroflot.com/{}', 'urlMain': 'https://coroflot.com/', 'username_claimed': 'blue'}, 'Cracked': {'errorType': 'response_url', 'errorUrl': 'https://www.cracked.com/', 'url': 'https://www.cracked.com/members/{}/', 'urlMain': 'https://www.cracked.com/', 'username_claimed': 'blue'}, 'Crevado': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9@_-]$', 'url': 'https://{}.crevado.com', 'urlMain': 'https://crevado.com/', 'username_claimed': 'blue'}, 'Crowdin': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9._-]{2,255}$', 'url': 'https://crowdin.com/profile/{}', 'urlMain': 'https://crowdin.com/', 'username_claimed': 'blue'}, 'Cryptomator Forum': {'errorType': 'status_code', 'url': 'https://community.cryptomator.org/u/{}', 'urlMain': 'https://community.cryptomator.org/', 'username_claimed': 'michael'}, 'Cults3D': {'errorMsg': 'Oh dear, this page is not working!', 'errorType': 'message', 'url': 'https://cults3d.com/en/users/{}/creations', 'urlMain': 'https://cults3d.com/en', 'username_claimed': 'brown'}, 'CyberDefenders': {'errorMsg': '<title>Blue Team Training for SOC analysts and DFIR - CyberDefenders</title>', 'errorType': 'message', 'regexCheck': '^[^\\/:*?"<>|@]{3,50}$', 'request_method': 'GET', 'url': 'https://cyberdefenders.org/p/{}', 'urlMain': 'https://cyberdefenders.org/', 'username_claimed': 'mlohn'}, 'DEV Community': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z][a-zA-Z0-9_-]*$', 'url': 'https://dev.to/{}', 'urlMain': 'https://dev.to/', 'username_claimed': 'blue'}, 'DMOJ': {'errorMsg': 'No such user', 'errorType': 'message', 'url': 'https://dmoj.ca/user/{}', 'urlMain': 'https://dmoj.ca/', 'username_claimed': 'junferno'}, 'DailyMotion': {'errorType': 'status_code', 'url': 'https://www.dailymotion.com/{}', 'urlMain': 'https://www.dailymotion.com/', 'username_claimed': 'blue'}, 'Dealabs': {'errorMsg': 'La page que vous essayez', 'errorType': 'message', 'regexCheck': '[a-z0-9]{4,16}', 'url': 'https://www.dealabs.com/profile/{}', 'urlMain': 'https://www.dealabs.com/', 'username_claimed': 'blue'}, 'DeviantART': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z][a-zA-Z0-9_-]*$', 'url': 'https://{}.deviantart.com', 'urlMain': 'https://deviantart.com', 'username_claimed': 'blue'}, 'Discogs': {'errorType': 'status_code', 'url': 'https://www.discogs.com/user/{}', 'urlMain': 'https://www.discogs.com/', 'username_claimed': 'blue'}, 'Discuss.Elastic.co': {'errorType': 'status_code', 'url': 'https://discuss.elastic.co/u/{}', 'urlMain': 'https://discuss.elastic.co/', 'username_claimed': 'blue'}, 'Disqus': {'errorType': 'status_code', 'url': 'https://disqus.com/{}', 'urlMain': 'https://disqus.com/', 'username_claimed': 'blue'}, 'Docker Hub': {'errorType': 'status_code', 'url': 'https://hub.docker.com/u/{}/', 'urlMain': 'https://hub.docker.com/', 'urlProbe': 'https://hub.docker.com/v2/users/{}/', 'username_claimed': 'blue'}, 'Dribbble': {'errorMsg': 'Whoops, that page is gone.', 'errorType': 'message', 'regexCheck': '^[a-zA-Z][a-zA-Z0-9_-]*$', 'url': 'https://dribbble.com/{}', 'urlMain': 'https://dribbble.com/', 'username_claimed': 'blue'}, 'Duolingo': {'errorMsg': '{"users":[]}', 'errorType': 'message', 'headers': {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0'}, 'url': 'https://www.duolingo.com/profile/{}', 'urlMain': 'https://duolingo.com/', 'urlProbe': 'https://www.duolingo.com/2017-06-30/users?username={}', 'username_claimed': 'blue'}, 'Eintracht Frankfurt Forum': {'errorType': 'status_code', 'regexCheck': '^[^.]*?$', 'url': 'https://community.eintracht.de/fans/{}', 'urlMain': 'https://community.eintracht.de/', 'username_claimed': 'mmammu'}, 'Envato Forum': {'errorType': 'status_code', 'url': 'https://forums.envato.com/u/{}', 'urlMain': 'https://forums.envato.com/', 'username_claimed': 'enabled'}, 'Erome': {'errorType': 'status_code', 'isNSFW': True, 'url': 'https://www.erome.com/{}', 'urlMain': 'https://www.erome.com/', 'username_claimed': 'bob'}, 'Exposure': {'errorType': 'status_code', 'url': 'https://{}.exposure.co/', 'urlMain': 'https://exposure.co/', 'username_claimed': 'jonasjacobsson'}, 'EyeEm': {'errorType': 'status_code', 'url': 'https://www.eyeem.com/u/{}', 'urlMain': 'https://www.eyeem.com/', 'username_claimed': 'blue'}, 'F3.cool': {'errorType': 'status_code', 'url': 'https://f3.cool/{}/', 'urlMain': 'https://f3.cool/', 'username_claimed': 'blue'}, 'Fameswap': {'errorType': 'status_code', 'url': 'https://fameswap.com/user/{}', 'urlMain': 'https://fameswap.com/', 'username_claimed': 'fameswap'}, 'Fandom': {'errorType': 'status_code', 'url': 'https://www.fandom.com/u/{}', 'urlMain': 'https://www.fandom.com/', 'username_claimed': 'Jungypoo'}, 'Finanzfrage': {'errorType': 'status_code', 'url': 'https://www.finanzfrage.net/nutzer/{}', 'urlMain': 'https://www.finanzfrage.net/', 'username_claimed': 'finanzfrage'}, 'Fiverr': {'errorMsg': '"status":"success"', 'errorType': 'message', 'regexCheck': '^[A-Za-z][A-Za-z\\d_]{5,14}$', 'request_method': 'POST', 'request_payload': {'username': '{}'}, 'url': 'https://www.fiverr.com/{}', 'urlMain': 'https://www.fiverr.com/', 'urlProbe': 'https://www.fiverr.com/validate_username', 'username_claimed': 'blueman'}, 'Flickr': {'errorType': 'status_code', 'url': 'https://www.flickr.com/people/{}', 'urlMain': 'https://www.flickr.com/', 'username_claimed': 'blue'}, 'Flightradar24': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9_]{3,20}$', 'url': 'https://my.flightradar24.com/{}', 'urlMain': 'https://www.flightradar24.com/', 'username_claimed': 'jebbrooks'}, 'Flipboard': {'errorType': 'status_code', 'regexCheck': '^([a-zA-Z0-9_]){1,15}$', 'url': 'https://flipboard.com/@{}', 'urlMain': 'https://flipboard.com/', 'username_claimed': 'blue'}, 'Football': {'errorMsg': 'Пользователь с таким именем не найден', 'errorType': 'message', 'url': 'https://www.rusfootball.info/user/{}/', 'urlMain': 'https://www.rusfootball.info/', 'username_claimed': 'solo87'}, 'FortniteTracker': {'errorType': 'status_code', 'url': 'https://fortnitetracker.com/profile/all/{}', 'urlMain': 'https://fortnitetracker.com/challenges', 'username_claimed': 'blue'}, 'Forum Ophilia': {'errorMsg': 'that user does not exist', 'errorType': 'message', 'isNSFW': True, 'url': 'https://www.forumophilia.com/profile.php?mode=viewprofile&u={}', 'urlMain': 'https://www.forumophilia.com/', 'username_claimed': 'bob'}, 'Fosstodon': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9_]{1,30}$', 'url': 'https://fosstodon.org/@{}', 'urlMain': 'https://fosstodon.org/', 'username_claimed': 'blue'}, 'Freelance.habr': {'errorMsg': '<div class="icon_user_locked"></div>', 'errorType': 'message', 'regexCheck': '^((?!\\.).)*$', 'url': 'https://freelance.habr.com/freelancers/{}', 'urlMain': 'https://freelance.habr.com/', 'username_claimed': 'adam'}, 'Freelancer': {'errorMsg': '"users":{}', 'errorType': 'message', 'url': 'https://www.freelancer.com/u/{}', 'urlMain': 'https://www.freelancer.com/', 'urlProbe': 'https://www.freelancer.com/api/users/0.1/users?usernames%5B%5D={}&compact=true', 'username_claimed': 'red0xff'}, 'Freesound': {'errorType': 'status_code', 'url': 'https://freesound.org/people/{}/', 'urlMain': 'https://freesound.org/', 'username_claimed': 'blue'}, 'GNOME VCS': {'errorType': 'response_url', 'errorUrl': 'https://gitlab.gnome.org/{}', 'regexCheck': '^(?!-)[a-zA-Z0-9_.-]{2,255}(?<!\\.)$', 'url': 'https://gitlab.gnome.org/{}', 'urlMain': 'https://gitlab.gnome.org/', 'username_claimed': 'adam'}, 'GaiaOnline': {'errorMsg': 'No user ID specified or user does not exist', 'errorType': 'message', 'url': 'https://www.gaiaonline.com/profiles/{}', 'urlMain': 'https://www.gaiaonline.com/', 'username_claimed': 'adam'}, 'Gamespot': {'errorType': 'status_code', 'url': 'https://www.gamespot.com/profile/{}/', 'urlMain': 'https://www.gamespot.com/', 'username_claimed': 'blue'}, 'GeeksforGeeks': {'errorType': 'status_code', 'url': 'https://auth.geeksforgeeks.org/user/{}', 'urlMain': 'https://www.geeksforgeeks.org/', 'username_claimed': 'adam'}, 'Genius (Artists)': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9]{5,50}$', 'url': 'https://genius.com/artists/{}', 'urlMain': 'https://genius.com/', 'username_claimed': 'genius'}, 'Genius (Users)': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9]*?$', 'url': 'https://genius.com/{}', 'urlMain': 'https://genius.com/', 'username_claimed': 'genius'}, 'Gesundheitsfrage': {'errorType': 'status_code', 'url': 'https://www.gesundheitsfrage.net/nutzer/{}', 'urlMain': 'https://www.gesundheitsfrage.net/', 'username_claimed': 'gutefrage'}, 'GetMyUni': {'errorType': 'status_code', 'url': 'https://www.getmyuni.com/user/{}', 'urlMain': 'https://getmyuni.com/', 'username_claimed': 'Upneet.Grover17'}, 'Giant Bomb': {'errorType': 'status_code', 'url': 'https://www.giantbomb.com/profile/{}/', 'urlMain': 'https://www.giantbomb.com/', 'username_claimed': 'bob'}, 'Giphy': {'errorType': 'status_code', 'url': 'https://giphy.com/{}', 'urlMain': 'https://giphy.com/', 'username_claimed': 'blue'}, 'GitBook': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9@_-]$', 'url': 'https://{}.gitbook.io/', 'urlMain': 'https://gitbook.com/', 'username_claimed': 'gitbook'}, 'GitHub': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$', 'url': 'https://www.github.com/{}', 'urlMain': 'https://www.github.com/', 'username_claimed': 'blue'}, 'GitLab': {'errorMsg': '[]', 'errorType': 'message', 'url': 'https://gitlab.com/{}', 'urlMain': 'https://gitlab.com/', 'urlProbe': 'https://gitlab.com/api/v4/users?username={}', 'username_claimed': 'blue'}, 'Gitee': {'errorType': 'status_code', 'url': 'https://gitee.com/{}', 'urlMain': 'https://gitee.com/', 'username_claimed': 'wizzer'}, 'GoodReads': {'errorType': 'status_code', 'url': 'https://www.goodreads.com/{}', 'urlMain': 'https://www.goodreads.com/', 'username_claimed': 'blue'}, 'Google Play': {'errorMsg': 'the requested URL was not found on this server', 'errorType': 'message', 'url': 'https://play.google.com/store/apps/developer?id={}', 'urlMain': 'https://play.google.com', 'username_claimed': 'GitHub'}, 'Gradle': {'errorType': 'status_code', 'regexCheck': '^(?!-)[a-zA-Z0-9-]{3,}(?<!-)$', 'url': 'https://plugins.gradle.org/u/{}', 'urlMain': 'https://gradle.org/', 'username_claimed': 'jetbrains'}, 'Grailed': {'errorType': 'response_url', 'errorUrl': 'https://www.grailed.com/{}', 'url': 'https://www.grailed.com/{}', 'urlMain': 'https://www.grailed.com/', 'username_claimed': 'blue'}, 'Gravatar': {'errorType': 'status_code', 'regexCheck': '^((?!\\.).)*$', 'url': 'http://en.gravatar.com/{}', 'urlMain': 'http://en.gravatar.com/', 'username_claimed': 'blue'}, 'Gumroad': {'errorMsg': 'Page not found (404) - Gumroad', 'errorType': 'message', 'regexCheck': '^[^.]*?$', 'url': 'https://www.gumroad.com/{}', 'urlMain': 'https://www.gumroad.com/', 'username_claimed': 'blue'}, 'Gutefrage': {'errorType': 'status_code', 'url': 'https://www.gutefrage.net/nutzer/{}', 'urlMain': 'https://www.gutefrage.net/', 'username_claimed': 'gutefrage'}, 'HackTheBox': {'errorType': 'status_code', 'url': 'https://forum.hackthebox.eu/profile/{}', 'urlMain': 'https://forum.hackthebox.eu/', 'username_claimed': 'angar'}, 'Hackaday': {'errorType': 'status_code', 'url': 'https://hackaday.io/{}', 'urlMain': 'https://hackaday.io/', 'username_claimed': 'adam'}, 'HackenProof (Hackers)': {'errorMsg': '<title>Web3’s Largest Ethical Hackers Community | HackenProof</title>', 'errorType': 'message', 'regexCheck': '^[\\w-]{,34}$', 'url': 'https://hackenproof.com/hackers/{}', 'urlMain': 'https://hackenproof.com/', 'username_claimed': 'blazezaria'}, 'HackerEarth': {'errorMsg': '404. URL not found.', 'errorType': 'message', 'url': 'https://hackerearth.com/@{}', 'urlMain': 'https://hackerearth.com/', 'username_claimed': 'naveennamani877'}, 'HackerNews': {'__comment__': 'First errMsg invalid, second errMsg rate limited. Not ideal. Adjust for better rate limit filtering.', 'errorMsg': ['No such user.', 'Sorry.'], 'errorType': 'message', 'url': 'https://news.ycombinator.com/user?id={}', 'urlMain': 'https://news.ycombinator.com/', 'username_claimed': 'blue'}, 'HackerOne': {'errorMsg': 'Page not found', 'errorType': 'message', 'url': 'https://hackerone.com/{}', 'urlMain': 'https://hackerone.com/', 'username_claimed': 'stok'}, 'HackerRank': {'errorMsg': 'Something went wrong', 'errorType': 'message', 'regexCheck': '^[^.]*?$', 'url': 'https://hackerrank.com/{}', 'urlMain': 'https://hackerrank.com/', 'username_claimed': 'satznova'}, 'Harvard Scholar': {'errorType': 'status_code', 'url': 'https://scholar.harvard.edu/{}', 'urlMain': 'https://scholar.harvard.edu/', 'username_claimed': 'ousmanekane'}, 'Hashnode': {'errorType': 'status_code', 'url': 'https://hashnode.com/@{}', 'urlMain': 'https://hashnode.com', 'username_claimed': 'blue'}, 'Heavy-R': {'errorMsg': 'Channel not found', 'errorType': 'message', 'isNSFW': True, 'url': 'https://www.heavy-r.com/user/{}', 'urlMain': 'https://www.heavy-r.com/', 'username_claimed': 'kilroy222'}, 'Holopin': {'errorMsg': 'true', 'errorType': 'message', 'request_method': 'POST', 'request_payload': {'username': '{}'}, 'url': 'https://holopin.io/@{}', 'urlMain': 'https://holopin.io', 'urlProbe': 'https://www.holopin.io/api/auth/username', 'username_claimed': 'red'}, 'Houzz': {'errorMsg': 'The page you requested was not found.', 'errorType': 'message', 'url': 'https://houzz.com/user/{}', 'urlMain': 'https://houzz.com/', 'username_claimed': 'blue'}, 'HubPages': {'errorType': 'status_code', 'url': 'https://hubpages.com/@{}', 'urlMain': 'https://hubpages.com/', 'username_claimed': 'blue'}, 'Hubski': {'errorMsg': 'No such user', 'errorType': 'message', 'url': 'https://hubski.com/user/{}', 'urlMain': 'https://hubski.com/', 'username_claimed': 'blue'}, 'HudsonRock': {'errorMsg': 'No results', 'errorType': 'message', 'url': 'https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-username?username={}', 'urlMain': 'https://hudsonrock.com', 'username_claimed': 'testadmin'}, 'ICQ': {'errorType': 'status_code', 'url': 'https://icq.im/{}/en', 'urlMain': 'https://icq.com/', 'username_claimed': 'Micheal'}, 'IFTTT': {'errorType': 'status_code', 'regexCheck': '^[A-Za-z0-9]{3,35}$', 'url': 'https://www.ifttt.com/p/{}', 'urlMain': 'https://www.ifttt.com/', 'username_claimed': 'blue'}, 'IRC-Galleria': {'errorType': 'response_url', 'errorUrl': 'https://irc-galleria.net/users/search?username={}', 'url': 'https://irc-galleria.net/user/{}', 'urlMain': 'https://irc-galleria.net/', 'username_claimed': 'appas'}, 'Icons8 Community': {'errorType': 'status_code', 'url': 'https://community.icons8.com/u/{}/summary', 'urlMain': 'https://community.icons8.com/', 'username_claimed': 'thefourCraft'}, 'Image Fap': {'errorMsg': 'Not found', 'errorType': 'message', 'isNSFW': True, 'url': 'https://www.imagefap.com/profile/{}', 'urlMain': 'https://www.imagefap.com/', 'username_claimed': 'blue'}, 'ImgUp.cz': {'errorType': 'status_code', 'url': 'https://imgup.cz/{}', 'urlMain': 'https://imgup.cz/', 'username_claimed': 'adam'}, 'Imgur': {'errorType': 'status_code', 'url': 'https://imgur.com/user/{}', 'urlMain': 'https://imgur.com/', 'urlProbe': 'https://api.imgur.com/account/v1/accounts/{}?client_id=546c25a59c58ad7', 'username_claimed': 'blue'}, 'Instagram': {'errorType': 'status_code', 'url': 'https://instagram.com/{}', 'urlMain': 'https://instagram.com/', 'urlProbe': 'https://www.picuki.com/profile/{}', 'username_claimed': 'instagram'}, 'Instructables': {'errorType': 'status_code', 'url': 'https://www.instructables.com/member/{}', 'urlMain': 'https://www.instructables.com/', 'urlProbe': 'https://www.instructables.com/json-api/showAuthorExists?screenName={}', 'username_claimed': 'blue'}, 'Intigriti': {'errorType': 'status_code', 'regexCheck': '[a-z0-9_]{1,25}', 'request_method': 'GET', 'url': 'https://app.intigriti.com/profile/{}', 'urlMain': 'https://app.intigriti.com', 'urlProbe': 'https://api.intigriti.com/user/public/profile/{}', 'username_claimed': 'blue'}, 'Ionic Forum': {'errorType': 'status_code', 'url': 'https://forum.ionicframework.com/u/{}', 'urlMain': 'https://forum.ionicframework.com/', 'username_claimed': 'theblue222'}, 'Issuu': {'errorType': 'status_code', 'url': 'https://issuu.com/{}', 'urlMain': 'https://issuu.com/', 'username_claimed': 'jenny'}, 'Itch.io': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9@_-]$', 'url': 'https://{}.itch.io/', 'urlMain': 'https://itch.io/', 'username_claimed': 'blue'}, 'Itemfix': {'errorMsg': '<title>ItemFix - Channel: </title>', 'errorType': 'message', 'url': 'https://www.itemfix.com/c/{}', 'urlMain': 'https://www.itemfix.com/', 'username_claimed': 'blue'}, 'Jellyfin Weblate': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9@._-]{1,150}$', 'url': 'https://translate.jellyfin.org/user/{}/', 'urlMain': 'https://translate.jellyfin.org/', 'username_claimed': 'EraYaN'}, 'Jimdo': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9@_-]$', 'url': 'https://{}.jimdosite.com', 'urlMain': 'https://jimdosite.com/', 'username_claimed': 'jenny'}, 'Joplin Forum': {'errorType': 'status_code', 'url': 'https://discourse.joplinapp.org/u/{}', 'urlMain': 'https://discourse.joplinapp.org/', 'username_claimed': 'laurent'}, 'KEAKR': {'errorType': 'status_code', 'url': 'https://www.keakr.com/en/profile/{}', 'urlMain': 'https://www.keakr.com/', 'username_claimed': 'beats'}, 'Kaggle': {'errorType': 'status_code', 'url': 'https://www.kaggle.com/{}', 'urlMain': 'https://www.kaggle.com/', 'username_claimed': 'dansbecker'}, 'Keybase': {'errorType': 'status_code', 'url': 'https://keybase.io/{}', 'urlMain': 'https://keybase.io/', 'username_claimed': 'blue'}, 'Kick': {'__comment__': 'Cloudflare. Only viable when proxied.', 'errorMsg': 'Not Found', 'errorType': 'message', 'url': 'https://kick.com/{}', 'urlMain': 'https://kick.com/', 'urlProbe': 'https://kick.com/api/v2/channels/{}', 'username_claimed': 'blue'}, 'Kik': {'errorMsg': 'The page you requested was not found', 'errorType': 'message', 'url': 'https://kik.me/{}', 'urlMain': 'http://kik.me/', 'urlProbe': 'https://ws2.kik.com/user/{}', 'username_claimed': 'blue'}, 'Kongregate': {'errorType': 'status_code', 'headers': {'Accept': 'text/html', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0'}, 'regexCheck': '^[a-zA-Z][a-zA-Z0-9_-]*$', 'url': 'https://www.kongregate.com/accounts/{}', 'urlMain': 'https://www.kongregate.com/', 'username_claimed': 'blue'}, 'LOR': {'errorType': 'status_code', 'url': 'https://www.linux.org.ru/people/{}/profile', 'urlMain': 'https://linux.org.ru/', 'username_claimed': 'red'}, 'Launchpad': {'errorType': 'status_code', 'url': 'https://launchpad.net/~{}', 'urlMain': 'https://launchpad.net/', 'username_claimed': 'blue'}, 'LeetCode': {'errorType': 'status_code', 'url': 'https://leetcode.com/u/{}', 'urlMain': 'https://leetcode.com/', 'username_claimed': 'blue'}, 'LessWrong': {'errorType': 'status_code', 'url': 'https://www.lesswrong.com/users/@{}', 'urlMain': 'https://www.lesswrong.com/', 'username_claimed': 'blue'}, 'Letterboxd': {'errorMsg': 'Sorry, we can’t find the page you’ve requested.', 'errorType': 'message', 'url': 'https://letterboxd.com/{}', 'urlMain': 'https://letterboxd.com/', 'username_claimed': 'blue'}, 'LibraryThing': {'errorMsg': 'Catalog your books online', 'errorType': 'message', 'url': 'https://www.librarything.com/profile/{}', 'urlMain': 'https://www.librarything.com/', 'username_claimed': 'blue'}, 'Lichess': {'errorMsg': 'Page not found!', 'errorType': 'message', 'url': 'https://lichess.org/@/{}', 'urlMain': 'https://lichess.org', 'username_claimed': 'blue'}, 'LinkedIn': {'errorType': 'status_code', 'headers': {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36'}, 'regexCheck': '^[a-zA-Z0-9]{3,100}$', 'request_method': 'GET', 'url': 'https://linkedin.com/in/{}', 'urlMain': 'https://linkedin.com', 'username_claimed': 'paulpfeister'}, 'Linktree': {'errorMsg': '"statusCode":404', 'errorType': 'message', 'regexCheck': '^[\\w\\.]{2,30}$', 'url': 'https://linktr.ee/{}', 'urlMain': 'https://linktr.ee/', 'username_claimed': 'anne'}, 'Listed': {'errorType': 'response_url', 'errorUrl': 'https://listed.to/@{}', 'url': 'https://listed.to/@{}', 'urlMain': 'https://listed.to/', 'username_claimed': 'listed'}, 'LiveJournal': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z][a-zA-Z0-9_-]*$', 'url': 'https://{}.livejournal.com', 'urlMain': 'https://www.livejournal.com/', 'username_claimed': 'blue'}, 'Lobsters': {'errorType': 'status_code', 'regexCheck': '[A-Za-z0-9][A-Za-z0-9_-]{0,24}', 'url': 'https://lobste.rs/u/{}', 'urlMain': 'https://lobste.rs/', 'username_claimed': 'jcs'}, 'LottieFiles': {'errorType': 'status_code', 'url': 'https://lottiefiles.com/{}', 'urlMain': 'https://lottiefiles.com/', 'username_claimed': 'lottiefiles'}, 'LushStories': {'errorType': 'status_code', 'isNSFW': True, 'url': 'https://www.lushstories.com/profile/{}', 'urlMain': 'https://www.lushstories.com/', 'username_claimed': 'chris_brown'}, 'MMORPG Forum': {'errorType': 'status_code', 'url': 'https://forums.mmorpg.com/profile/{}', 'urlMain': 'https://forums.mmorpg.com/', 'username_claimed': 'goku'}, 'Mapify': {'errorType': 'response_url', 'errorUrl': 'https://mapify.travel/{}', 'url': 'https://mapify.travel/{}', 'urlMain': 'https://mapify.travel/', 'username_claimed': 'mapify'}, 'Medium': {'errorMsg': '<body', 'errorType': 'message', 'url': 'https://medium.com/@{}', 'urlMain': 'https://medium.com/', 'urlProbe': 'https://medium.com/feed/@{}', 'username_claimed': 'blue'}, 'Memrise': {'errorType': 'status_code', 'url': 'https://www.memrise.com/user/{}/', 'urlMain': 'https://www.memrise.com/', 'username_claimed': 'blue'}, 'Minecraft': {'errorCode': 204, 'errorType': 'status_code', 'url': 'https://api.mojang.com/users/profiles/minecraft/{}', 'urlMain': 'https://minecraft.net/', 'username_claimed': 'blue'}, 'MixCloud': {'errorType': 'status_code', 'url': 'https://www.mixcloud.com/{}/', 'urlMain': 'https://www.mixcloud.com/', 'urlProbe': 'https://api.mixcloud.com/{}/', 'username_claimed': 'jenny'}, 'Monkeytype': {'errorType': 'status_code', 'url': 'https://monkeytype.com/profile/{}', 'urlMain': 'https://monkeytype.com/', 'urlProbe': 'https://api.monkeytype.com/users/{}/profile', 'username_claimed': 'Lost_Arrow'}, 'Motherless': {'errorMsg': 'no longer a member', 'errorType': 'message', 'isNSFW': True, 'url': 'https://motherless.com/m/{}', 'urlMain': 'https://motherless.com/', 'username_claimed': 'hacker'}, 'Motorradfrage': {'errorType': 'status_code', 'url': 'https://www.motorradfrage.net/nutzer/{}', 'urlMain': 'https://www.motorradfrage.net/', 'username_claimed': 'gutefrage'}, 'MyAnimeList': {'errorType': 'status_code', 'url': 'https://myanimelist.net/profile/{}', 'urlMain': 'https://myanimelist.net/', 'username_claimed': 'blue'}, 'MyMiniFactory': {'errorType': 'status_code', 'url': 'https://www.myminifactory.com/users/{}', 'urlMain': 'https://www.myminifactory.com/', 'username_claimed': 'blue'}, 'Mydramalist': {'errorMsg': 'Sign in - MyDramaList', 'errorType': 'message', 'url': 'https://www.mydramalist.com/profile/{}', 'urlMain': 'https://mydramalist.com', 'username_claimed': 'elhadidy12398'}, 'Myspace': {'errorType': 'status_code', 'url': 'https://myspace.com/{}', 'urlMain': 'https://myspace.com/', 'username_claimed': 'blue'}, 'NICommunityForum': {'errorMsg': 'The page you were looking for could not be found.', 'errorType': 'message', 'url': 'https://community.native-instruments.com/profile/{}', 'urlMain': 'https://www.native-instruments.com/forum/', 'username_claimed': 'jambert'}, 'NationStates Nation': {'errorMsg': 'Was this your nation? It may have ceased to exist due to inactivity, but can rise again!', 'errorType': 'message', 'url': 'https://nationstates.net/nation={}', 'urlMain': 'https://nationstates.net', 'username_claimed': 'the_holy_principality_of_saint_mark'}, 'NationStates Region': {'errorMsg': 'does not exist.', 'errorType': 'message', 'url': 'https://nationstates.net/region={}', 'urlMain': 'https://nationstates.net', 'username_claimed': 'the_west_pacific'}, 'Naver': {'errorType': 'status_code', 'url': 'https://blog.naver.com/{}', 'urlMain': 'https://naver.com', 'username_claimed': 'blue'}, 'Needrom': {'errorType': 'status_code', 'url': 'https://www.needrom.com/author/{}/', 'urlMain': 'https://www.needrom.com/', 'username_claimed': 'needrom'}, 'Newgrounds': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z][a-zA-Z0-9_-]*$', 'url': 'https://{}.newgrounds.com', 'urlMain': 'https://newgrounds.com', 'username_claimed': 'blue'}, 'Nextcloud Forum': {'errorType': 'status_code', 'regexCheck': '^(?![.-])[a-zA-Z0-9_.-]{3,20}$', 'url': 'https://help.nextcloud.com/u/{}/summary', 'urlMain': 'https://nextcloud.com/', 'username_claimed': 'blue'}, 'Nightbot': {'errorType': 'status_code', 'url': 'https://nightbot.tv/t/{}/commands', 'urlMain': 'https://nightbot.tv/', 'urlProbe': 'https://api.nightbot.tv/1/channels/t/{}', 'username_claimed': 'green'}, 'Ninja Kiwi': {'errorType': 'response_url', 'errorUrl': 'https://ninjakiwi.com/profile/{}', 'url': 'https://ninjakiwi.com/profile/{}', 'urlMain': 'https://ninjakiwi.com/', 'username_claimed': 'Kyruko'}, 'NintendoLife': {'errorType': 'status_code', 'url': 'https://www.nintendolife.com/users/{}', 'urlMain': 'https://www.nintendolife.com/', 'username_claimed': 'goku'}, 'NitroType': {'errorMsg': '<title>Nitro Type | Competitive Typing Game | Race Your Friends</title>', 'errorType': 'message', 'url': 'https://www.nitrotype.com/racer/{}', 'urlMain': 'https://www.nitrotype.com/', 'username_claimed': 'jianclash'}, 'NotABug.org': {'errorType': 'status_code', 'url': 'https://notabug.org/{}', 'urlMain': 'https://notabug.org/', 'urlProbe': 'https://notabug.org/{}/followers', 'username_claimed': 'red'}, 'Nyaa.si': {'errorType': 'status_code', 'url': 'https://nyaa.si/user/{}', 'urlMain': 'https://nyaa.si/', 'username_claimed': 'blue'}, 'OGUsers': {'errorType': 'status_code', 'url': 'https://ogu.gg/{}', 'urlMain': 'https://ogu.gg/', 'username_claimed': 'ogusers'}, 'OpenStreetMap': {'errorType': 'status_code', 'regexCheck': '^[^.]*?$', 'url': 'https://www.openstreetmap.org/user/{}', 'urlMain': 'https://www.openstreetmap.org/', 'username_claimed': 'blue'}, 'Opensource': {'errorType': 'status_code', 'url': 'https://opensource.com/users/{}', 'urlMain': 'https://opensource.com/', 'username_claimed': 'red'}, 'OurDJTalk': {'errorMsg': 'The specified member cannot be found', 'errorType': 'message', 'url': 'https://ourdjtalk.com/members?username={}', 'urlMain': 'https://ourdjtalk.com/', 'username_claimed': 'steve'}, 'PCGamer': {'errorMsg': "The specified member cannot be found. Please enter a member's entire name.", 'errorType': 'message', 'url': 'https://forums.pcgamer.com/members/?username={}', 'urlMain': 'https://pcgamer.com', 'username_claimed': 'admin'}, 'PSNProfiles.com': {'errorType': 'response_url', 'errorUrl': 'https://psnprofiles.com/?psnId={}', 'url': 'https://psnprofiles.com/{}', 'urlMain': 'https://psnprofiles.com/', 'username_claimed': 'blue'}, 'Packagist': {'errorType': 'response_url', 'errorUrl': 'https://packagist.org/search/?q={}&reason=vendor_not_found', 'url': 'https://packagist.org/packages/{}/', 'urlMain': 'https://packagist.org/', 'username_claimed': 'psr'}, 'Pastebin': {'errorMsg': 'Not Found (#404)', 'errorType': 'message', 'url': 'https://pastebin.com/u/{}', 'urlMain': 'https://pastebin.com/', 'username_claimed': 'blue'}, 'Patreon': {'errorType': 'status_code', 'url': 'https://www.patreon.com/{}', 'urlMain': 'https://www.patreon.com/', 'username_claimed': 'blue'}, 'PentesterLab': {'errorType': 'status_code', 'regexCheck': '^[\\w]{4,30}$', 'url': 'https://pentesterlab.com/profile/{}', 'urlMain': 'https://pentesterlab.com/', 'username_claimed': '0day'}, 'PepperIT': {'errorMsg': 'La pagina che hai provato a raggiungere non si trova qui', 'errorType': 'message', 'url': 'https://www.pepper.it/profile/{}/overview', 'urlMain': 'https://www.pepper.it', 'username_claimed': 'asoluinostrisca'}, 'Periscope': {'errorType': 'status_code', 'url': 'https://www.periscope.tv/{}/', 'urlMain': 'https://www.periscope.tv/', 'username_claimed': 'blue'}, 'Pinkbike': {'errorType': 'status_code', 'regexCheck': '^[^.]*?$', 'url': 'https://www.pinkbike.com/u/{}/', 'urlMain': 'https://www.pinkbike.com/', 'username_claimed': 'blue'}, 'PlayStore': {'errorType': 'status_code', 'url': 'https://play.google.com/store/apps/developer?id={}', 'urlMain': 'https://play.google.com/store', 'username_claimed': 'Facebook'}, 'PocketStars': {'errorMsg': 'Join Your Favorite Adult Stars', 'errorType': 'message', 'isNSFW': True, 'url': 'https://pocketstars.com/{}', 'urlMain': 'https://pocketstars.com/', 'username_claimed': 'hacker'}, 'Pokemon Showdown': {'errorType': 'status_code', 'url': 'https://pokemonshowdown.com/users/{}', 'urlMain': 'https://pokemonshowdown.com', 'username_claimed': 'blue'}, 'Polarsteps': {'errorType': 'status_code', 'url': 'https://polarsteps.com/{}', 'urlMain': 'https://polarsteps.com/', 'urlProbe': 'https://api.polarsteps.com/users/byusername/{}', 'username_claimed': 'james'}, 'Polygon': {'errorType': 'status_code', 'url': 'https://www.polygon.com/users/{}', 'urlMain': 'https://www.polygon.com/', 'username_claimed': 'swiftstickler'}, 'Polymart': {'errorType': 'response_url', 'errorUrl': 'https://polymart.org/user/-1', 'url': 'https://polymart.org/user/{}', 'urlMain': 'https://polymart.org/', 'username_claimed': 'craciu25yt'}, 'Pornhub': {'errorType': 'status_code', 'isNSFW': True, 'url': 'https://pornhub.com/users/{}', 'urlMain': 'https://pornhub.com/', 'username_claimed': 'blue'}, 'ProductHunt': {'errorMsg': 'We seem to have lost this page', 'errorType': 'message', 'url': 'https://www.producthunt.com/@{}', 'urlMain': 'https://www.producthunt.com/', 'username_claimed': 'jenny'}, 'PromoDJ': {'errorType': 'status_code', 'url': 'http://promodj.com/{}', 'urlMain': 'http://promodj.com/', 'username_claimed': 'blue'}, 'PyPi': {'errorType': 'status_code', 'url': 'https://pypi.org/user/{}', 'urlMain': 'https://pypi.org', 'username_claimed': 'Blue'}, 'Rajce.net': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9@_-]$', 'url': 'https://{}.rajce.idnes.cz/', 'urlMain': 'https://www.rajce.idnes.cz/', 'username_claimed': 'blue'}, 'Rate Your Music': {'errorType': 'status_code', 'url': 'https://rateyourmusic.com/~{}', 'urlMain': 'https://rateyourmusic.com/', 'username_claimed': 'blue'}, 'Rclone Forum': {'errorType': 'status_code', 'url': 'https://forum.rclone.org/u/{}', 'urlMain': 'https://forum.rclone.org/', 'username_claimed': 'ncw'}, 'RedTube': {'errorType': 'status_code', 'isNSFW': True, 'url': 'https://www.redtube.com/users/{}', 'urlMain': 'https://www.redtube.com/', 'username_claimed': 'hacker'}, 'Redbubble': {'errorType': 'status_code', 'url': 'https://www.redbubble.com/people/{}', 'urlMain': 'https://www.redbubble.com/', 'username_claimed': 'blue'}, 'Reddit': {'errorMsg': 'Sorry, nobody on Reddit goes by that name.', 'errorType': 'message', 'headers': {'accept-language': 'en-US,en;q=0.9'}, 'url': 'https://www.reddit.com/user/{}', 'urlMain': 'https://www.reddit.com/', 'username_claimed': 'blue'}, 'Reisefrage': {'errorType': 'status_code', 'url': 'https://www.reisefrage.net/nutzer/{}', 'urlMain': 'https://www.reisefrage.net/', 'username_claimed': 'reisefrage'}, 'Replit.com': {'errorType': 'status_code', 'url': 'https://replit.com/@{}', 'urlMain': 'https://replit.com/', 'username_claimed': 'blue'}, 'ResearchGate': {'errorType': 'response_url', 'errorUrl': 'https://www.researchgate.net/directory/profiles', 'regexCheck': '\\w+_\\w+', 'url': 'https://www.researchgate.net/profile/{}', 'urlMain': 'https://www.researchgate.net/', 'username_claimed': 'John_Smith'}, 'ReverbNation': {'errorMsg': "Sorry, we couldn't find that page", 'errorType': 'message', 'url': 'https://www.reverbnation.com/{}', 'urlMain': 'https://www.reverbnation.com/', 'username_claimed': 'blue'}, 'Roblox': {'errorMsg': 'Page cannot be found or no longer exists', 'errorType': 'message', 'url': 'https://www.roblox.com/user.aspx?username={}', 'urlMain': 'https://www.roblox.com/', 'username_claimed': 'bluewolfekiller'}, 'RocketTube': {'errorMsg': 'OOPS! Houston, we have a problem', 'errorType': 'message', 'isNSFW': True, 'url': 'https://www.rockettube.com/{}', 'urlMain': 'https://www.rockettube.com/', 'username_claimed': 'Tatteddick5600'}, 'RoyalCams': {'errorType': 'status_code', 'url': 'https://royalcams.com/profile/{}', 'urlMain': 'https://royalcams.com', 'username_claimed': 'asuna-black'}, 'RubyGems': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z][a-zA-Z0-9_-]{1,40}', 'url': 'https://rubygems.org/profiles/{}', 'urlMain': 'https://rubygems.org/', 'username_claimed': 'blue'}, 'Rumble': {'errorType': 'status_code', 'url': 'https://rumble.com/user/{}', 'urlMain': 'https://rumble.com/', 'username_claimed': 'John'}, 'RuneScape': {'errorMsg': '{"error":"NO_PROFILE","loggedIn":"false"}', 'errorType': 'message', 'regexCheck': '^(?! )[\\w -]{1,12}(?<! )$', 'url': 'https://apps.runescape.com/runemetrics/app/overview/player/{}', 'urlMain': 'https://www.runescape.com/', 'urlProbe': 'https://apps.runescape.com/runemetrics/profile/profile?user={}', 'username_claimed': 'L33'}, 'SWAPD': {'errorType': 'status_code', 'url': 'https://swapd.co/u/{}', 'urlMain': 'https://swapd.co/', 'username_claimed': 'swapd'}, 'Sbazar.cz': {'errorType': 'status_code', 'url': 'https://www.sbazar.cz/{}', 'urlMain': 'https://www.sbazar.cz/', 'username_claimed': 'blue'}, 'Scratch': {'errorType': 'status_code', 'url': 'https://scratch.mit.edu/users/{}', 'urlMain': 'https://scratch.mit.edu/', 'username_claimed': 'griffpatch'}, 'Scribd': {'errorMsg': 'Page not found', 'errorType': 'message', 'url': 'https://www.scribd.com/{}', 'urlMain': 'https://www.scribd.com/', 'username_claimed': 'blue'}, 'ShitpostBot5000': {'errorType': 'status_code', 'url': 'https://www.shitpostbot.com/user/{}', 'urlMain': 'https://www.shitpostbot.com/', 'username_claimed': 'blue'}, 'Shpock': {'errorType': 'status_code', 'url': 'https://www.shpock.com/shop/{}/items', 'urlMain': 'https://www.shpock.com/', 'username_claimed': 'user'}, 'Signal': {'errorMsg': 'Oops! That page doesn’t exist or is private.', 'errorType': 'message', 'url': 'https://community.signalusers.org/u/{}', 'urlMain': 'https://community.signalusers.org', 'username_claimed': 'jlund'}, 'Sketchfab': {'errorType': 'status_code', 'url': 'https://sketchfab.com/{}', 'urlMain': 'https://sketchfab.com/', 'username_claimed': 'blue'}, 'Slack': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z][a-zA-Z0-9_-]*$', 'url': 'https://{}.slack.com', 'urlMain': 'https://slack.com', 'username_claimed': 'blue'}, 'Slant': {'errorType': 'status_code', 'regexCheck': '^.{2,32}$', 'url': 'https://www.slant.co/users/{}', 'urlMain': 'https://www.slant.co/', 'username_claimed': 'blue'}, 'Slashdot': {'errorMsg': 'user you requested does not exist', 'errorType': 'message', 'url': 'https://slashdot.org/~{}', 'urlMain': 'https://slashdot.org', 'username_claimed': 'blue'}, 'SlideShare': {'errorType': 'status_code', 'url': 'https://slideshare.net/{}', 'urlMain': 'https://slideshare.net/', 'username_claimed': 'blue'}, 'Slides': {'errorCode': 204, 'errorType': 'status_code', 'url': 'https://slides.com/{}', 'urlMain': 'https://slides.com/', 'username_claimed': 'blue'}, 'SmugMug': {'errorType': 'status_code', 'url': 'https://{}.smugmug.com', 'urlMain': 'https://smugmug.com', 'username_claimed': 'winchester'}, 'Smule': {'errorMsg': 'Smule | Page Not Found (404)', 'errorType': 'message', 'url': 'https://www.smule.com/{}', 'urlMain': 'https://www.smule.com/', 'username_claimed': 'blue'}, 'Snapchat': {'errorType': 'status_code', 'regexCheck': '^[a-z][a-z-_.]{3,15}', 'request_method': 'GET', 'url': 'https://www.snapchat.com/add/{}', 'urlMain': 'https://www.snapchat.com', 'username_claimed': 'teamsnapchat'}, 'SoundCloud': {'errorType': 'status_code', 'url': 'https://soundcloud.com/{}', 'urlMain': 'https://soundcloud.com/', 'username_claimed': 'blue'}, 'SourceForge': {'errorType': 'status_code', 'url': 'https://sourceforge.net/u/{}', 'urlMain': 'https://sourceforge.net/', 'username_claimed': 'blue'}, 'SoylentNews': {'errorMsg': 'The user you requested does not exist, no matter how much you wish this might be the case.', 'errorType': 'message', 'url': 'https://soylentnews.org/~{}', 'urlMain': 'https://soylentnews.org', 'username_claimed': 'adam'}, 'Speedrun.com': {'errorMsg': 'Not found', 'errorType': 'message', 'url': 'https://speedrun.com/user/{}', 'urlMain': 'https://speedrun.com/', 'username_claimed': '3Tau'}, 'Spells8': {'errorType': 'status_code', 'url': 'https://forum.spells8.com/u/{}', 'urlMain': 'https://spells8.com', 'username_claimed': 'susurrus'}, 'Splice': {'errorType': 'status_code', 'url': 'https://splice.com/{}', 'urlMain': 'https://splice.com/', 'username_claimed': 'splice'}, 'Splits.io': {'errorType': 'status_code', 'regexCheck': '^[^.]*?$', 'url': 'https://splits.io/users/{}', 'urlMain': 'https://splits.io', 'username_claimed': 'cambosteve'}, 'Sporcle': {'errorType': 'status_code', 'url': 'https://www.sporcle.com/user/{}/people', 'urlMain': 'https://www.sporcle.com/', 'username_claimed': 'blue'}, 'Sportlerfrage': {'errorType': 'status_code', 'url': 'https://www.sportlerfrage.net/nutzer/{}', 'urlMain': 'https://www.sportlerfrage.net/', 'username_claimed': 'sportlerfrage'}, 'SportsRU': {'errorType': 'status_code', 'url': 'https://www.sports.ru/profile/{}/', 'urlMain': 'https://www.sports.ru/', 'username_claimed': 'blue'}, 'Spotify': {'errorType': 'status_code', 'headers': {'user-agent': 'PostmanRuntime/7.29.2'}, 'url': 'https://open.spotify.com/user/{}', 'urlMain': 'https://open.spotify.com/', 'username_claimed': 'blue'}, 'Star Citizen': {'errorMsg': '404', 'errorType': 'message', 'url': 'https://robertsspaceindustries.com/citizens/{}', 'urlMain': 'https://robertsspaceindustries.com/', 'username_claimed': 'blue'}, 'Steam Community (Group)': {'errorMsg': 'No group could be retrieved for the given URL', 'errorType': 'message', 'url': 'https://steamcommunity.com/groups/{}', 'urlMain': 'https://steamcommunity.com/', 'username_claimed': 'blue'}, 'Steam Community (User)': {'errorMsg': 'The specified profile could not be found', 'errorType': 'message', 'url': 'https://steamcommunity.com/id/{}/', 'urlMain': 'https://steamcommunity.com/', 'username_claimed': 'blue'}, 'Strava': {'errorMsg': 'Strava | Running, Cycling &amp; Hiking App - Train, Track &amp; Share', 'errorType': 'message', 'regexCheck': '^[^.]*?$', 'url': 'https://www.strava.com/athletes/{}', 'urlMain': 'https://www.strava.com/', 'username_claimed': 'blue'}, 'SublimeForum': {'errorType': 'status_code', 'url': 'https://forum.sublimetext.com/u/{}', 'urlMain': 'https://forum.sublimetext.com/', 'username_claimed': 'blue'}, 'TETR.IO': {'errorMsg': 'No such user!', 'errorType': 'message', 'url': 'https://ch.tetr.io/u/{}', 'urlMain': 'https://tetr.io', 'urlProbe': 'https://ch.tetr.io/api/users/{}', 'username_claimed': 'osk'}, 'TLDR Legal': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9]{3,20}$', 'url': 'https://tldrlegal.com/users/{}/', 'urlMain': 'https://tldrlegal.com/', 'username_claimed': 'kevin'}, 'TRAKTRAIN': {'errorType': 'status_code', 'url': 'https://traktrain.com/{}', 'urlMain': 'https://traktrain.com/', 'username_claimed': 'traktrain'}, 'Telegram': {'errorMsg': ['<title>Telegram Messenger</title>', 'If you have <strong>Telegram</strong>, you can contact <a class="tgme_username_link" href="tg://resolve?domain='], 'errorType': 'message', 'regexCheck': '^[a-zA-Z0-9_]{3,32}[^_]$', 'url': 'https://t.me/{}', 'urlMain': 'https://t.me/', 'username_claimed': 'blue'}, 'Tellonym.me': {'errorType': 'status_code', 'url': 'https://tellonym.me/{}', 'urlMain': 'https://tellonym.me/', 'username_claimed': 'blue'}, 'Tenor': {'errorType': 'status_code', 'regexCheck': '^[A-Za-z0-9_]{2,32}$', 'url': 'https://tenor.com/users/{}', 'urlMain': 'https://tenor.com/', 'username_claimed': 'red'}, 'ThemeForest': {'errorType': 'status_code', 'url': 'https://themeforest.net/user/{}', 'urlMain': 'https://themeforest.net/', 'username_claimed': 'user'}, 'TnAFlix': {'errorType': 'status_code', 'isNSFW': True, 'url': 'https://www.tnaflix.com/profile/{}', 'urlMain': 'https://www.tnaflix.com/', 'username_claimed': 'hacker'}, 'TorrentGalaxy': {'errorMsg': "<title>TGx:Can't show details</title>", 'errorType': 'message', 'regexCheck': '^[A-Za-z0-9]{3,15}$', 'url': 'https://torrentgalaxy.to/profile/{}', 'urlMain': 'https://torrentgalaxy.to/', 'username_claimed': 'GalaxyRG'}, 'TradingView': {'errorType': 'status_code', 'request_method': 'GET', 'url': 'https://www.tradingview.com/u/{}/', 'urlMain': 'https://www.tradingview.com/', 'username_claimed': 'blue'}, 'Trakt': {'errorType': 'status_code', 'regexCheck': '^[^.]*$', 'url': 'https://www.trakt.tv/users/{}', 'urlMain': 'https://www.trakt.tv/', 'username_claimed': 'blue'}, 'TrashboxRU': {'errorType': 'status_code', 'regexCheck': '^[A-Za-z0-9_-]{3,16}$', 'url': 'https://trashbox.ru/users/{}', 'urlMain': 'https://trashbox.ru/', 'username_claimed': 'blue'}, 'Trawelling': {'errorType': 'status_code', 'url': 'https://traewelling.de/@{}', 'urlMain': 'https://traewelling.de/', 'username_claimed': 'lassestolley'}, 'Trello': {'errorMsg': 'model not found', 'errorType': 'message', 'url': 'https://trello.com/{}', 'urlMain': 'https://trello.com/', 'urlProbe': 'https://trello.com/1/Members/{}', 'username_claimed': 'blue'}, 'TryHackMe': {'errorMsg': '{"success":false}', 'errorType': 'message', 'regexCheck': '^[a-zA-Z0-9.]{1,16}$', 'url': 'https://tryhackme.com/p/{}', 'urlMain': 'https://tryhackme.com/', 'urlProbe': 'https://tryhackme.com/api/user/exist/{}', 'username_claimed': 'ashu'}, 'Tuna': {'errorType': 'status_code', 'regexCheck': '^[a-z0-9]{4,40}$', 'url': 'https://tuna.voicemod.net/user/{}', 'urlMain': 'https://tuna.voicemod.net/', 'username_claimed': 'bob'}, 'Tweakers': {'errorType': 'status_code', 'url': 'https://tweakers.net/gallery/{}', 'urlMain': 'https://tweakers.net', 'username_claimed': 'femme'}, 'Twitch': {'errorType': 'status_code', 'url': 'https://www.twitch.tv/{}', 'urlMain': 'https://www.twitch.tv/', 'urlProbe': 'https://m.twitch.tv/{}', 'username_claimed': 'jenny'}, 'Twitter': {'errorMsg': '<div class="error-panel"><span>User ', 'errorType': 'message', 'regexCheck': '^[a-zA-Z0-9_]{1,15}$', 'url': 'https://x.com/{}', 'urlMain': 'https://x.com/', 'urlProbe': 'https://nitter.net/{}', 'username_claimed': 'blue'}, 'Typeracer': {'errorMsg': 'Profile Not Found', 'errorType': 'message', 'url': 'https://data.typeracer.com/pit/profile?user={}', 'urlMain': 'https://typeracer.com', 'username_claimed': 'blue'}, 'Ultimate-Guitar': {'errorType': 'status_code', 'url': 'https://ultimate-guitar.com/u/{}', 'urlMain': 'https://ultimate-guitar.com/', 'username_claimed': 'blue'}, 'Unsplash': {'errorType': 'status_code', 'regexCheck': '^[a-z0-9_]{1,60}$', 'url': 'https://unsplash.com/@{}', 'urlMain': 'https://unsplash.com/', 'username_claimed': 'jenny'}, 'Untappd': {'errorType': 'status_code', 'url': 'https://untappd.com/user/{}', 'urlMain': 'https://untappd.com/', 'username_claimed': 'untappd'}, 'VK': {'errorType': 'response_url', 'errorUrl': 'https://www.quora.com/profile/{}', 'url': 'https://vk.com/{}', 'urlMain': 'https://vk.com/', 'username_claimed': 'brown'}, 'VSCO': {'errorType': 'status_code', 'url': 'https://vsco.co/{}', 'urlMain': 'https://vsco.co/', 'username_claimed': 'blue'}, 'Velomania': {'errorMsg': 'Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'errorType': 'message', 'url': 'https://forum.velomania.ru/member.php?username={}', 'urlMain': 'https://forum.velomania.ru/', 'username_claimed': 'red'}, 'Venmo': {'errorMsg': ['Venmo | Page Not Found'], 'errorType': 'message', 'headers': {'Host': 'account.venmo.com'}, 'url': 'https://account.venmo.com/u/{}', 'urlMain': 'https://venmo.com/', 'urlProbe': 'https://test1.venmo.com/u/{}', 'username_claimed': 'jenny'}, 'Vero': {'errorType': 'status_code', 'request_method': 'GET', 'url': 'https://vero.co/{}', 'urlMain': 'https://vero.co/', 'username_claimed': 'blue'}, 'Vimeo': {'errorType': 'status_code', 'url': 'https://vimeo.com/{}', 'urlMain': 'https://vimeo.com/', 'username_claimed': 'blue'}, 'VirusTotal': {'errorType': 'status_code', 'request_method': 'GET', 'url': 'https://www.virustotal.com/gui/user/{}', 'urlMain': 'https://www.virustotal.com/', 'urlProbe': 'https://www.virustotal.com/ui/users/{}/avatar', 'username_claimed': 'blue'}, 'WICG Forum': {'errorType': 'status_code', 'regexCheck': '^(?![.-])[a-zA-Z0-9_.-]{3,20}$', 'url': 'https://discourse.wicg.io/u/{}/summary', 'urlMain': 'https://discourse.wicg.io/', 'username_claimed': 'stefano'}, 'Warrior Forum': {'errorType': 'status_code', 'url': 'https://www.warriorforum.com/members/{}.html', 'urlMain': 'https://www.warriorforum.com/', 'username_claimed': 'blue'}, 'Wattpad': {'errorType': 'status_code', 'url': 'https://www.wattpad.com/user/{}', 'urlMain': 'https://www.wattpad.com/', 'urlProbe': 'https://www.wattpad.com/api/v3/users/{}/', 'username_claimed': 'Dogstho7951'}, 'WebNode': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9@_-]$', 'url': 'https://{}.webnode.cz/', 'urlMain': 'https://www.webnode.cz/', 'username_claimed': 'radkabalcarova'}, 'Weblate': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9@._-]{1,150}$', 'url': 'https://hosted.weblate.org/user/{}/', 'urlMain': 'https://hosted.weblate.org/', 'username_claimed': 'adam'}, 'Weebly': {'errorType': 'status_code', 'url': 'https://{}.weebly.com/', 'urlMain': 'https://weebly.com/', 'username_claimed': 'blue'}, 'Wikidot': {'errorMsg': 'User does not exist.', 'errorType': 'message', 'url': 'http://www.wikidot.com/user:info/{}', 'urlMain': 'http://www.wikidot.com/', 'username_claimed': 'blue'}, 'Wikipedia': {'errorMsg': 'centralauth-admin-nonexistent:', 'errorType': 'message', 'url': 'https://en.wikipedia.org/wiki/Special:CentralAuth/{}?uselang=qqx', 'urlMain': 'https://www.wikipedia.org/', 'username_claimed': 'Hoadlck'}, 'Windy': {'errorType': 'status_code', 'url': 'https://community.windy.com/user/{}', 'urlMain': 'https://windy.com/', 'username_claimed': 'blue'}, 'Wix': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9@_-]$', 'url': 'https://{}.wix.com', 'urlMain': 'https://wix.com/', 'username_claimed': 'support'}, 'WolframalphaForum': {'errorType': 'status_code', 'url': 'https://community.wolfram.com/web/{}/home', 'urlMain': 'https://community.wolfram.com/', 'username_claimed': 'unico'}, 'WordPress': {'errorType': 'response_url', 'errorUrl': 'wordpress.com/typo/?subdomain=', 'regexCheck': '^[a-zA-Z][a-zA-Z0-9_-]*$', 'url': 'https://{}.wordpress.com/', 'urlMain': 'https://wordpress.com', 'username_claimed': 'blue'}, 'WordPressOrg': {'errorType': 'response_url', 'errorUrl': 'https://wordpress.org', 'url': 'https://profiles.wordpress.org/{}/', 'urlMain': 'https://wordpress.org/', 'username_claimed': 'blue'}, 'Wordnik': {'errorMsg': 'Page Not Found', 'errorType': 'message', 'regexCheck': '^[a-zA-Z0-9_.+-]{1,40}$', 'url': 'https://www.wordnik.com/users/{}', 'urlMain': 'https://www.wordnik.com/', 'username_claimed': 'blue'}, 'Wykop': {'errorType': 'status_code', 'url': 'https://www.wykop.pl/ludzie/{}', 'urlMain': 'https://www.wykop.pl', 'username_claimed': 'blue'}, 'Xbox Gamertag': {'errorType': 'status_code', 'url': 'https://xboxgamertag.com/search/{}', 'urlMain': 'https://xboxgamertag.com/', 'username_claimed': 'red'}, 'Xvideos': {'errorType': 'status_code', 'isNSFW': True, 'url': 'https://xvideos.com/profiles/{}', 'urlMain': 'https://xvideos.com/', 'username_claimed': 'blue'}, 'YandexMusic': {'__comment__': 'The first and third errorMsg relate to geo-restrictions and bot detection/captchas.', 'errorMsg': ['Ошибка 404', '<meta name="description" content="Открывайте новую музыку каждый день.', '<input type="submit" class="CheckboxCaptcha-Button"'], 'errorType': 'message', 'url': 'https://music.yandex/users/{}/playlists', 'urlMain': 'https://music.yandex', 'username_claimed': 'ya.playlist'}, 'YouNow': {'errorMsg': 'No users found', 'errorType': 'message', 'url': 'https://www.younow.com/{}/', 'urlMain': 'https://www.younow.com/', 'urlProbe': 'https://api.younow.com/php/api/broadcast/info/user={}/', 'username_claimed': 'blue'}, 'YouPic': {'errorType': 'status_code', 'url': 'https://youpic.com/photographer/{}/', 'urlMain': 'https://youpic.com/', 'username_claimed': 'blue'}, 'YouPorn': {'errorType': 'status_code', 'isNSFW': True, 'url': 'https://youporn.com/uservids/{}', 'urlMain': 'https://youporn.com', 'username_claimed': 'blue'}, 'YouTube': {'errorType': 'status_code', 'headers': {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36'}, 'url': 'https://www.youtube.com/@{}', 'urlMain': 'https://www.youtube.com/', 'username_claimed': 'youtube'}, 'akniga': {'errorType': 'status_code', 'url': 'https://akniga.org/profile/{}', 'urlMain': 'https://akniga.org/profile/blue/', 'username_claimed': 'blue'}, 'authorSTREAM': {'errorType': 'status_code', 'url': 'http://www.authorstream.com/{}/', 'urlMain': 'http://www.authorstream.com/', 'username_claimed': 'blue'}, 'babyRU': {'errorMsg': 'Страница, которую вы искали, не найдена', 'errorType': 'message', 'url': 'https://www.baby.ru/u/{}/', 'urlMain': 'https://www.baby.ru/', 'username_claimed': 'blue'}, 'babyblogRU': {'errorType': 'response_url', 'errorUrl': 'https://www.babyblog.ru/', 'url': 'https://www.babyblog.ru/user/{}', 'urlMain': 'https://www.babyblog.ru/', 'username_claimed': 'blue'}, 'chaos.social': {'errorType': 'status_code', 'url': 'https://chaos.social/@{}', 'urlMain': 'https://chaos.social/', 'username_claimed': 'rixx'}, 'couchsurfing': {'errorType': 'status_code', 'url': 'https://www.couchsurfing.com/people/{}', 'urlMain': 'https://www.couchsurfing.com/', 'username_claimed': 'blue'}, 'd3RU': {'errorType': 'status_code', 'url': 'https://d3.ru/user/{}/posts', 'urlMain': 'https://d3.ru/', 'username_claimed': 'blue'}, 'dailykos': {'errorMsg': '{"result":true,"message":null}', 'errorType': 'message', 'url': 'https://www.dailykos.com/user/{}', 'urlMain': 'https://www.dailykos.com', 'urlProbe': 'https://www.dailykos.com/signup/check_nickname?nickname={}', 'username_claimed': 'blue'}, 'datingRU': {'errorType': 'status_code', 'url': 'http://dating.ru/{}', 'urlMain': 'http://dating.ru', 'username_claimed': 'blue'}, 'devRant': {'errorType': 'response_url', 'errorUrl': 'https://devrant.com/', 'url': 'https://devrant.com/users/{}', 'urlMain': 'https://devrant.com/', 'username_claimed': 'blue'}, 'drive2': {'errorType': 'status_code', 'url': 'https://www.drive2.ru/users/{}', 'urlMain': 'https://www.drive2.ru/', 'username_claimed': 'blue'}, 'eGPU': {'errorType': 'status_code', 'url': 'https://egpu.io/forums/profile/{}/', 'urlMain': 'https://egpu.io/', 'username_claimed': 'blue'}, 'eintracht': {'errorType': 'status_code', 'regexCheck': '^[^.]*?$', 'url': 'https://community.eintracht.de/fans/{}', 'urlMain': 'https://eintracht.de', 'username_claimed': 'blue'}, 'fixya': {'errorType': 'status_code', 'url': 'https://www.fixya.com/users/{}', 'urlMain': 'https://www.fixya.com', 'username_claimed': 'adam'}, 'fl': {'errorType': 'status_code', 'url': 'https://www.fl.ru/users/{}', 'urlMain': 'https://www.fl.ru/', 'username_claimed': 'blue'}, 'forum_guns': {'errorMsg': 'action=https://forum.guns.ru/forummisc/blog/search', 'errorType': 'message', 'url': 'https://forum.guns.ru/forummisc/blog/{}', 'urlMain': 'https://forum.guns.ru/', 'username_claimed': 'red'}, 'freecodecamp': {'errorType': 'status_code', 'url': 'https://www.freecodecamp.org/{}', 'urlMain': 'https://www.freecodecamp.org/', 'urlProbe': 'https://api.freecodecamp.org/api/users/get-public-profile?username={}', 'username_claimed': 'naveennamani'}, 'furaffinity': {'errorMsg': 'This user cannot be found.', 'errorType': 'message', 'url': 'https://www.furaffinity.net/user/{}', 'urlMain': 'https://www.furaffinity.net', 'username_claimed': 'jesus'}, 'geocaching': {'errorType': 'status_code', 'url': 'https://www.geocaching.com/p/default.aspx?u={}', 'urlMain': 'https://www.geocaching.com/', 'username_claimed': 'blue'}, 'gfycat': {'errorType': 'status_code', 'url': 'https://gfycat.com/@{}', 'urlMain': 'https://gfycat.com/', 'username_claimed': 'Test'}, 'habr': {'errorType': 'status_code', 'url': 'https://habr.com/ru/users/{}', 'urlMain': 'https://habr.com/', 'username_claimed': 'blue'}, 'hackster': {'errorType': 'status_code', 'url': 'https://www.hackster.io/{}', 'urlMain': 'https://www.hackster.io', 'username_claimed': 'blue'}, 'hunting': {'errorMsg': 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', 'errorType': 'message', 'url': 'https://www.hunting.ru/forum/members/?username={}', 'urlMain': 'https://www.hunting.ru/forum/', 'username_claimed': 'red'}, 'iMGSRC.RU': {'errorType': 'response_url', 'errorUrl': 'https://imgsrc.ru/', 'url': 'https://imgsrc.ru/main/user.php?user={}', 'urlMain': 'https://imgsrc.ru/', 'username_claimed': 'blue'}, 'igromania': {'errorMsg': 'Пользователь не зарегистрирован и не имеет профиля для просмотра.', 'errorType': 'message', 'url': 'http://forum.igromania.ru/member.php?username={}', 'urlMain': 'http://forum.igromania.ru/', 'username_claimed': 'blue'}, 'interpals': {'errorMsg': 'The requested user does not exist or is inactive', 'errorType': 'message', 'url': 'https://www.interpals.net/{}', 'urlMain': 'https://www.interpals.net/', 'username_claimed': 'blue'}, 'irecommend': {'errorType': 'status_code', 'url': 'https://irecommend.ru/users/{}', 'urlMain': 'https://irecommend.ru/', 'username_claimed': 'blue'}, 'jbzd.com.pl': {'errorType': 'status_code', 'url': 'https://jbzd.com.pl/uzytkownik/{}', 'urlMain': 'https://jbzd.com.pl/', 'username_claimed': 'blue'}, 'jeuxvideo': {'errorType': 'status_code', 'request_method': 'GET', 'url': 'https://www.jeuxvideo.com/profil/{}', 'urlMain': 'https://www.jeuxvideo.com', 'urlProbe': 'https://www.jeuxvideo.com/profil/{}?mode=infos', 'username_claimed': 'adam'}, 'kofi': {'errorType': 'response_url', 'errorUrl': 'https://ko-fi.com/art?=redirect', 'url': 'https://ko-fi.com/{}', 'urlMain': 'https://ko-fi.com', 'username_claimed': 'yeahkenny'}, 'kwork': {'errorType': 'status_code', 'url': 'https://kwork.ru/user/{}', 'urlMain': 'https://www.kwork.ru/', 'username_claimed': 'blue'}, 'last.fm': {'errorType': 'status_code', 'url': 'https://last.fm/user/{}', 'urlMain': 'https://last.fm/', 'username_claimed': 'blue'}, 'leasehackr': {'errorType': 'status_code', 'url': 'https://forum.leasehackr.com/u/{}/summary/', 'urlMain': 'https://forum.leasehackr.com/', 'username_claimed': 'adam'}, 'livelib': {'errorType': 'status_code', 'url': 'https://www.livelib.ru/reader/{}', 'urlMain': 'https://www.livelib.ru/', 'username_claimed': 'blue'}, 'mastodon.cloud': {'errorType': 'status_code', 'url': 'https://mastodon.cloud/@{}', 'urlMain': 'https://mastodon.cloud/', 'username_claimed': 'TheAdmin'}, 'mastodon.social': {'errorType': 'status_code', 'url': 'https://mastodon.social/@{}', 'urlMain': 'https://chaos.social/', 'username_claimed': 'Gargron'}, 'mastodon.technology': {'errorType': 'status_code', 'url': 'https://mastodon.technology/@{}', 'urlMain': 'https://mastodon.xyz/', 'username_claimed': 'ashfurrow'}, 'mastodon.xyz': {'errorType': 'status_code', 'url': 'https://mastodon.xyz/@{}', 'urlMain': 'https://mastodon.xyz/', 'username_claimed': 'TheKinrar'}, 'mercadolivre': {'errorType': 'status_code', 'url': 'https://www.mercadolivre.com.br/perfil/{}', 'urlMain': 'https://www.mercadolivre.com.br', 'username_claimed': 'blue'}, 'minds': {'errorMsg': '"valid":true', 'errorType': 'message', 'url': 'https://www.minds.com/{}/', 'urlMain': 'https://www.minds.com', 'urlProbe': 'https://www.minds.com/api/v3/register/validate?username={}', 'username_claimed': 'john'}, 'moikrug': {'errorType': 'status_code', 'url': 'https://moikrug.ru/{}', 'urlMain': 'https://moikrug.ru/', 'username_claimed': 'blue'}, 'mstdn.io': {'errorType': 'status_code', 'url': 'https://mstdn.io/@{}', 'urlMain': 'https://mstdn.io/', 'username_claimed': 'blue'}, 'nairaland.com': {'errorType': 'status_code', 'url': 'https://www.nairaland.com/{}', 'urlMain': 'https://www.nairaland.com/', 'username_claimed': 'red'}, 'nnRU': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9@_-]$', 'url': 'https://{}.www.nn.ru/', 'urlMain': 'https://www.nn.ru/', 'username_claimed': 'blue'}, 'note': {'errorType': 'status_code', 'url': 'https://note.com/{}', 'urlMain': 'https://note.com/', 'username_claimed': 'blue'}, 'npm': {'errorType': 'status_code', 'url': 'https://www.npmjs.com/~{}', 'urlMain': 'https://www.npmjs.com/', 'username_claimed': 'kennethsweezy'}, 'opennet': {'errorMsg': 'Имя участника не найдено', 'errorType': 'message', 'regexCheck': '^[^-]*$', 'url': 'https://www.opennet.ru/~{}', 'urlMain': 'https://www.opennet.ru/', 'username_claimed': 'anonismus'}, 'osu!': {'errorType': 'status_code', 'url': 'https://osu.ppy.sh/users/{}', 'urlMain': 'https://osu.ppy.sh/', 'username_claimed': 'blue'}, 'phpRU': {'errorMsg': 'Указанный пользователь не найден. Пожалуйста, введите другое имя.', 'errorType': 'message', 'url': 'https://php.ru/forum/members/?username={}', 'urlMain': 'https://php.ru/forum/', 'username_claimed': 'apple'}, 'pikabu': {'errorType': 'status_code', 'url': 'https://pikabu.ru/@{}', 'urlMain': 'https://pikabu.ru/', 'username_claimed': 'blue'}, 'pr0gramm': {'errorType': 'status_code', 'url': 'https://pr0gramm.com/user/{}', 'urlMain': 'https://pr0gramm.com/', 'urlProbe': 'https://pr0gramm.com/api/profile/info?name={}', 'username_claimed': 'cha0s'}, 'prog.hu': {'errorType': 'response_url', 'errorUrl': 'https://prog.hu/azonosito/info/{}', 'url': 'https://prog.hu/azonosito/info/{}', 'urlMain': 'https://prog.hu/', 'username_claimed': 'Sting'}, 'queer.af': {'errorType': 'status_code', 'url': 'https://queer.af/@{}', 'urlMain': 'https://queer.af/', 'username_claimed': 'erincandescent'}, 'satsisRU': {'errorType': 'status_code', 'url': 'https://satsis.info/user/{}', 'urlMain': 'https://satsis.info/', 'username_claimed': 'red'}, 'sessionize': {'errorType': 'status_code', 'url': 'https://sessionize.com/{}', 'urlMain': 'https://sessionize.com/', 'username_claimed': 'jason-mayes'}, 'skyrock': {'errorType': 'status_code', 'regexCheck': '^[a-zA-Z0-9@_-]$', 'url': 'https://{}.skyrock.com/', 'urlMain': 'https://skyrock.com/', 'username_claimed': 'red'}, 'social.tchncs.de': {'errorType': 'status_code', 'url': 'https://social.tchncs.de/@{}', 'urlMain': 'https://social.tchncs.de/', 'username_claimed': 'Milan'}, 'spletnik': {'errorType': 'status_code', 'url': 'https://spletnik.ru/user/{}', 'urlMain': 'https://spletnik.ru/', 'username_claimed': 'blue'}, 'svidbook': {'errorType': 'status_code', 'url': 'https://www.svidbook.ru/user/{}', 'urlMain': 'https://www.svidbook.ru/', 'username_claimed': 'green'}, 'toster': {'errorType': 'status_code', 'url': 'https://www.toster.ru/user/{}/answers', 'urlMain': 'https://www.toster.ru/', 'username_claimed': 'adam'}, 'uid': {'errorType': 'status_code', 'url': 'http://uid.me/{}', 'urlMain': 'https://uid.me/', 'username_claimed': 'blue'}, 'Warframe Market': {'errorType': 'status_code', 'url': 'https://warframe.market/profile/{}', 'urlMain': 'https://warframe.market/', 'username_claimed': 'AlexJuli'}, 'wiki.vg': {'errorType': 'status_code', 'url': 'https://wiki.vg/User:{}', 'urlMain': 'https://wiki.vg/', 'username_claimed': 'Auri'}, 'xHamster': {'errorType': 'status_code', 'isNSFW': True, 'url': 'https://xhamster.com/users/{}', 'urlMain': 'https://xhamster.com', 'urlProbe': 'https://xhamster.com/users/{}?old_browser=true', 'username_claimed': 'blue'}, 'znanylekarz.pl': {'errorType': 'status_code', 'url': 'https://www.znanylekarz.pl/{}', 'urlMain': 'https://znanylekarz.pl', 'username_claimed': 'janusz-nowak'}, 'One.lt': {'errorType': 'status_code', 'url': 'https://www.one.lt/{}', 'urlMain': 'https://www.one.lt', 'username_claimed': 'lietuvis'}}"""
    print("getting site data")
    site_data_all = {site.name: site.information for site in sites}
    query_notify = QueryNotifyPrint()
    print("STARTING")
    results = sherlock(
        username=username,
        site_data=site_data_all,
        query_notify=query_notify,
        progress_callback=progress_callback
    )

    found_sites = []
    for site in results:
        if (str(results[site]["status"]) == "Claimed"):
            finding = {
                "name": site,
                "url": results[site]["url_user"]
            }
            found_sites.append(finding)

    print("returning side data")
    return found_sites
