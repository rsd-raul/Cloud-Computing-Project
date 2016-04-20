from aws.EC2 import EC2Instance
from aws.Connections import Connection
from aws.Volumes import Volumes
from aws.S3 import S3Bucket
from aws.Glacier import GlacierVaults
from aws.CloudWatch import CloudWatch
from aws.AutoScale import AutoScale

from openstack.EC2 import EC2InstanceOS
from openstack.S3 import S3BucketOS

from boto import exception
from time import sleep
import webbrowser


class Application:

    # ----------------------------------------------- CONSTRUCTOR ------------------------------------------------

    def __init__(self):

        # Menus and sub-menus declaration
        self.menuString = {
            '0': [
                "Compute",
                "Storage",
                "Monitoring",
                "Extras"],
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
                "Launch a new instance",
                "Create a new volume (new)"],
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
                "Set an alarm"],
            '31': [
                "Activate monitoring (new)",
                "Get metrics"],
            '4': [
                "Glacier Vaults Interface (new)",
                "AutoScale Interface (new)",
                "Delete everything *warning"],
            '41': [
                "List Vaults (new)",
                "Create Vault (new)",
                "Delete Vault (new)"],
            '42': [
                "Testing connection (new)",
                "Create AutoScaling Group (new)",
                "Delete AutoScaling Group (new)",
                "Create Scaling policies (up and down) (new)",
                "Create custom Alarm w. AutoScale (new)"
            ]
        }
        # Interface related strings
        self.app_strings = {
            'starting_app': "\n~~~~~~~~~~ Starting system ~~~~~~~~~\n",
            'terminated': "\n~~~~~~~~~~~~~ Good Bye ~~~~~~~~~~~~~\n",
            'terminating': "------ Terminating everything ------",
            'restart': "\n-------------- Options -------------\n",
            'start': "\n/--------- Starting action --------\\\n",
            'completed': "\n\\-------- Action completed --------/\n",
            'no_running': "---------- Nothing running ---------",
            'no_selected': "--------- Nothing selected ---------",
            'no_found': "----------- Nothing found ----------",
            'created': "--------- Instance created ---------",
            'selected': "-------- Instances selected --------\n",
            'created_glacier': "------ Glacier Vault created -------",
            'deleted_glacier': "------ Glacier Vault deleted -------",
            'created_vol': "---------- Volume created ----------",
            'attached': "---------- Volume attached ---------\n",
            'detached': "---------- Volume detached ---------\n",
            'stored': "------------ File stored -----------",
            'removed': "------------ File removed ----------",
            'downloaded': "---------- File downloaded ---------",
            'creating_alarm': "---------- Creating alarm ----------\n",
            'created_alarm':  "\n----------- Alarm created ----------",
            'failure_alarm':  "---------- Creation failed ---------",
            'created_group':  "\n----------- Group created ----------",
            'deleted_group':  "\n----------- Group deleted ----------"
        }
        # Initialize app with main menu
        print self.app_strings['starting_app']
        self.process_selection(0)

    # --------------------------------------------- MENU & REACTION ----------------------------------------------

    def show_menu(self, key):
        """ Based on the unique key that identifies the menu, show it """

        # Retrieve the menu from the menu list
        menu = self.menuString[key]

        # Iterate over all the options and show an index besides
        for index, value in enumerate(menu, 1):
            print index, value

        # Unless we are in the main menu, show a "Go back" button
        if key != '0':
            print ('%s Go back' % (len(menu)+1))

    def process_selection(self, action):
        """ Based on the user input, this method decides how to proceed (show menu / do action) """

        # In case of a menu, input_needed will request the user for one of the options on the menu list
        input_needed = True

        # Number of options in each menu, initialized to 3 as it's the most frequent value
        max_val = 3

        # Main menu
        if action == 0:
            self.show_menu('0')
            max_val = 4

        # Secondary Menus
        elif action == 1 or action == 2:
            self.show_menu('12')
        elif action == 11:
            self.show_menu('1-1')
            max_val = 10
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
        elif action == 31:
            self.show_menu('31')
        elif action == 4:
            self.show_menu('4')
            max_val = 4
        elif action == 41:
            self.show_menu('41')
            max_val = 4
        elif action == 42:
            self.show_menu('42')
            max_val = 6

        # Go back options
        elif action == 13 or action == 120 or action == 1123 or action == 1183 or action == 122 or action == 216 \
            or action == 2123 or action == 226 or action == 2223 or action == 23 or action == 33 or action == 313 \
                or action == 44 or action == 414 or action == 426:
            # If it's a go back option divide the "action" by 100 without rest, that will effectively bring you back
            self.process_selection(action // 100)
            input_needed = False

        # Actions
        else:
            # If it's not a "menu/sub-menu" or a "go back" option, it's an action, execute it
            self.apply_action(action)
            input_needed = False

        # If is not a "Go back" or an action, don't request input
        if input_needed:
            self.process_selection((action*10) + Application.ask_option(max_val))

    # -------------------------------------------------- ACTIONS -------------------------------------------------

    def apply_action(self, action):
        """ Depending on the user action request, this method will execute the suitable code/functionality """

        print self.app_strings['start']

        # AWS - List all running instances / Choose from list / Enter an instance ID
        if action == 111 or action == 1121 or action == 1122:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

            # Find all running instances
            instances = EC2Instance.find_instances_running(conn_ec2)

            # If there is nothing running, inform the user
            if not instances:
                print self.app_strings['no_running']

            # If there are instances running, react depending of the user choice
            else:
                # 111 - List all
                if action == 111:
                    # Format and print the requested information
                    print "Running AWS EC2 instances"
                    for index, instance in enumerate(instances):
                        # This method will be tasked with the extraction and formatting of the instance attributes
                        self.print_instance(index, instance)

                # 1121 - Choose from list
                elif action == 1121:
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

                # 1122 - Enter an instance ID
                else:
                    # Request the instance Id
                    inst_id = self.ask_string()

                    something = False
                    # Iterate over all the instances looking for the requested one (by id)
                    for instance in instances:
                        if instance.id == inst_id:
                            # If the instance is found, format and print it, then exit the loop
                            print self.app_strings['selected']
                            self.print_instance(-1, instance)
                            something = True
                            break

                    # If no instances where found, inform the user
                    if not something:
                        print self.app_strings['no_selected']

        # AWS - Start a new instance based on an existing AMI
        elif action == 113:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

            # Keep asking for a correct ami until it's correctly introduced
            success = False
            while not success:
                try:
                    # Ask the user for the ami
                    ami = self.ask_custom_string("Type the ami: ")

                    # Launch the new instance based on the ami
                    EC2Instance.create_instance_with_ami(conn_ec2, ami)

                    print self.app_strings['created']
                    success = True

                # If an exception is raised, notify the user of the incorrect ami format and ask again
                except exception.EC2ResponseError:
                    print "Invalid id, expecting 'ami-...'\n"

        # AWS - Stop all instances / a specific instance
        elif action == 114:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

            # Stop all the running instances
            EC2Instance.stop_instances(conn_ec2)

        # AWS - Stop a specific instance
        elif action == 115:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

            # Ask for the instance id
            instance_id = self.ask_string()

            # Stop the running instance based on the id
            EC2Instance.stop_instance(conn_ec2, instance_id)

        # AWS - Create a new volume
        elif action == 119:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

            # Create the new volume
            success = Volumes.create_volume(conn_ec2)
            if success:
                print self.app_strings['created_vol']

        # AWS - Attach/Detach an existing volume to/from an instance
        elif action == 116 or action == 117:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

            # Find all volumes
            volumes = Volumes.list_volumes(conn_ec2)

            # if there are running volumes
            if volumes:
                # Show and ask for the volume
                print "Volumes available:"
                for index, volume in enumerate(volumes, 1):
                    print '\t', index, 'Id:', volume.id, 'Zone', volume.zone, 'Status:', volume.status

                print "\nType the number of the Volume to attach:"
                volume_num = self.ask_option(len(volumes))

                # Retrieve the volume from the list and extract the required id
                volume = volumes[volume_num - 1]
                volume_id = volume.id

                # 116 Attach an existing volume to an instance
                if action == 116:
                    # Extract the zone
                    volume_zone = volume.zone

                    # Get all instances in the volume zone (different zones are incompatible)
                    instances = EC2Instance.find_instances_running_zone(conn_ec2, volume_zone)

                    # If there are instances
                    if instances:
                        # Show the list of instances with an index for the user to choose from
                        print "Instances available:"
                        for index, instance in enumerate(instances, 1):
                            print '\t', index, 'Id:', instance.id, 'Zone', instance.placement, 'State:', instance.state

                        # Ask for the instance and retrieve the instance id
                        print "\nType the number of the Instance to attach the Volume:", volume_id
                        instance_num = self.ask_option(len(instances))
                        instance_id = instances[instance_num - 1].id

                        # Attach the volume and notify if the operation was successful
                        success = Volumes.attach_volume(conn_ec2, volume_id, instance_id)
                        if success:
                            print self.app_strings['attached']

                    # Notify the user if there are no instances running in the volume's zone
                    else:
                        print "\nYou need running instances in the zone: ", volume_zone, \
                              "\nto perform the attach operation"

                # 117 Detach a volume from an instance
                else:
                    # Detach the volume with the id provided by the user and notify if the operation is successful
                    success = Volumes.detach_volume(conn_ec2, volume_id)
                    if success:
                        print self.app_strings['detached']

            # If there are no running volumes, notify the user
            else:
                print "\nYou need running volumes\n" \
                      "to perform the operation"

        # AWS - Launch a new instance - Windows instance / Linux instance
        elif action == 1181 or action == 1182:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

            # Depending on the request, apply for a windows or a linux machine
            so = "windows" if action == 1181 else "linux"

            # Create a new instance passing the os request as a parameter
            EC2Instance.create_instance_with_so(conn_ec2, so)
            print self.app_strings['created']

        # OS - List all running instances
        elif action == 121:

            # List all running instances
            nodes = EC2InstanceOS.find_instances_running()

            # If nothing is running, notify the user
            if not nodes:
                print self.app_strings['no_running']
            else:
                # Format and print the retrieved instances
                print "\nRunning AWS EC2 nodes"
                for index, node in enumerate(nodes):
                    # This method will print the requested attributes from each of the nodes (instances)
                    self.print_node(index, node)

        # AWS - List all buckets
        elif action == 211:
            # Start a S3 connection
            conn_s3 = Connection.s3_connection()

            # Retrieve all the buckets
            buckets = S3Bucket.list_buckets(conn_s3)

            # If there are buckets, print them with a custom format
            if buckets:
                print "Current AWS S3 Buckets:"
                for b in buckets:
                    print "\n\t", b.name
            # If not, notify the user
            else:
                print self.app_strings['no_found']

        # AWS - List all objects in a bucket - Choose from list
        elif action == 2121:
            # Start a S3 connection
            conn_s3 = Connection.s3_connection()

            # Retrieve all the buckets
            buckets = S3Bucket.list_buckets(conn_s3)

            # If there are buckets
            if buckets:
                # Show them all and ask for the index of the desired one
                print "Current AWS S3 Buckets:"
                for index, bucket in enumerate(buckets, 1):
                    print '\t', str(index) + ":", bucket.name

                print "\nType the number of the Bucket"
                bucket_num = self.ask_option(len(buckets))

                # Retrieve all objects in the bucket
                bucket_objects = buckets[bucket_num - 1].list()

                # If the bucket have object, print them (their name)
                if bucket_objects:
                    print "The objects in the bucket are:"
                    for bucket_object in bucket_objects:
                        print '\t' + str(bucket_object.key)
                # If no objects are found, notify the user
                else:
                    print self.app_strings['no_found']

            # If no buckets are found, notify the user
            else:
                print self.app_strings['no_found']

        # AWS - List all objects in a bucket - Enter a bucket name
        elif action == 2122:
            # Start a S3 connection
            conn_s3 = Connection.s3_connection()

            # Retrieve all the buckets
            buckets = S3Bucket.list_buckets(conn_s3)

            # If there are buckets
            if buckets:
                # Ask for the bucket name
                print "\nType the name of the Bucket"
                bucket_name = self.ask_custom_string("Type the name: ")

                # Iterate over the buckets looking for a match in names
                success = False
                for bucket in buckets:
                    if bucket.name == bucket_name:
                        success = True

                        # If the bucket is found retrieve its files and print them (Their name
                        bucket_objects = bucket.list()
                        print "The objects in the bucket are:"
                        for bucket_object in bucket_objects:
                            print '\t' + str(bucket_object.key)

                        # If there are no files, warn the user
                        if not bucket_objects:
                            print self.app_strings['no_found']

                        # As the bucket name must be unique, break from the loop
                        break

                # If there are no bucket with that name, warn the user
                if not success:
                    print self.app_strings['no_found']

            # If there are no bucket, warn the user
            else:
                print self.app_strings['no_found']

        # AWS - Upload / Download / Delete an object
        elif action == 213 or action == 214 or action == 215:
            # Start a S3 connection
            conn_s3 = Connection.s3_connection()

            # Retrieve all the buckets
            buckets = S3Bucket.list_buckets(conn_s3)

            # If there are buckets
            if buckets:
                # Show all the buckets with an index and ask the user to select one
                print "Current AWS S3 Buckets:"
                for index, bucket in enumerate(buckets, 1):
                    print '\t', str(index) + ":", bucket.name

                # Ask the user for the index and retrieve the bucket with it
                print "\nType the number of the Bucket"
                bucket_num = self.ask_option(len(buckets))
                bucket = buckets[bucket_num - 1]

                # Ask for the identifier of the file and depending on the requested action delete/upload/download it.
                print "Type the identifier of the file"
                file_title = self.ask_string()

                # 213 Upload an object
                if action == 213:
                    # Ask for the location of the file to upload
                    print "Type the location of the file (e.g. res/test.txt"
                    file_location = self.ask_custom_string("Type location: ")

                    # Store in the bucket the file with the title provided and from the location given
                    success = S3Bucket.store_in_bucket(bucket, file_title, file_location)
                    if success:
                        print self.app_strings['stored']

                # 214 Download an object
                elif action == 214:
                    # Search among the bucket files for one with the title typed by the user
                    for key in bucket.list():
                        if key.name == file_title:
                            # If found, download it to res/... and notify the user
                            print "Downloading to res/\n"
                            key.get_contents_to_filename('res/' + key.name)
                            print self.app_strings['downloaded']

                # 215 Delete an object
                else:
                    # Delete the file from the bucket using its name and notify the user
                    S3Bucket.delete_from_bucket(bucket, file_title)

                    print self.app_strings['removed']

            # If there are no bucket, warn the user
            else:
                print self.app_strings['no_found']

        # OS - List all buckets
        elif action == 221:

            # Retrieve all buckets
            buckets = S3BucketOS.list_buckets()

            # If there are buckets
            if buckets:
                print "\nCurrent OS S3 Buckets:"
                for b in buckets:
                    print "\n\t", b.name

            # If there are no bucket, warn the user
            else:
                print self.app_strings['no_found']

        # OS - List all objects in a bucket - Enter a bucket name
        elif action == 2222:

            # Retrieve all buckets
            buckets = S3BucketOS.list_buckets()

            # If there are buckets
            if buckets:
                # Ask for the bucket name
                print "\nType the name of the Bucket"
                bucket_name = self.ask_custom_string("Type the name: ")

                # Iterate all the buckets looking for a name match
                success = False
                for bucket in buckets:
                    if bucket.name == bucket_name:
                        success = True
                        bucket_objects = bucket.list_objects()

                        # If there are files, list them with a customized format
                        if bucket_objects:
                            print "The objects in the bucket are:"
                            for bucket_object in bucket_objects:
                                print '\t' + bucket_object.name

                        # If there are no files, warn the user
                        else:
                            print self.app_strings['no_found']

                # If there is no bucket with that name, warn the user
                if not success:
                    print self.app_strings['no_found']

            # If there are no buckets, warn the user
            else:
                print self.app_strings['no_found']

        # OS - Upload / Download / Delete an object / List all objects
        elif action == 223 or action == 224 or action == 225 or action == 2221:

            # Retrieve all buckets
            buckets = S3BucketOS.list_buckets()

            # If there are buckets
            if buckets:
                # Show and ask for the bucket
                print "Current OS S3 Buckets:"
                for index, bucket in enumerate(buckets, 1):
                    print '\t', str(index) + ":", bucket.name

                print "\nType the number of the Bucket"
                bucket_num = self.ask_option(len(buckets))

                # 2221 List all objects in a bucket
                if action == 2221:
                    # Retrieve all files in the bucket
                    bucket_objects = buckets[bucket_num - 1].list_objects()

                    # If there are files, list them with a customized format
                    if bucket_objects:
                        for bucket_object in bucket_objects:
                            print '\t' + bucket_object.name

                    # If there are no files in the bucket, warn the user
                    else:
                        print self.app_strings['no_found']

                # 223, 224, 225 Upload / Download / Delete an object
                else:
                    # Retrieve the correct bucket from the list
                    bucket = buckets[bucket_num - 1]

                    # Ask for the identifier of the file and depending on the action upload/download/delete it
                    print "Type the identifier of the file"
                    file_title = self.ask_string()

                    # 223 Upload an object
                    if action == 223:
                        # Asl for the location of the file to upload
                        print "Type the location of the file"
                        file_location = self.ask_custom_string("Type location: ")

                        # Save in the bucket the file on the desired location with the desired name
                        S3BucketOS.store_in_bucket(bucket, file_title, file_location)
                        print self.app_strings['stored']

                    # 224, 225 Download/Delete an object
                    else:
                        # Iterate over all the objects in the bucket looking for a name/title match
                        for key in bucket.list_objects():
                            if key.name == file_title:

                                # 224 Download an object
                                if action == 224:
                                    # Download the object on the resources folder and notify the user
                                    print "Downloading to res/\n"
                                    key.download('res/' + key.name)
                                    print self.app_strings['downloaded']

                                # 225 Delete an object
                                else:
                                    # Delete the object from the bucket and notify the user
                                    key.delete()
                                    print self.app_strings['removed']

            # If there are no buckets, warn the user
            else:
                print self.app_strings['no_found']

        # Performance metrics for a EC2 instance - Activate monitoring / Query an instance / Setup alarm
        elif action == 311 or action == 312 or action == 32:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

            # Retrieve all actives
            instances = EC2Instance.find_instances_running(conn_ec2)

            # If no instances are found, exit
            if not instances:
                print self.app_strings['no_running']

            # If there are instances
            else:
                # Show index and id for the user to select the desired ones
                print "Running AWS EC2 instances:\n"
                for index, instance in enumerate(instances, 1):
                    print index, ':', instance.id

                # Ask for the desired instances
                print "\nType the number of the id"
                index = self.ask_option(len(instances))

                # Retrieve the instance from the list
                instance = instances[index-1]

                # 311 Activate monitoring
                if action == 311:
                    CloudWatch.enable_cw_on_instance(conn_ec2, str(instance.id))

                # 312 Get metrics
                elif action == 312:
                    # New CW connection
                    conn_cw = Connection.cw_connection()

                    # Query the CloudWatch metrics by the instance id
                    CloudWatch.query_cw_by_instance_id(str(instance.id), conn_cw)

                # 32 Create an alarm
                else:
                    # Retrieve the necessary fields for the alarm creation (offering clues to guide the user)
                    print "Type a short but meaningful name for your alarm."
                    alarm_name = self.ask_custom_string("Type name: ")

                    print "Type the email address you want to be notified when the alarm fires."
                    email_address = self.ask_custom_string("Type email: ")

                    print "Type the Metric you want to be notified about. Valid values are:"
                    print "DiskReadBytes | DiskWriteBytes | DiskReadOps | DiskWriteOps"
                    print "NetworkIn | NetworkOut"
                    print "CPUUtilization"
                    metric_name = self.ask_custom_string("Type metric: ")

                    print "Type the comparison operator. Valid values are:"
                    print ">= | > | < | <="
                    comparison = self.ask_custom_string("Type operator: ")

                    print "Type the threshold value that the metric will be compared against."
                    threshold = self.ask_custom_string("Type threshold: ")

                    print "Type the granularity of the returned data."
                    print "Minimum value is 60 (seconds), others must be multiples of 60."
                    period = self.ask_custom_string("Type period: ")

                    print "Type the number of periods over which the alarm must be"
                    print "measured before triggering notification."
                    eval_periods = self.ask_custom_string("Type number of periods: ")

                    print "Type the statistic to apply. Valid values are:"
                    print "SampleCount | Average | Sum | Minimum | Maximum"
                    statistics = self.ask_custom_string("Type statistic: ")

                    # Create the alarm with the fields the user introduced
                    print self.app_strings['creating_alarm']
                    success = CloudWatch.create_cw_alarm(instance.id, alarm_name, email_address, metric_name,
                                                         comparison, threshold, period, eval_periods, statistics)

                    # Notify the user of the result of the operation
                    if success:
                        print self.app_strings['created_alarm']
                    else:
                        print self.app_strings['failure_alarm']

        # AWS - List all Glacier Vaults
        elif action == 411:

            # Start a Glacier connection
            conn_glacier = Connection.glacier_connection()

            # Retrieve all the vaults for the account
            vaults = GlacierVaults.list_vaults(conn_glacier)

            # If there are vaults, show them formatted with the required fields
            if vaults:
                print "Active Vaults:"
                for index, vault in enumerate(vaults, 1):
                    print '\t' + str(index) + ':', 'Name:', vault.name, 'Size:', vault.size,\
                        'Created in:', vault.creation_date

            # If there aren't, notify the user
            else:
                print self.app_strings['no_found']

        # AWS - Create / Delete a Glacier Vault
        elif action == 412 or action == 413:
            # Start a Glacier connection
            conn_glacier = Connection.glacier_connection()

            # Ask the user for the name of the vault
            name = self.ask_custom_string("Type vault name: ")

            # 412 Create a Glacier Vault
            if action == 412:

                # Create a vault wih the provided name (duplication is ignored by AWS, no need to control it)
                GlacierVaults.create_vault(conn_glacier, name)
                print self.app_strings['created_glacier']

            # 413 Delete a Glacier Vault
            else:
                # Delete the vault from AWS (non-existent vault names are ignored by AWS, no need to control it)
                GlacierVaults.delete_vault(conn_glacier, name)
                print self.app_strings['deleted_glacier']

        # AWS - Auto Scale - Test connection
        elif action == 421:

            # Test the connection with AutoScale by printing it
            print "Testing connection:"
            print '\n\t', Connection.as_connection()

        # AWS - Auto Scale - Create Auto Scaling Group
        elif action == 422:

            # Create an AutoScaling connection
            conn_as = Connection.as_connection()

            # Ask for the required fields for creation
            launch_config_name = self.ask_custom_string("Type Launch Configuration name: ")
            as_group_name = self.ask_custom_string("Type Auto Scaling group name: ")

            # Ask for min and max limits for the instances in the group
            min_inst = self.ask_custom_int("Type min instances (min 0, max 20)", 0, 20)
            max_inst = self.ask_custom_int("Type max instances (min " + str(min_inst) + " max 40)", min_inst, 40)

            # Create the Launch Configuration and the Auto Scaling Group, notify the user of the result
            success = AutoScale.create_as_group(conn_as, launch_config_name, as_group_name, min_inst, max_inst)
            if success:
                print self.app_strings['created_group']

        # AWS - Auto Scale - Delete Auto Scaling Group
        elif action == 423:

            # Create an AutoScaling connection
            conn_as = Connection.as_connection()

            # Ask for an existing
            launch_config_name = self.ask_custom_string("Type Launch Configuration name: ")
            as_group_name = self.ask_custom_string("Type Auto Scaling group name: ")

            # Try to delete the Launch Configuration and the Auto Scaling Group, notify the user of the result
            success = AutoScale.delete_as_group(conn_as, as_group_name, launch_config_name)
            if success:
                print self.app_strings['deleted_group']

        # AWS - Auto Scale - Create policies
        elif action == 424:

            # Create an AutoScaling connection
            conn_as = Connection.as_connection()

            # Ask for the Group name to create the policies, the method will handle the exceptions
            as_group_name = self.ask_custom_string("Type Auto Scaling group name: ")
            AutoScale.create_scale_policies(conn_as, as_group_name)

        # AWS - Auto Scale - Create alarm
        elif action == 425:
            # Create both AutoScaling and CloudWatch connections
            conn_as = Connection.as_connection()
            conn_cw = Connection.cw_connection()

            # Ask for the necessary fields for the alarm creation (offering clues for the user to follow)
            print "Type the Auto Scaling group name to set the alarm on"
            as_group_name = self.ask_custom_string("Type Auto Scaling group name: ")

            print "Type a short but meaningful name for your alarm."
            alarm_name = self.ask_custom_string("Type name: ")

            print "Select the scaling policy. Valid values are:"
            print "scale_up | scale_down "
            scaling_policy_name = self.ask_custom_string("Type one of them")

            print "Type the Metric you want to be notified about. Valid values are:"
            print "DiskReadBytes | DiskWriteBytes | DiskReadOps | DiskWriteOps"
            print "NetworkIn | NetworkOut"
            print "CPUUtilization"
            metric_name = self.ask_custom_string("Type metric: ")

            print "Type the comparison operator. Valid values are:"
            print ">= | > | < | <="
            comparison = self.ask_custom_string("Type operator: ")

            print "Type the threshold value that the metric will be compared against."
            threshold = self.ask_custom_string("Type threshold: ")

            print "Type the granularity of the returned data."
            print "Minimum value is 60 (seconds), others must be multiples of 60."
            period = self.ask_custom_string("Type period: ")

            print "Type the number of periods over which the alarm must be"
            print "measured before triggering notification."
            eval_periods = self.ask_custom_string("Type number of periods: ")

            print "Type the statistic to apply. Valid values are:"
            print "SampleCount | Average | Sum | Minimum | Maximum"
            statistics = self.ask_custom_string("Type statistic: ")

            # Try to create the alarm and notify the user of the result
            print self.app_strings['creating_alarm']
            success = AutoScale.create_scale_alarm(conn_as, conn_cw, as_group_name, alarm_name, scaling_policy_name,
                                                   metric_name, comparison, threshold, period, eval_periods, statistics)
            if success:
                print self.app_strings['created_alarm']

        # AWS - Exit -> Terminate all
        elif action == 43:
            print self.app_strings['terminating']

            # Start EC2, AutoScaling and Glacier connections
            conn_ec2 = Connection.ec2_connection()
            conn_as = Connection.as_connection()
            conn_glacier = Connection.glacier_connection()

            # Terminate all instances
            print "\nTerminating instances:\n"
            EC2Instance.terminate_all_instances(conn_ec2)

            # Terminate all volumes (wait for instances to detach its volumes)
            print "\nTerminating volumes:\n"
            sleep(7)
            Volumes.delete_all_volumes(conn_ec2)
            print "\tTerminated"

            # Terminate all vaults
            print "\nTerminating vaults:\n"
            GlacierVaults.terminate_all_vaults(conn_glacier)
            print "\tTerminated"

            # Terminate all groups, launch configuration and policies
            print "\nTerminating groups, launch configuration and policies:\n"
            AutoScale.delete_everything(conn_as)
            print "\tTerminated"

            # Redirect to AWS web page to check manually, just in case
            print "\nRedirecting to amazon in 5 seconds, check manually!"
            sleep(5)
            webbrowser.open('https://eu-west-1.console.aws.amazon.com/ec2/v2/home?region=eu-west-1#')
            sleep(1)
            webbrowser.open('https://console.aws.amazon.com/s3/home?region=eu-west-1')
            sleep(1)
            webbrowser.open('https://eu-west-1.console.aws.amazon.com/glacier/home?region=eu-west-1')
            sleep(1)
            webbrowser.open('https://eu-west-1.console.aws.amazon.com/ec2/autoscaling/home?region=eu-west-1#'
                            'LaunchConfigurations:')
            sleep(1)
            webbrowser.open('https://eu-west-1.console.aws.amazon.com/ec2/autoscaling/home?region=eu-west-1#'
                            'AutoScalingGroups:')

        # Notify the user the action has been completed
        print self.app_strings['completed']

        # Restart the previous menu unless you are terminating all AWS instances/volumes/etc
        if action != 42:
            print self.app_strings['restart']
            self.process_selection(action // 10)
        else:
            print self.app_strings['terminated']

    # ------------------------------------------------ USER INPUT ------------------------------------------------

    @staticmethod
    def ask_string():
        """ Ask for a string id, must be composed of more than 1 character """

        valid = False
        result = ""

        while not valid:
            result = raw_input("Type id: ")
            if 1 <= len(result):
                valid = True

        print
        return result

    @staticmethod
    def ask_custom_string(question):
        """ Ask for a string with a custom question, the user input must be only one word"""

        valid = False
        result = ""

        while not valid:
            result = raw_input(question)
            if 1 <= len(result):
                valid = True

        print
        return result

    @staticmethod
    def ask_option(max_val):
        """ Ask for a number, must be more than 0 and less than the max value established by the request"""

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
    def ask_custom_int(question, min_val, max_val):
        """ Ask for a number with a custom question, the number must be more than the minimum value and
        less than the maximum value established by the request"""

        valid = False
        option = -1

        while not valid:
            try:
                option = int(raw_input(question))
                if min_val <= option <= max_val:
                    valid = True
            except ValueError:
                valid = False

        print
        return option

    @staticmethod
    def ask_multiple_options(max_val):
        """ Ask for several numbers, the size number list must be lower than the maximum value established
        all individual numbers must be lower/equal to the max value and bigger than 0"""

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
                            raise ValueError('number must be lower/equal to the max index and bigger than 0')

            except ValueError:
                valid = False

        print
        return list_values

    # ------------------------------------------------ FORMATTING ------------------------------------------------

    @staticmethod
    def print_instance(index, instance):
        """ This method is tasked with the extraction and formatting of the instance attributes """

        # Print the index with the correct format if the index is available
        index_str = "\t" + ("" if index == -1 else str(index) + ':')

        # Print each of the requested instance attributes
        print index_str, instance.id, '-', instance.instance_type, '<' + str(instance.region) + \
            '>: <Running since:', str(instance.launch_time) + '>'

    @staticmethod
    def print_node(index, node):
        """ This method is tasked with the extraction and formatting of the instance attributes, as
         LibCloud supports many different Cloud Services, the AWS formatting is also provided """

        result = "\t" + ("" if index == -1 else str(index) + ':')

        # Amazon Web Services
        # print result, node.id, '-', node.extra['instance_type'], '<' + node.extra['availability'] + \
        #                                                          '>: <Running since:', node.extra['launch_time'] + '>'

        # OpenStack

        # Calculate the machine type based on the flavorId
        flavours = {'1': "tiny", '2': "small", '3': "medium", '4': "large", '5': "x-large"}
        instance_type = "m1." + str(flavours[node.extra['flavorId']])

        # Print each of the requested instance attributes
        print result, node.id, '-', instance_type, '<' + node.extra['availability_zone'] + '>: <Running since:', \
            node.extra['created'] + '>'
