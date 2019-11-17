# nitka
## Wikipedia API extractor
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fa153606e6284a658ed05a1573a0f658)](https://www.codacy.com/manual/antonkurenkov/nitka?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=antonkurenkov/nitka&amp;utm_campaign=Badge_Grade)

This is a [Flask][flask] app for searching in [Wikipedia][wiki].

## Description

It looks as a simple web page with a textbox and a “search” button.
Hitting “search” searches a term (or phrase) in Wikipedia using its API.

-   If the result is found it displays a short description and an image (optionally).
-   If multiple results found, shows “It may refer to:” and list of links. Links are clickable and search more precise term.
-   Else, it shows “term not found”.

## Setup

The app is written in Python 3.7.4, so you need a proper version be installed.
It depends on following libs, so you also need:

-   `flask`
-   `requests`
-   `re`

## Run

Just hit the `run.py` file in the main folder for the Flask server to start.
The application could be accessed on `http://localhost:5000`.

## Usage

Input the term or phrase into the textbox and hit the "Search" button.

The app connects to Wikipedia API and returns a simple web page containing data depending on response type.

If the ID for the response page is `'-1'`, there is no results for the requested phrase.
An empty page be returned.

If the response page has embedded key `'disambiguation'`, the list of referred titles be returned.
Being clicked it returns a rendered page depends on type of API response (recursively).
A page containing a list of related clickable titles be returned.

If the response page has a proper ID and it is not a 'disambiguation' page, treats the page like an article.
In this case the article description and image be extracted if it is possible.
In case of description absence the first summary sentence be used instead.
A page containing an image (optionally) and a short description be returned.

[flask]: https://github.com/pallets/flask
[wiki]: https://wikipedia.org