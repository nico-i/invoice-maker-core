# Invoice-Maker Core

The Invoice Maker is program dedicated to extracting work-time through
the Google Calendar API and export a dynamically filled .pdf-invoice with
the help of Beautiful Soup 4 and WeasyPrint.

## First Steps

To ensure a rather plug & play start into development, there are a few things that need setting up first.

### Python & Pip

Because the majority of this project is based on [Python 3.9](https://www.python.org/downloads/), you will need to install it. [Pip](https://pip.pypa.io/en/stable/installation/) should also be installed to proceed with the upcoming steps.

### WeasyPrint & Beautiful Soup 4

This software uses two modules to enable the editing and parsing of HTML files, these modules are [WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) and [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup).

As soon as **pip** is installed, the installation of the aforementioned modules can be done rather easily by using the following command:

```python
pip install weasyprint beautifulsoup4
```

### Google API

The last piece of the puzzle is the [Google Calendar API](https://developers.google.com/calendar/api). The best way to install it, is by following the [Python Quick-Start Guide](https://developers.google.com/calendar/api/quickstart/python). This guide gives a basic understanding on how the API works aside from just installing necessary modules. The acquired knowledge could be useful when extending this software's code later on. You will also need to **generate a credentials.json** to enable the Google API and place it into the root folder.

## Running the Invoice-Maker

After setting up, you are almost ready to start your first test print. There is just one more thing that needs configuring, namely the **CAL_ID field** in the [config.txt](./resource/mock/config.txt). Because unless you are subscribed to the [Holidays in Germany](https://calendar.google.com/calendar/embed?src=en.german%23holiday%40group.v.calendar.google.com&ctz=Europe%2FBerlin) calendar, the mock-data will throw an exception. You need to change this value to a calendar-id that is connected to your google account. You can achieve this by either running the [python-script](./src/all_calendars.py) with:

```shell
/usr/local/bin/python3 ./src/all_calendars.py
```

and extracting an id from the console or just follow [this guide by Google](https://developers.google.com/calendar/api/v3/reference/calendarList/list#try-it).

You can then execute the invoice_maker.py script for the first time by using this command!

```shell
/usr/local/bin/python3 ./src/invoice_maker.py
```

### First Execute

When running invoice_maker.py for the first time a login prompt to your google account will open and require you to login. This is necessary so that the script is allowed to access the event data of the calendar that you specified.

### Preliminary Invoice Run

There are two ways of running the invoice_maker. The first one is called the **Preliminary Invoice Run** or **PIR** and the second one is called the **Actual Invoice Run** or **AIR** for short. The difference is that an AIR will update the **OVERTIME_PREV** field in your config.txt. A PIR can be done to just get an overview of how many hours you have worked and what your payout is currently, it is done by a simple execute as seen above and shown again here:

```shell
/usr/local/bin/python3 ./src/invoice_maker.py
```

### Actual Invoice Run

As mentioned before, an AIR will update your config.txt and should therefore be executed with caution and only on the day the invoice needs to be sent, to avoid errors in coming invoices. It can be run with an extra parameter as follows:

```shell
/usr/local/bin/python3 ./src/invoice_maker.py 1
```

## Configuring the Invoice-Maker

To be able to create invoices that do not use mockup data, a modification of the config-files is needed. These can be found under the following paths:

```text
invoice-maker-core/resource/data
```

Should the values of the config-files be empty, mockup-data is used to enable debugging. This data's path is as follows and can be used as a reference when configuring one's own Invoice-Maker:

```text
invoice-maker-core/resource/mock
```

### The Config-File

The **config.txt** contains a number of key-value-pairs that can be modified. What these pairs actually do is explained in the following list.

- **OUTPUT_PDF_PATH**
  - Sets the path and name of the end-result, which is printed after a program execution.
- **PAYDAY**
  - Sets the date of the Month when the invoice is do.
  - *NOTE: The maximal value should be 27, when leap years are a concern!*
- **CAL_ID**
  - The id of the google calendar that is to be searched for events.
- **MAX_LOAN**
  - The maximal loan one is allowed to get paid in one month's time.
  - Set to 0 if there is none.
- **HOURLY_RATE**
  - The hourly rate one gets paid.
- **OVERTIME_PREV_MONTH**
  - The overtime of the previous month.
  - Set to 0 if there is none.
