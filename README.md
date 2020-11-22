[![GitHub issues](https://img.shields.io/github/issues/RealKevinApetrei/MySeea)](https://github.com/RealKevinApetrei/MySeea/issues) 
[![GitHub forks](https://img.shields.io/github/forks/RealKevinApetrei/MySeea)](https://github.com/RealKevinApetrei/MySeea/network)
[![GitHub stars](https://img.shields.io/github/stars/RealKevinApetrei/MySeea)](https://github.com/RealKevinApetrei/MySeea/stargazers)
[![GitHub license](https://img.shields.io/github/license/RealKevinApetrei/MySeea)](https://github.com/RealKevinApetrei/MySeea/blob/master/LICENSE)

# Table of Contents
- [About the Project](#about-the-project)
  - [Information](#information)
  - [Features](#features)
  - [Built With](#built-with)
  - [Connection Types](#connection-types)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage and Controls](#usage-and-controls)
  - [How to connect with mysql.connector?](#how-to-connect-with-mysqlconnector)
  - [Roadmap](#roadmap)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)
  - [Acknowledgements and Credits](#acknowledgements-and-credits)

# About the Project
## Information
![MySeeaShowcase](https://user-images.githubusercontent.com/65184258/99902135-531b5380-2cb3-11eb-860a-921eaa8f1479.PNG)


This project is a MySQL Database Viewer. It features **table reading** and a **functional feel**.
This is probably my biggest project I have done as of *22 November 2020*.

MySeea allows you to connect to a web-based MySQL Database and view it's tables.

**INFO: All data is stored locally. This means that no information will be stored externally or outsourced to anybody but you.**
**DISCLAIMER: This program may not work on Linux or MacOS as those versions have not been released yet!**

## Features
Here are some of the features of the project:

- Connect/Disconnect to MySQL Database
- Read Tables
- Keybinds and Shortcuts
- Clean Look
- Interactive Help Menu

## Built With
This project was made with:

- Made in Python3.8.6
- Tkinter

## Connection Types
These are the currently available connection types:

- **mysql.connector**

# Getting Started
Requirements and details on how to get the program running

# Prerequisites
Requirements:

- Python3.6+\
  **Download Python3.8.6: `https://www.python.org/downloads/release/python-386/`**
- pip3
- Tkinter\
  **For Python3: `pip3 install tkinter`**\
- Sqlite3\
  **For Python3: `pip3 install sqlite3`**\
- mysql.connector (*Connection Type*)\
  **For Python3: `pip3 install mysql.connector`**\
  
Other Requirements:

- Tkinter.font (Preinstlled with Tkinter)

# Installation
**INFO: Windows 10 executable downloadable from [here](https://github.com/RealKevinApetrei/MySeea/releases) or [here](https://github.com/RealKevinApetrei/MySeea/tree/main/Windows%2010%20(Executable))**

1. Make sure you have correctly completed the [Prerequisites](#prerequisites).
2. Clone the repository\
   **`git clone https://github.com/RealKevinApetrei/MySeea/`**

# Usage and Controls
Information on how to use the program.

**Usage and Control Information is on the `Help` menu on the application.**

## How to connect with mysql.connector?

1. Go to `Settings`
2. Fill in database login details
3. Choose connection type under `Advanced Settings` as `mysql.connector`
4. Add `allowed tables` under `Security Settings` that you want to view in the future
5. Save settings
6. Go to `Main Menu` and `Connect to Database` under `Connection` menu
(To view a table, go to `View` menu and choose an allowed table to view)

## Roadmap

See the [open issues](https://github.com/RealKevinApetrei/MySeea/issues) for a list of proposed features (and known issues).

I am happy to add more features upon request and I will be working on more features in time. The Help Menu is not fully developed, please contact me if you would like me to add anything urgently.

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the **MIT License**. See `LICENSE` for more information.

## Contact

Kevin Apetrei - [@KevinApetrei](https://twitter.com/KevinApetrei) - realkevinapetrei@gmail.com\
Project Link: https://github.com/RealKevinApetrei/MySeea/

## Acknowledgements and Credits
- All rights reserved
