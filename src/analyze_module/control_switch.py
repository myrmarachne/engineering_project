import subprocess
import io
import json

class Controller:

    def __init__(self, pathToFile):

        self.switches = {}

        try:
            with open("topo.json") as json_string:
                self.switches = json.load(json_string)
                json_string.close()
        except Exception:
            pass

        pwd = subprocess.run(['pwd'], stdout=subprocess.PIPE)
        path = str(pwd.stdout.decode("utf-8").rstrip())
        self.switchPath = path+"/../../../bmv2/targets/simple_switch/simple_switch_CLI "


    def insert_new(self, command, swID):
        """
        Command should look like <table name> <action name> <match fields> => <action parameters>
        """
        if swID in self.switches.keys():
            path = str(self.switchPath) + " --thrift-port "+str(self.switches[swID][0]) + " --thrift-ip " + str(self.switches[swID][1])
            string = path
            p = subprocess.Popen([string], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

            p.stdin.write(str.encode("table_add " + command))
            p.communicate()[0]

            p.stdin.close()
            p.stdout.close()

    def delete_command(self, command, swID):
        """
        Command should look like <table name> <match fields>
        """
        if swID in self.switches.keys():

            path = str(self.switchPath) + " --thrift-port "+str(self.switches[swID][0]) + " --thrift-ip " + str(self.switches[swID][1])
            string = path

            p = subprocess.Popen([string], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            p.stdin.write(str.encode("table_dump_entry_from_key "+command))

            p.stdin.close()

            ID = -1

            while True:
                line = p.stdout.readline()
                if line != b'':
                    l = line.split()
                    if str.encode("entry") in l:
                        ID = int(l[-1], 0)
                        break
                else:
                    break
            p.stdout.close()

            if ID != -1: # Entry exists in table
                p = subprocess.Popen([string], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

                deleteCommand = "table_delete " + command.split()[0] + " " + str(ID)
                p.stdin.write(str.encode(deleteCommand))

                p.communicate()[0]

                p.stdin.close()
                p.stdout.close()

    def get_tagging_info(self, flow, swID):
        # Change flow to string:
        if swID in self.switches.keys():

            flow_list = flow.split(".")

            flow_string =".".join(flow_list[0:4]) + " " + ".".join(flow_list[4:8])+" "+" ".join(flow_list[8:])

            # Read current frequency
            path = str(self.switchPath) + " --thrift-port "+str(self.switches[swID][0]) + " --thrift-ip " + str(self.switches[swID][1])
            string = path

            p = subprocess.Popen([string], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

            p.stdin.write(str.encode("table_dump_entry_from_key mh_create "+flow_string))
            p.stdin.close()

            freq = -1
            modify = 0

            while True:
                line = p.stdout.readline()
                if line != b'':
                    l = line.split()
                    if str.encode("Action") in l:
                        modify  = int(l[-1])
                        freq = int(l[-2][:-1])
                        break
                else:
                    break

            p.stdout.close()
            return (freq, modify)

    def set_modify(self, flow, swID, newModify):

        if swID in self.switches.keys():

            # Change flow to string:
            flow_list = flow.split(".")
            flow_string =".".join(flow_list[0:4]) + " " + ".".join(flow_list[4:8])+" "+" ".join(flow_list[8:])

            # Read current frequency
            path = str(self.switchPath) + " --thrift-port "+str(self.switches[swID][0]) + " --thrift-ip " + str(self.switches[swID][1])
            string = path
            p = subprocess.Popen([string], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

            p.stdin.write(str.encode("table_dump_entry_from_key mh_create "+flow_string))
            p.stdin.close()

            freq = -1
            modify = 0
            index = 0

            while True:

                line = p.stdout.readline()
                if line != b'':
                    l = line.split()

                    if str.encode("Action") in l:
                        modify  = int(l[-1])
                        freq = int(l[-2][:-1])
                        index = int(l[-3][:-1])
                        break
                else:
                    break

            self.delete_command("mh_create " + flow_string, swID)
            self.insert_new("mh_create set_counters "+flow_string+" => "+str(index)+" "+str(freq)+" "+str(newModify), swID)

    def set_freq(self, flow, swID, newFreq):

        if swID in self.switches.keys():

            # Change flow to string:
            flow_list = flow.split(".")
            flow_string =".".join(flow_list[0:4]) + " " + ".".join(flow_list[4:8])+" "+" ".join(flow_list[8:])

            # Read current frequency
            path = str(self.switchPath) + " --thrift-port "+str(self.switches[swID][0]) + " --thrift-ip " + str(self.switches[swID][1])
            string = path

            p = subprocess.Popen([string], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

            p.stdin.write(str.encode("table_dump_entry_from_key mh_create "+flow_string))
            p.stdin.close()

            freq = -1
            modify = 0
            index = 0

            while True:
                line = p.stdout.readline()
                if line != b'':
                    l = line.split()
                    if str.encode("Action") in l:
                        modify  = int(l[-1])
                        freq = int(l[-2][:-1])
                        index = int(l[-3][:-1])
                        break
                else:
                    break

            p.stdout.close()
            self.delete_command("mh_create " + flow_string, swID)
            self.insert_new("mh_create set_counters "+flow_string+" => "+str(index)+" "+str(newFreq)+" "+str(modify), swID)

    def set_priority(self, flow, swID, newPriority):
        if swID in self.switches.keys():

            # Change flow to string:
            flow_list = flow.split(".")
            flow_string =".".join(flow_list[0:4]) + " " + ".".join(flow_list[4:8])+" "+" ".join(flow_list[8:])

            self.delete_command("priority " + flow_string, swID)
            self.insert_new("priority set_priority "+flow_string+" => "+str(newPriority), swID)

    def prepare(self, list):
        return " --thrift port " + list[0]
