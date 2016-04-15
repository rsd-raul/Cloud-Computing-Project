from EC2 import EC2Instance
from Connections import Connection


class Application:

    # ----------------------------------------------- CONSTRUCTOR ------------------------------------------------

    def __init__(self):
        self.menuString = {
            '0': [
                "Compute",
                "Storage",
                "Monitoring",
                "Exit"],
            '12': [
                "AWS",
                "OpenStack"],
            '1-1': [
                "List all running instances",
                "List some of the running instances",
                "Start a new instance based on an existing AMI",
                "Stop all instances",
                "Stop a specific instance",
                "Attach an existing volume to an instance",
                "Detach a volume from an instance",
                "Launch a new instance"],
            '1-1-2': [
                "Choose from list",
                "Enter an instance ID"],
            '1-1-8': [
                "Windows instance",
                "Linux instance"],
            '1-2': [
                "List all running instances"],
            '2-12': [
                "List all buckets",
                "List all objects in a bucket",
                "Upload an object",
                "Download an object",
                "Delete an object"],
            '2-12-2': [
                "Choose from list",
                "Enter a bucket name"],
            '3': [
                "Performance metrics for a EC2 instance",
                "Set an alarm"]
        }
        self.app_strings = {
            'start': "\n/--------- Starting action --------\\\n",
            'no_running': "---------- Nothing running ---------",
            'no_selected': "--------- Nothing selected ---------",
            'created': "--------- Instance created ---------",
            'selected': "-------- Instances selected --------\n",
            'terminating': "------ Terminating everything ------",
            'terminated': "\n------------- Good Bye -------------\n",
            'restart':    "\n------------ Restarting ------------\n",
            'completed': "\n\\-------- Action completed --------/\n"
        }
        # Initialize app with main menu
        self.process_selection(0)

    # --------------------------------------------- MENU & REACTION ----------------------------------------------

    def show_menu(self, key):
        menu = self.menuString[key]

        for index, value in enumerate(menu, 1):
            print index, value

        if key != '0':
            print ('%s Go back' % (len(menu)+1))

    def process_selection(self, action):
        input_needed = True
        max_val = 3             # Most frequent max value

        # Main menu
        if action == 0:
            self.show_menu('0')
            max_val = 4

        # Secondary Menus
        elif action == 1 or action == 2:
            self.show_menu('12')
        elif action == 11:
            self.show_menu('1-1')
            max_val = 9
        elif action == 112:
            self.show_menu('1-1-2')
        elif action == 118:
            self.show_menu('1-1-8')
        elif action == 12:
            self.show_menu('1-2')
            max_val = 2
        elif action == 21 or action == 22:
            self.show_menu('2-12')
            max_val = 6
        elif action == 212 or action == 222:
            self.show_menu('2-12-2')
        elif action == 3:
            self.show_menu('3')

        # Go back options
        elif action == 13 or action == 119 or action == 1123 or action == 1183 \
                or action == 122 or action == 216 or action == 2123 or action == 226 \
                or action == 2223 or action == 23 or action == 33:
            self.process_selection(action // 100)
            input_needed = False

        # Actions
        else:
            self.apply_action(action)
            input_needed = False

        # If is not a "Go back" or an action, don't request input
        if input_needed:
            self.process_selection((action*10) + Application.ask_option(max_val))

    # -------------------------------------------------- ACTIONS -------------------------------------------------

    def apply_action(self, action):
        print self.app_strings['start']

        # Exit -> Terminate all
        if action == 4:
            print self.app_strings['terminating']

            # Start a EC2 connection
            conn_ec2 = Connection().ec2_connection()

            # Terminate all instances
            EC2Instance.terminate_all_instances(conn_ec2)

        # AWS - List all running instances
        elif action == 111:
            # Start a EC2 connection
            conn_ec2 = Connection().ec2_connection()

            # List All
            instances = EC2Instance.find_instances_running(conn_ec2)

            if not instances:
                print self.app_strings['no_running']
            else:
                # Format and print the requested information
                print "Running AWS EC2 instances"
                for index, instance in enumerate(instances):
                    self.print_instance(index, instance)

        # AWS - List some of the running instances - Choose from list
        elif action == 1121:
            # Start a EC2 connection
            conn_ec2 = Connection().ec2_connection()

            # Retrieve all actives
            instances = EC2Instance.find_instances_running(conn_ec2)

            # If none, exit
            if not instances:
                print self.app_strings['no_running']
            else:
                # Show index and id for the user to select the desired ones
                print "Running AWS EC2 instances:\n"
                for index, instance in enumerate(instances, 1):
                    print index, ':', instance.id

                # Ask for the desired instances
                print "\nType the number/s (separated by spaces)"
                numbers = self.ask_multiple_options(len(instances))

                # Format and print
                for index in numbers:
                    instance = instances[index]
                    self.print_instance(index, instance)

        # AWS - List some of the running instances - Enter an instance ID
        elif action == 1122:
            # Start a EC2 connection
            conn_ec2 = Connection().ec2_connection()

            # Retrieve all actives
            instances = EC2Instance.find_instances_running(conn_ec2)

            # If none, exit
            if not instances:
                print self.app_strings['no_running']
            else:
                inst_id = self.ask_string()

                something = False
                for instance in instances:
                    if instance.id == inst_id:
                        if not something:
                            print self.app_strings['selected']
                        self.print_instance(-1, instance)
                        something = True

                if not something:
                    print self.app_strings['no_selected']

        # AWS - Start a new instance based on an existing AMI
        elif action == 113:
            # Start a EC2 connection
            conn_ec2 = Connection().ec2_connection()

            # Launch the new instance
            EC2Instance.create_instance(conn_ec2)

            print self.app_strings['created']
        # AWS - Stop all instances
        elif action == 114:
            # Start a EC2 connection
            conn_ec2 = Connection().ec2_connection()

            # Stop all the running instances
            EC2Instance.stop_instances(conn_ec2)

        # AWS - Stop a specific instance
        elif action == 115:
            # Start a EC2 connection
            conn_ec2 = Connection().ec2_connection()

            # Ask for the instance id
            instance_id = self.ask_string()

            # Stop the running instance
            EC2Instance.stop_instance(conn_ec2, instance_id)

        # AWS - Attach an existing volume to an instance
        elif action == 116:
            self.place_holder()

        # AWS - Detach a volume from an instance
        elif action == 117:
            self.place_holder()

        # AWS - Launch a new instance - Windows instance
        elif action == 1181:
            self.place_holder()

        # AWS - Launch a new instance - Linux instance
        elif action == 1182:
            self.place_holder()

        # OS - List all running instances
        elif action == 121:
            self.place_holder()

        # AWS - List all buckets
        elif action == 211:
            self.place_holder()

        # AWS - List all objects in a bucket - Choose from list
        elif action == 2121:
            self.place_holder()

        # AWS - List all objects in a bucket - Enter a bucket name
        elif action == 2122:
            self.place_holder()

        # AWS - Upload an object
        elif action == 213:
            self.place_holder()

        # AWS - Download an object
        elif action == 214:
            self.place_holder()

        # AWS - Delete an object
        elif action == 215:
            self.place_holder()

        # OS - List all buckets
        elif action == 221:
            self.place_holder()

        # OS - List all objects in a bucket - Choose from list
        elif action == 2221:
            self.place_holder()

        # OS - List all objects in a bucket - Enter a bucket name
        elif action == 2222:
            self.place_holder()

        # OS - Upload an object
        elif action == 223:
            self.place_holder()

        # OS - Download an object
        elif action == 224:
            self.place_holder()

        # OS - Delete an object
        elif action == 225:
            self.place_holder()

        # Performance metrics for a EC2 instance
        elif action == 31:
            self.place_holder()

        # Set an alarm
        elif action == 32:
            self.place_holder()

        print self.app_strings['completed']

        if action != 4:
            print self.app_strings['restart']
            self.process_selection(0)
        else:
            print self.app_strings['terminated']

    @staticmethod
    def place_holder():
        print "placeholder"

    # ------------------------------------------------ USER INPUT ------------------------------------------------

    @staticmethod
    def ask_string():
        valid = False
        result = ""

        while not valid:
            result = raw_input("Type id: ")
            if 1 <= len(result):
                valid = True

        print
        return result

    @staticmethod
    def ask_option(max_val):
        valid = False
        option = -1

        while not valid:
            try:
                option = int(raw_input("Select option: "))
                if 1 <= option <= max_val:
                    valid = True
            except ValueError:
                valid = False

        print
        return option

    @staticmethod
    def ask_multiple_options(max_val):
        valid = False
        list_values = []

        while not valid:
            try:
                user_input = raw_input("Type numbers: ")

                # Build a list of numbers based on the user input
                list_values = [int(value)-1 for value in user_input.split(' ')]

                # If the list is not empty and doesn't have more options than available, correct
                if 0 < len(list_values) <= max_val:
                    valid = True

                    # Unless one of the values is bigger (or equal, remember the -1 in the loop) than the max value
                    for value in list_values:
                        if value < 0 or value >= max_val:
                            raise ValueError('number must be lower/equal to the max index')

            except ValueError:
                valid = False

        print
        return list_values

    # ------------------------------------------------ FORMATTING ------------------------------------------------

    @staticmethod
    def print_instance(index, instance):
        result = "\t" + ("" if index == -1 else str(index) + ':')

        print result, instance.id, '-', instance.instance_type, '<' + str(instance.region) + \
            '>: <Running since:', str(instance.launch_time) + '>'
