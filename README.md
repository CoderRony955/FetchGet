<p align="center">
  <img src="imgs\fetchget_banner.png">
</p>


# FetchGet 1.1

FectchGet is a multi-component system utility and networking tool designed to streamline monitoring and interaction with local systems and networks. It combines the power of the command line with two versions of intelligent **Discord bots** **FetchGet B** and **FetchGet Y** to provide flexible ways to perform network tasks. This tool is built to assist users in gathering vital system information, performing routine networking operations, and executing remote commands via Discord, making it ideal for sysadmins, power users, or anyone managing distributed systems.



## Key Features:

### **Command-Line Interface (CLI)**: A fast and intuitive CLI to execute system utility functions and network commands directly from the terminal.

<p align="center">
  <img src="screenshots\cli_view.png">
</p>

- Interact with system utilities
- Execute network commands
- Gather system information
- Make HTTP requests
- Perform Lookups
- Test URLs if they are malicious or not
- Check abuseive IPs
- Perform userlookup on over 20+ social networks
- Gather IPs information and more...
  
For check about new features and updates, [See Changelog here](./CHANGELOG.md).


### **Dual Discord Bots (version B & Version Y)**: Two versions of Discord bots integrated with the FetchGet tool to interact with the network. Each bot offers different features or interfaces for improved accessibility and testing.

### **FetchGet B1.0**:
<p align="left">
  <img src="screenshots\fetchget_bot_v_b.png" width="400" height="auto">
</p>

This version of bot is allow users to make **HTTP requests** by using any method such as GET, POST, PUT, DELETE. 

<blockquote style="border-left: 4px solid orange; padding: 0.5em; background: #fff8dc;">
  <strong>⚠️ Warning:</strong> Making HTTP requests illegal are not allowed, this is against the TOS of Discord.
</blockquote>

FetchGet B.10 bot has less features as compare to FetchGet Y1.0 because, B version specially developed for whole community members, every server members can access this bot just like a normal bots. And the reason is to adding less features in this version is to, for some reasons another features such as gathering someones IPs information and performing such other tasks publicy is not consider in public.

### **FetchGet Y1.1**:
<p align="left">
  <img src="imgs\fetchget_bot_y_v.png" width="100" height="auto">
</p>

**FetchGet Y1.1** bot especially designed for those peoples who mostly active on Discord such as a networking person who moslty active on Discord. And this bot only for private and personal use only because some features are of this bot are not consider to used public channels. So that's why this bot only for private use only.

**Commands and Features:**

- **HTTP Request**: Allows users to make HTTP requests using any method such as GET, POST, PUT, DELETE.
- **IP Lookup**: Looks up the IP address of a domain or IP address.
- **Malicious URL Check**: Checks if a given URL is malicious or not.
- **DNS Lookup**: Looks up the DNS records for a domain.
- **Abusive IP Check**: Checks if an IP address is considered abusive or not.
- **Whois Lookup**: Looks up the WHOIS information for a domain.

For check about new features and updates, [See Changelog here](./CHANGELOG.md).
<blockquote style="border-left: 4px solid orange; padding: 0.5em; background: #fff8dc;">
  <strong>⚠️ Warning:</strong> FetchGet Y1.1 is only for private use. Do not use it in public channels and also do not use it for illegal purposes.
</blockquote>


## Command Line Installation:

### Prerequisites:
- [Python3](https://www.python.org/)
- [Cython](https://cython.org/)
- [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- [Discord.py](https://discordpy.readthedocs.io/en/latest/index.html)
- [uv](https://docs.astral.sh/uv/) or [pip](https://pypi.org/project/pip/)
- [vt (VirusTotal API for Python) ](https://virustotal.github.io/vt-py/)
- [AbuseIPDB API](https://docs.abuseipdb.com/#introduction)


### Windows:
1. Clone this repository to your local machine.
2. Open a terminal or command prompt and navigate to the cloned directory.
3. Run the following command to make virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    ```bash
    .\venv\Scripts\activate
    ```
5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Then navigate to `cli` directory and run:
  ```bash
  python setup.py build_ext --inplace
  ```
7. Now run command to use command-line locally:
  ```bash
  python fetchget.py -h
  ```


### Linux:
1. Clone this repository to your local machine.
2. Open a terminal or command prompt and navigate to the cloned directory.
3. Run the following command to make virtual environment:
    ```bash
    python3 -m venv venv
    ```
4. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Then navigate to `cli` directory and run:
  ```bash
  python3 setup.py build_ext --inplace
  ```
7. Now run command to use command-line locally:
  ```bash
  python3 fetchget.py -h
  ```


### MacOS:
1. Clone this repository to your local machine.
2. Open a terminal or command prompt and navigate to the cloned directory.
3. Run the following command to make virtual environment:
    ```bash
    python3 -m venv venv
    ```
4. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Then navigate to `cli` directory and run:
  ```bash
  python3 setup.py build_ext --inplace
  ```
7. Now run command to use command-line locally:
  ```bash
  python3 fetchget.py -h
  ```

## Discord Bots setup (add FetchGet capabilities in your bot):
Firstly go to [discord developer portal](https://discord.com/developers/applications) and create a new application and copy the bot token.

1. Clone this repository to your local machine.
2. Open a terminal or command prompt and navigate to the cloned directory.
3. Run the following command to make virtual environment:
    ```bash
    python3 -m venv venv
    ```
4. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Go to `.env` file to add your bot token as per your choice and `vt` and `AbuseIPDB` api key:
<p align="center">
  <img src="imgs\env.png" width="400" height="auto">
</p>

7. Then navigate to `discord-bot` and then your preferred bot version directory `cd yellow_v`:
8. Run the following command to run bot locally:
    ```bash
    python yellow_v.py
    ```
Now see bot logs in `logs` directory and you will see bot is running now.
  
**Wohooo! All Done! now FetchGet capablities are ready to use.** 🔥


## Contribution:
Contributers are welcome and appreciated! To contribute:

1. Fork this repository.
2. Clone your fork:
3. Create a new branch for your feature or fix:
4. Make your changes and commit them with clear messages.

Push to your fork and open a Pull Request.


## Acknowledgment

This tool is still evolving, and there's much more to come. In the future, it will be available via popular package managers and packed with even more commands and features to make your experience even better. And for latest updates, keep eye on [Changelog](./CHANGELOG.md).

Stay tuned, and feel free to contribute or suggest improvements — your input helps shape the future of this project.


## License
This project is licensed under the [MIT License](https://mit-license.org/). Feel free to use, modify, and distribute it under the terms of the license.



 