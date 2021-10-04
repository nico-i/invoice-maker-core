# Invoice-Maker Core

The Invoice Maker is program dedicated to extracting work-time through
the Google Calendar API and export a dynamically filled .pdf-invoice with
the help of Beautiful Soup 4 and WeasyPrint.

## First Steps

To ensure a rather plug & play start into development, there are a few things that need setting up first.

### Python & Pip

Because the majority of this project is based on [Python 3.9](https://www.python.org/downloads/), you will need to install it as well as [pip](https://pip.pypa.io/en/stable/installation/) to proceed with the next steps.

### WeasyPrint & Beautiful Soup 4

In addition to Python, this software uses two modules to enable the editing and parsing of HTML files, these modules are [WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) and [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup).

As soon as **pip** is installed, the installation of the aforementioned modules can be done rather easily, mainly by using the following command:

```python
pip install weasyprint beautifulsoup4
```

### Google API

The last piece of the puzzle is [Google Calendar API](https://developers.google.com/calendar/api). The best way to install it, is by following the [Python Quick-Start Guide](https://developers.google.com/calendar/api/quickstart/python). This gives a basic understanding on how the API works aside from just installing necessary modules, which could be useful when extending this softwares code.
