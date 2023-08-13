# SF2DB Project

A python utility to fetch data from Salesforce and store the information in a relational database of choice.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Developer Notes](#dev-notes)
- [Future Developments](#future-dev)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The program facilitates its functionality by allowing the user to configure most aspects, especially mapping between Salesforce objects and target relational database.  

The program one Salesforce objects with a database table. E.g. `Accounts` Salesforce object can be mapped against `User` database table. 

The program is limited in its ability to establish a relationship between multiple Salesforce objects and transform them into one a single relational table.  
## Installation  

Clone the repo ensure and all files & sub-folders in `config` and `src` are present  

All configuration files in `config` folder must be setup prior to running the program.  
Refer to [Examples section](#examples) for the purpose of these configuration files

## Usage
The program can to be used in part of 3rd party codebase or as a standalone utility in a batch process  

Examples of batch process  

1. **Scheduling with Cron (Unix-like systems)**  

    Edit cron  
        ```sh
        crontab -e
        ```  

    Add the following line to run the script every day at 2:00 AM:  
        ```sh
        0 2 * * * /path/to/python3 /path/to/src/main.py
        ```  

2. **Scheduling with a Batch File (Windows)**  

    Create a batch file (e.g., run_script.bat) using a text editor, and add the following line:  

    ```powershell 
    C:\path\to\python.exe C:\path\to\src\main.py
    ```  

    Replace `C:\path\to\python.exe` with the actual path to your Python interpreter and `C:\path\to\src\main.py` with the actual path to your script.  

## Developer Notes  

__Application entry__  
`src.main.py` which calls `src.sf2db.app.app.py`  

__Salesforce API__  
[`simple-salesforce`](https://pypi.org/project/simple-salesforce/) is the primary Adapter used to login and query Salesforce.
The primary adapter can be change to another package or custom implementation so long as it is adheres to the contract of `src.sf2db.salesforce.SFInterface` Protocol class  

__Folder organisation__  
- `/config` : all user driven configrations  
- `/src` : source code  
    - `/src/app` : integration point
    - `/src/db` : target database concerns
    - `/src/salesforce` : concerned with interacting with salesforce site
    - `/src/mapping` : mapping between salesforce objects and database tables
    - `/src/util` : utility functions used by other modules
  


- `/test/` : unit tests *not implemented yet  
## Future developments

- [x] Logging 
- [ ] Unit testing
- [ ] Success / Failutre notification to various targets
- [ ] Utility to verify configurations
- [ ] Decoupling of SQL Alchemy as ORM package via Abstraction/Interfaces

## Examples

Note that all configuration items are case sensitive  

__`db_config.yaml`__

    Defines the connection string to the target database  
    Sample file is `config/examples/db_config.json`  

    Program accesses this file using `src/sf2db/app/config.py`s `ConfigFiles.DB_URI`  

__`db_tables.json`__  

    Defines the relational DB structure  
    Sample file is `config/examples/db_tables.json`  

    Program accesses this file using `src/sf2db/app/config.py`s `ConfigFiles.DB_TABLES`  
 
    Columns only support `name`, `type`, and `primary_key` as json attributes  
    `type` is one of [SQLAlchemy Types](https://docs.sqlalchemy.org/en/20/core/types.html)  
    Permitted types are in `src/sf2db/db/model_factory.py`'s `ALLOWED_SQLALCHEMY_TYPES`  

__`salesforce_to_db.json`__  

    Maps Salesforce objects with relational database tables defined in `db_tables.json`  
    Sample file is `config/examples/db_tables.json`.   

    Program accesses this file using `src/sf2db/app/config.py`s `ConfigFiles.SF2DB_MAPPINGS`  

__`salesforce_credentatials.yaml`__  

    Maps Salesforce objects with relational database tables defined in `db_tables.json`  
    Sample file is `config/examples/salesforce_credentatials.yaml`.   
    Production file _must be renamed_ to `salesforce_credentatials.yaml`  

    Program accesses this file using `src/sf2db/app/config.py`s `ConfigFiles.SALESFORCE_CREDENTIALS`  

## Contributing

 You can contribute in various ways, including reporting issues, suggesting improvements, and submitting pull requests.

### Reporting Issues

If you find a bug or have a feature request, please open an issue on our [GitHub repository](https://github.com/neotechmonk/cmcs/issues). Provide as much detail as possible so that the issue can be undertood and reproduced  

### Suggesting Enhancements

If you have a suggestion for an enhancement, an issue on  [GitHub repository](https://github.com/neotechmonk/cmcs/issues) and label it as an "enhancement."  

### Pull Requests

We welcome pull requests from the community! If you'd like to contribute code to the project, follow these steps:  

1. Fork the repository on GitHub.
2. Create a new branch from the `main` branch: `git checkout -b your-feature-branch`
3. Make your changes, following the project's coding guidelines.
4. Test your changes thoroughly.
5. Commit your changes: `git commit -m "Add your descriptive commit message"`
6. Push your branch to your fork: `git push origin your-feature-branch`
7. Open a pull request against the `main` branch of the original repository.

Will review your pull request and provide feedback. Once your changes are approved, they will be merged into the main project.  

### Coding Guidelines

- Follow the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/) for Python code.  
- Keep your code clean and well-documented.  
- Write meaningful commit messages that explain your changes.  

## Licensing

SF2DB is open-source software released under the [MIT License](https://choosealicense.com/licenses/mit/).
You can find the full text of the MIT License in the [LICENSE](LICENSE.txt) file.

