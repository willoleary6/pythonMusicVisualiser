# Set default to first in list or ask Windows
'''
try:
    default_device_index = self.p.get_default_input_device_info()
except IOError:
    default_device_index = -1

# Select Device
print(textcolors.blue + "Available devices:\n" + textcolors.end)
for i in range(0, self.p.get_device_count()):
    info = self.p.get_device_info_by_index(i)
    print(textcolors.green + str(info["index"]) + textcolors.end + ": \t %s \n \t %s \n" % (
    info["name"], self.p.get_host_api_info_by_index(info["hostApi"])["name"]))

    if default_device_index == -1:
        default_device_index = info["index"]

# Handle no devices available
if default_device_index == -1:
    print(textcolors.fail + "No device available. Quitting." + textcolors.end)
    exit()

# Get input or default
device_id = int(input("Choose device [" + textcolors.blue + str(
    default_device_index) + textcolors.end + "]: ") or default_device_index)
print("")

# Get device info
try:
    device_info = self.p.get_device_info_by_index(device_id)
except IOError:
    device_info = self.p.get_device_info_by_index(default_device_index)
    print(textcolors.warning + "Selection not available, using default." + textcolors.end)

# Choose between loopback or standard mode
is_input = device_info["maxInputChannels"] > 0
is_wasapi = (self.p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1
if is_input:
    print(textcolors.blue + "Selection is input using standard mode.\n" + textcolors.end)
else:
    if is_wasapi:
        useloopback = True;
        print(textcolors.green + "Selection is output. Using loopback mode.\n" + textcolors.end)
    else:
        print(
            textcolors.fail + "Selection is input and does not support loopback mode. Quitting.\n" + textcolors.end)
        exit()
'''