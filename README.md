# Flight Data Services - Technical Test

## Brief
This task is a typical example of the problems we solve at Flight Data Services. We have solved this particular problem many times using different languages and technologies. The task should be completed using Python and any freely available libraries that the candidate might find useful.

Write a program that accepts a decimal longitude and latitude location as input and displays the nearest airport, from the data file provided, as output. It is up to the candidate to decide how the input is captured and how the output is displayed.

## Requirements
In order to run the test app you will require the following:

* Python 3.6.

## Getting Started
Before running the test application, you will need to make sure you install the following required Python libraries:
- Numpy - for trigonometric functions
- PySimpleGui - to provide a simple GUI for running the test app

The simplest way to install these libraries is via `pip install`:
```
$ pip install -r requirements.txt
```

## Launching the Test App
```
$ python ./fds_test_nick.py
```

You will be presented with a simple interface with two input fields, allowing you to enter a latitude and longitude. It is expected the inputs for latitude and longitude are floats.

Once your required values are entered, simply click the `Submit` button. The app will then calculate the distance between the location you entered and the location of every airport within its data.

You will then be presented with a modal dialog showing you the closest airport and calculated distance from your entered location.
