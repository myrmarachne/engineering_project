#!/usr/bin/env python
import getpass
import argparse
import pika
import sys
import json
import logging
import threading
import os
import re
import time
from control_switch import Controller
import MySQLdb
import pandas as pd

class DataBaseConnector:

    def __init__(self, host="localhost", port=3306, db="testdb"):

        self.host = host
        self.port = port
        self.db = db

        # Prompt for login and password

        print("Provide database connection credentials")
        self.user = input("Username [%s]: " % getpass.getuser())
        if not self.user:
            self.user = getpass.getuser()

        self.passwd = getpass.getpass("Password : " )

        try:
            conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd)
            conn.close()

        except MySQLdb.Error as error:
            print("The connection was down, following error occurred: %s", error)
            sys.exit(1)


    def add_to_db(self, flow, alert, warning):

        # Check if already exists in database
        self.del_from_db(flow)

        try:
            mysql_cn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db)
            c = mysql_cn.cursor()
            addstmt = "INSERT INTO SLA (flow, delay_warning, delay_alert) VALUES(%s, %s, %s)"
            c.execute(addstmt, (flow, warning, alert,))
            mysql_cn.commit()
            mysql_cn.close()

        except (MySQLdb.Error, MySQLdb.Warning, pd.io.sql.DatabaseError) as e:
            print(e)
            return None

        pass

    def del_from_db(self, flow):

        # Delete from database
        try:
            mysql_cn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db)
            c = mysql_cn.cursor()
            delstatmt = "DELETE FROM SLA WHERE flow = %s"
            c.execute(delstatmt, (flow,))
            mysql_cn.commit()
            mysql_cn.close()

        except (MySQLdb.Error, MySQLdb.Warning, pd.io.sql.DatabaseError) as e:
            print(e)
            return None


    def db_prepare(self):

        try:
            mysql_cn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd)
            query = "CREATE DATABASE " + self.db;
            c = mysql_cn.cursor()
            c.execute(query)
            mysql_cn.close()

        except (MySQLdb.Error, MySQLdb.Warning, pd.io.sql.DatabaseError) as e:
            print(e)

        create_query = "CREATE TABLE IF NOT EXISTS SLA\
        (flow CHAR(50) PRIMARY KEY,\
        delay_warning BIGINT,\
        delay_alert BIGINT)"

        self.run(query=create_query)

    def run(self, query=""):
        try:
            mysql_cn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db)
            c = mysql_cn.cursor()
            c.execute(query)
            mysql_cn.close()

        except (MySQLdb.Error, MySQLdb.Warning, pd.io.sql.DatabaseError) as e:
            print(e)
            return None


    def db_pull(self):

        def get_data(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, query=""):
            try:
                mysql_cn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db)
                df_mysql = pd.read_sql(query, con=mysql_cn)
                mysql_cn.close()

                return df_mysql

            except (MySQLdb.Error, MySQLdb.Warning, pd.io.sql.DatabaseError) as e:
                print(e)
                return None


        create_query = "SELECT * FROM SLA"
        return get_data(query=create_query)
        #for i in range (0, sla_data.shape[0]):



