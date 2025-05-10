# Project Instructions

## How to Run the Project

To run the main script, execute the following command:

```bash
python main.py
```

## Running Unit Tests

To run all unit tests located inside the `tests` folder, use this command:

```bash
python -m pytest tests
```

## Running Test Coverage

To measure the test coverage for the `tests` folder, execute this command:

```bash
coverage run -m pytest tests
```

## Viewing Coverage Report

After running the coverage command, open the HTML report by executing:

```bash
start htmlcov/index.html
```

## Checking Scripts

### Check Dirty Patterns

To detect dirty patterns in the data, run the following script:

```bash
python check/check_dirty_patterns.py
```

### Check Data Types

To verify and validate data types, execute this script:

```bash
python check/check_data_type.py
```

## Reference

Google Sheets Data can be accessed at the following link:

[View the Google Sheet](https://docs.google.com/spreadsheets/d/19vweQTnSLL-9Qy52-YH0OZOJlevBm0uBqRRSpRS8dl8/edit?gid=0#gid=0)

---

**Note :** In this project, I have tried to follow PEP8 guidelines to ensure that the code is clean, consistent, and easy to read.
