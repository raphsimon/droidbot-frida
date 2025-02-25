import logging
from subprocess import Popen, PIPE

from droidbot.adapter.adapter import Adapter

class FridaTraceException(Exception):
    """
    Exception from frida-trace
    """
    pass

class FridaTrace(Adapter):
    """
    Class to set the frida command to execute.
    """
    def __init__(self, device=None , package_name=None, target_functions=None, output_path=None):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.device = device

        self.target_app = package_name
        self.target_functions = target_functions
        self.output = output_path
        self.command = []
        self.process = None

        self.ready = False  # We are ready to execute commands when frida-server is running
                            # on the device


    def build_command(self):
        if self.target_app and self.target_functions:
            self.command = ["frida-trace", "-U", "-O", self.target_functions,
                            "-f", self.target_app,
                            "-o", self.output + f"frida_trace_{self.target_app}.txt"]
        else:
            if not self.target_app:
                self.logger.error("Package name is missing for frida-trace")
            if not self.target_functions:
                self.logger.error("No trace arguments provided")


    def start_tracing(self):
        self.build_command()
        if self.command and self.ready:
            self.logger.info(f'Running frida-trace command: {self.command}')
            self.process = Popen(self.command)
        else:
            if not self.command:
                self.logger.error("Command is not set")
            else:
                self.logger.error("frida-server is not running on the device")


    def check_connectivity(self):
        # Here we can se whether or not frida-server is running on the device
        self.ready = self.device.check_frida_server_state()
        return self.ready


    def disconnect(self):
        if self.process:
            self.process.kill()


    def set_app_to_trace(self, package_name):
        self.target_app = package_name