class Server:

    def __init__(self, host="10.0.2.15", port=5672, login="guest", password="guest", db="testdb"):

        parser = argparse.ArgumentParser()

        parser.add_argument("--db", action="store", dest="db", help="Provide the database name")
        parser.add_argument("--dbhost", action="store", dest="dbhost", \
                            help="Provide the database hostname (or IP address)")
        parser.add_argument("--dbport", action="store", dest="dbport", type=int, \
                            help="Provide the database connection port")

        parser.add_argument("--server", action="store", dest="host", \
                            help="Provide the hostname (or IP address) of the broker server")
        parser.add_argument("--port", action="store", dest="port", type=int, \
                            help="Provide the broker connection port")
        parser.add_argument("--topo", action="store", dest="topo", \
                            help="Provide the path to JSON file with Topology")

        args = parser.parse_args()

        host = args.host
        port = int(args.port)

        dbhost = args.dbhost
        dbport = args.dbport
        db = args.db
        pathToTopoFile = args.topo

        # Prompt for login and password
        print("Provide login and password for broker connection")

        login = input("Username [%s]: " % getpass.getuser())
        if not login:
            login = getpass.getuser()

        self.connection = None


        while True:
            try:
                password = getpass.getpass("Password : " )

                self.credentials = pika.PlainCredentials(login, password)
                self.params = pika.connection.ConnectionParameters(host, port, "/", self.credentials)
                print("Connected to server")
                break
            except Exception:
                print("The password you entered is incorrect.")

        self.channel = None
        self.exchange = "topic_logs3"
        self.type = "topic"
        self.sla_checkers = []
        self.sla = {}
        self.measurements = {}
        self.switch =  Controller(pathToTopoFile)
        self.priorFlows = []

        self.dataBaseConnector = DataBaseConnector(host=dbhost, port=dbport, db=db)
        self.dataBaseConnector.db_prepare()
        self.pull_from_db()


    def connect(self):
        try:
            if not self.connection or self.connection.is_closed:
                self.connection = pika.BlockingConnection(self.params)
                self.channel = self.connection.channel()
                self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.type)
        except Exception as error:
            logging.debug("The connection was down, following error occurred: %s", error)

    def add_sla_flow(self, routing_key, msg):
        try:
            self.publish(str(routing_key), json.dumps(msg).encode())
        except Exception as error:
            logging.debug("The connection was down, following error occurred: %s", error)
            print(error)

    def publish(self, routingkey, msg):
        try:
            self.channel.basic_publish(exchange=self.exchange, routing_key=routingkey, body=msg)
            print("Message", msg," sent to  ",routingkey)
        except Exception as error:
            logging.debug("The connection was down, following error occurred: %s", error)
            print(error)

    def close(self):
        if self.connection and self.connection.is_open:
            logging.debug("The connection is being closed.")
            self.connection.close()

    def callback(self, ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))

    def pull_from_db(self):
        sla_data = self.dataBaseConnector.db_pull()
        for i in range (0, sla_data.shape[0]):
            self.sla[sla_data["flow"].iloc[i]] = {\
            "delay":{\
            "warning" : str(sla_data["delay_warning"].iloc[i]), \
            "alert" : str(sla_data["delay_alert"].iloc[i])\
            },            \
            "flow" : sla_data["flow"].iloc[i],\
            "action" : "ADD"}


    def handle_measurments(self, ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
        flowID = method.routing_key.split(".", 1)[1]
        measurment_dict = json.loads(body.decode("utf-8"))

        if "state" in measurment_dict.keys():

                if measurment_dict["state"] == "OK":

                    # Delete from priorFlows
                    tempPriors = [item for item in self.priorFlows if item[0] == flowID]
                    if len(tempPriors) > 0 :
                        try:
                            self.priorFlows.remove(tempPriors[0])
                            self.switch.set_priority(flowID, measurment_dict["created"], 0)
                        except ValueError:
                            pass

                    if flowID not in self.measurements.keys():
                        pass
                    else:
                        temp, nr = self.measurements[flowID]
                        if nr >= 3:
                            self.switch.set_modify(flowID, temp["created"], 0)
                        self.measurements[flowID] = (measurment_dict, 0)

                elif measurment_dict["state"] == "WARNING":
                    tempPriors = [item for item in self.priorFlows if item[0] == flowID]
                    if len(tempPriors) > 0 and tempPriors[0][1] + 60 < time.time() :
                        try:
                            self.priorFlows.remove(tempPriors[0])
                            self.switch.set_priority(flowID, measurment_dict["created"], 0)
                        except ValueError:
                            pass

                    if flowID not in self.measurements.keys():
                        self.measurements[flowID]  = (measurment_dict, 0)
                    else:
                        temp_dict, nr = self.measurements[flowID]
                        if temp_dict["state"] == "OK":
                            nr = 0
                        else:
                            nr = nr + 1

                        if nr==3:
                            self.switch.set_modify(flowID, measurment_dict["created"], 0)

                        else:
                            self.measurements[flowID]  = (measurment_dict, nr)


                elif measurment_dict["state"] == "ALERT":


                    if flowID not in self.measurements.keys():
                        self.measurements[flowID]  = (measurment_dict, 0)
                    else:
                        temp_dict, nr = self.measurements[flowID]
                        if temp_dict["state"] == "OK":
                            nr = 0
                        else:
                            nr = nr + 1

                        if nr==3:
                            nr = nr + 1
                            tempPriors = [item for item in self.priorFlows if item[0] == flowID]
                            if len(tempPriors) == 0 :
                                self.switch.set_priority(flowID, measurment_dict["created"], 1)
                                self.priorFlows.append((flowID, time.time()))
                                #print(self.priorFlows)
                            tempPriors = [item for item in self.priorFlows if item[0] == flowID]

                            if len(tempPriors) > 0 and tempPriors[0][1] + 60 < time.time() :
                                try:
                                    self.priorFlows.remove(tempPriors[0])
                                    self.switch.set_priority(flowID, measurment_dict["created"], 0)
                                except ValueError:
                                    pass

                            self.switch.set_modify(flowID, measurment_dict["created"], 1)
                            self.measurements[flowID]  = (measurment_dict, nr)
                        else:
                            self.measurements[flowID]  = (measurment_dict, nr)

    def add_sla_checkers(self, binding_key, no_ack=True):
        try:
            result = self.channel.queue_declare(exclusive=False)
            queue_name = result.method.queue
            self.channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=binding_key)
            self.channel.basic_consume(self.get_sla, queue=queue_name, no_ack=no_ack)
            self.channel.start_consuming()
        except Exception as error:
            logging.debug("The connection was down, following error occurred: %s", error)

    def get_sla(self, ch, method, properties, body):
        try:
            sla_dict = json.loads(body.decode("utf-8"))
            if "GET" in sla_dict.keys():
                print(sla_dict["GET"])
                # check if the number for the sla checker is unique
                if sla_dict["GET"] not in self.sla_checkers:
                    # add sla checker with that number to the table
                    self.sla_checkers.append(sla_dict["GET"])
                    # send all local data
                    for flow in self.sla.keys():
                        temp = self.sla[flow]
                        temp["action"] = "ADD"
                        temp["flow"] = flow
                        self.add_sla_flow("SLA."+str(sla_dict["GET"]), temp)
                else:
                    pass #

        except json.decoder.JSONDecodeError:
            pass


    def parse_sla(self, ch, method, properties, body):
        """ Getting information about added / modfied / deleted SLAs, parsing them
            and sending to listening SLA checkers - to the persistence module """

        sla_dict = json.loads(body.decode("utf-8"))
        keys = sla_dict.keys() # Getting the list of all listening SLA checkers


        if "action" in keys and "flow" in keys:

            if sla_dict["action"] == "ADD" or sla_dict["action"] == "MODIFY":
                # add to self.sla
                temp_dict = {}
                if "delay" in keys:
                    temp_dict["delay"] = sla_dict["delay"]

                self.sla[sla_dict["flow"]] = temp_dict
            #    print(self.sla)

                temp = self.sla[sla_dict["flow"]]
                temp["action"] = "ADD"
                temp["flow"] = sla_dict["flow"]

                for sla_checker in self.sla_checkers:
                    self.add_sla_flow("SLA."+str(sla_checker), temp)

                alert = None
                warning = None
                if("alert" in temp_dict["delay"].keys()):
                    alert = int(temp_dict["delay"]["alert"])
                if("warning" in temp_dict["delay"].keys()):
                    warning = int(temp_dict["delay"]["warning"])

                self.dataBaseConnector.add_to_db(temp["flow"], alert=alert, warning=warning)

            if sla_dict["action"] == "DELETE":
                # check if flow exists in self.sla
                if sla_dict["flow"] in self.sla:
                    temp = self.sla[sla_dict["flow"]]
                    temp["action"] = sla_dict["action"]
                    temp["flow"] = sla_dict["flow"]
                    # delete entry
                    self.sla.pop(sla_dict["flow"])
                #    print(self.sla)’

                    for sla_checker in self.sla_checkers: # Send to all listening SLA checkers
                        self.add_sla_flow("SLA."+str(sla_checker), temp)


                    self.dataBaseConnector.del_from_db(temp["flow"])

    def consume(self, binding_key, function_name="callback",no_ack=True, exclusive=False):
        try:
            self.connection = pika.BlockingConnection(self.params)
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.type)

            result = self.channel.queue_declare(exclusive=False)
            queue_name = result.method.queue
            function = getattr(self,function_name)
            self.channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=binding_key)
            self.channel.basic_consume(function, queue=queue_name, no_ack=no_ack)
            self.channel.start_consuming()
        except Exception as error:
            logging.debug("The connection was down, following error occurred: %s", error)


def main():
    scriptPath = sys.argv[0]
    filename = os.path.basename(scriptPath)
    directory = re.sub(filename+"$", "", scriptPath)
    if len(directory) == 0:
        directory = "."
    os.chdir(directory)

    s = Server()

    t1 = threading.Thread(target = s.consume, args=("SLA.server", "parse_sla",))
    t2 = threading.Thread(target = s.consume, args=("SLA.get", "get_sla",))
    t3 = threading.Thread(target = s.consume, args=("measured.#", "handle_measurments",))

    t1.start()
    time.sleep(1)
    t2.start()
    time.sleep(1)
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    s.close()

if __name__ == "__main__":
    main()
