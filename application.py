from EC2 import EC2Instance
from Connections import Connection


class Application:

    # ----------------------------------------------- CONSTRUCTOR ------------------------------------------------

    def __init__(self):
        self.menuString = {
            '0': [
                "Compute",
                "Storage",
                "Monitoring"],
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
                "Set an alarm"]}

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
        print "\n/--------- Starting action --------\\\n"

        # AWS - List all running instances
        if action == 111:
            # Start a EC2 connection
            conn_ec2 = Connection().ec2_connection()

            # List All
            instances = EC2Instance.find_instances_running(conn_ec2)

            if not instances:
                print "---------- Nothing running ---------"
            else:
                # Format and print the requested information
                print "Running AWS EC2 instances"
                for index, instance in enumerate(instances):
                    print index, ':', instance.id, '-', instance.instance_type, '<', instance.region, \
                        '>: <Running since:', instance.launch_time, '>'

        # AWS - List some of the running instances - Choose from list
        elif action == 1121:
            # Start a EC2 connection
            conn_ec2 = Connection().ec2_connection()

            # Retrieve all actives
            instances = EC2Instance.find_instances_running(conn_ec2)

            # If none, exit
            if not instances:
                print "---------- Nothing running ---------"
            else:
                # Show index and id for the user to select the desired ones
                print "Running AWS EC2 instances"
                for index, instance in enumerate(instances, 1):
                    print index, ':', instance.id

                # Ask for the desired instances
                print "Type the number/s (separated by spaces)"
                numbers = self.ask_multiple_options(len(instances))

                # If the user typed 0, exit
                if len(numbers) == 1 and numbers[0] == 0:
                    print "--------- Nothing selected ---------"
                # Else, format and print
                else:
                    for index in numbers:
                        instance = instances[index]
                        print index, ':', instance.id, '-', instance.instance_type, '<', instance.region, \
                            '>: <Running since:', instance.launch_time, '>'

        # AWS - List some of the running instances - Enter an instance ID
        elif action == 1122:
            self.place_holder()

        # AWS - Start a new instance based on an existing AMI
        elif action == 113:
            self.place_holder()

        # AWS - Stop all instances
        elif action == 114:
            self.place_holder()

        # AWS - Stop a specific instance
        elif action == 115:
            self.place_holder()

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

        print "\n\\-------- Action completed --------/\n"

        print "\n------------ Restarting ------------\n"
        self.process_selection(0)

    @staticmethod
    def place_holder():
        print "placeholder"

    # ------------------------------------------------ USER INPUT ------------------------------------------------

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
        result = []

        while not valid:
            result = []

            try:
                list_string = (raw_input("Select option: ")).split (' ')
                if 0 <= len(list_string) <= max_val:
                    valid = True
                    for aux in list_string:
                        value = int(aux)
                        result.append(value-1)
                        if value > max_val:
                            raise ValueError('number must be lower/equal to the max index')

            except ValueError:
                valid = False

        print
        return result
