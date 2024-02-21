from time import sleep
from colorama import Fore, init

init(autoreset=True)

class Incresp():
    def __init__(self):
        self.__str__()
        self.RESPONSE = ""
        self.Run()

    def __str__(self):
        print(Fore.LIGHTYELLOW_EX + """
         _nnnn_                      
        dGGGGMMb     ,''''''''''''''''''''''''';
       @p~qp~~qMb    | Linux Incident Response! |
       M|@||@) M|   _;.........................;
       @,----.JM| -' 
      JS^\__/  qKL
     dZP        qKRb
    dZP          qKKb
   fZP            SMMb
   HZM            MMMM
   FqM            MMMM
 __| ".        |\dS"qML
 |    `.       | `' \Zq
_)      \.___.,|     .'
\____   )MMMMMM|   .'
     `-'       `--' Author: By emrekybs 
     		    https://github.com/emrekybs    
        """)

    def Run(self):
        sleep(2)
        report_saved = False
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Incident Response Report</title>
        </head>
        <body>
            <!-- Linux Computer Incident Response Reporting Form -->
            <h1>Linux Computer Incident Reporting Form</h1>
            <form action="/submit-incident" method="post">
                <label for="isDrill">Is this a drill?</label>
                <select id="isDrill" name="isDrill">
                    <option value="yes">Yes</option>
                    <option value="no" selected>No</option>
                </select>
                
                <!-- General Incident Information -->
                <fieldset>
                    <legend>General Incident Information</legend>
                    <label for="date">Date:</label>
                    <input type="date" id="date" name="date" required>
                    
                    <label for="time">Time:</label>
                    <input type="time" id="time" name="time" required>
                    
                    <label for="timezone">Time Zone:</label>
                    <input type="text" id="timezone" name="timezone" required>
                    
                    <label for="incidentHandlerName">Incident Handler Name:</label>
                    <input type="text" id="incidentHandlerName" name="incidentHandlerName" required>
                    
                    <label for="incidentHandlerPhone">Incident Handler Phone:</label>
                    <input type="tel" id="incidentHandlerPhone" name="incidentHandlerPhone" required>
                    
                    <label for="incidentHandlerEmail">Incident Handler Email:</label>
                    <input type="email" id="incidentHandlerEmail" name="incidentHandlerEmail" required>
                </fieldset>
                
                <!-- Initial Detection -->
                <fieldset>
                    <legend>Initial Detection</legend>
                    <label for="typeOfIncident">Type of Incident:</label>
                    <input type="text" id="typeOfIncident" name="typeOfIncident" required>
                    
                    <label for="detectionDateTime">Date, time, and time zone of first detection:</label>
                    <input type="text" id="detectionDateTime" name="detectionDateTime" required>
                    
                    <label for="involvedPersons">List names and contact information for all persons involved in detection and initial investigation:</label>
                    <textarea id="involvedPersons" name="involvedPersons" rows="4" required></textarea>
                    
                    <label for="incidentDetectionMethod">How was incident detected?</label>
                    <input type="text" id="incidentDetectionMethod" name="incidentDetectionMethod" required>
                    
                    <label for="incidentDescription">What do you think happened?</label>
                    <textarea id="incidentDescription" name="incidentDescription" rows="4" required></textarea>
                    
                    <label for="systemsInvolved">List of systems involved:</label>
                    <textarea id="systemsInvolved" name="systemsInvolved" rows="4" required></textarea>
                </fieldset>
            </form>
            <!-- End of the Linux Computer Incident Reporting Form -->

            <!-- Existing template for command execution results -->
            <table border="1">
                <tr>
                    <th style="font-size: 18px;">Checked</th>
                    <th>INCIDENT RESPONSE RESULT</th>
                </tr>
                {}
            </table>
        </body>
        </html>
        """

      
        html_content = ""

        commands = [
            ("ifconfig && ip a", "Network Interfaces and IP Addresses."),
            ("arp -a", "ARP Table."),
            ("hostname", "Display the system's hostname."),
            ("uname -a", "Display system information including the kernel version."),
            ("df -h", "Display disk usage."),
            ("free -m", "Display memory usage."),
            ("ps aux", "Display running processes."),
            ("top -n 1 -o %CPU", "Display real-time system statistics."),
            ("cat /etc/passwd", "User Accounts."),
            ("cat /etc/shadow", "Password Information."),
            ("cat /etc/group", "Information about user groups."),
            ("cat /etc/sudoers", "sudoers file content."),
            ("lastlog", "Last Login Information."),
            ("tail /var/log/auth.log", "Authentication logs."),
            ("tail /var/log/syslog.log", "System logs."),
            ("tail /var/log/demon.log", "Demon logs."),
            ("tail /var/log/apache/access.log", "Apache Access Logs."),
            ("tail /var/log/nginx/access.log", "Nginx Access Logs."),
            ("tail /var/log/mysqld.log", "MySQL Server Logs."),
            ("ps -aux", "Detailed Process Information."),
            ("uptime", "System Uptime."),
            ("cat /proc/meminfo", "Memory Information."),
            ("ps aux", "Currently Running Processes."),
            ("last -f /var/log/wtmp", "Login History."),
            ("cat /etc/resolv.conf", "DNS Resolver Configuration."),
            ("cat /etc/hosts", "Display Hosts File Content."),
            ("ls -alR /proc/*/cwd", "List current working directories of processes."),
            ("iptables -L -v -n", "Display Firewall Rules."),
            ("service --status-all", "List All Available Services."),
            ("find / -type f -size +512k -exec ls -lh {{}};", "Find and list large files on the system."),
            ("netstat -punta", "Network Statistics."),
            ("echo $PATH", "Display the system's PATH environment variable.")
        ]

        try:
            for command, description in commands:
                print(Fore.LIGHTGREEN_EX + description)
                output = self.execute_command(command)

                html_content += f"<tr><td><div style='font-size: 18px;'>{description}</div></td><td><pre>{output}</pre></td></tr>"

                self.RESPONSE += f"{command}:\n{output}"
        except Exception as e:
            print(e)
        finally:
            report_saved = self.save_report(html_template, html_content)

        if report_saved:
            print("Report saved.")

    def execute_command(self, command):
        import subprocess
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            return output
        except subprocess.CalledProcessError as e:
            return e.output

    def save_report(self, html_template, html_content):
        try:
            with open("report.html", "w") as html_file:
                html_output = html_template.format(html_content)
                html_file.write(html_output)
            return True
        except Exception as e:
            print("Error occurred while saving report:", e)
            return False

incresp = Incresp()
