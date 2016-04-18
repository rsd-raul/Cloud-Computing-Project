from aws.EC2 import EC2Instance
from aws.Connections import Connection
from aws.Volumes import Volumes
from aws.S3 import S3Bucket
from aws.Glacier import GlacierVaults
from aws.CloudWatch import CloudWatch
from aws.AutoScale import AutoScale

from openstack.EC2 import EC2InstanceOS
from openstack.S3 import S3BucketOS

from time import sleep
import webbrowser


class Application:

    # ----------------------------------------------- CONSTRUCTOR ------------------------------------------------

    def __init__(self):
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
                or action == 414 or action == 425:
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

        # AWS - List all running instances
        if action == 111:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

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
            conn_ec2 = Connection.ec2_connection()

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
            conn_ec2 = Connection.ec2_connection()

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
            conn_ec2 = Connection.ec2_connection()

            # Launch the new instance
            EC2Instance.create_instance(conn_ec2)

            print self.app_strings['created']
        # AWS - Stop all instances
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

            # Stop the running instance
            EC2Instance.stop_instance(conn_ec2, instance_id)

        # AWS - Create a new volume
        elif action == 119:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

            # Create the new volume
            success = Volumes.create_volume(conn_ec2)
            if success:
                print self.app_strings['created_vol']

        # AWS - Attach an existing volume to an instance
        elif action == 116:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

            # Get all volumes
            volumes = Volumes.list_volumes(conn_ec2)

            if volumes:
                # Show and ask for the volume
                print "Volumes available:"
                for index, volume in enumerate(volumes, 1):
                    print '\t', index, 'Id:', volume.id, 'Zone', volume.zone, 'Status:', volume.status

                print "\nType the number of the Volume to attach:"
                volume_num = self.ask_option(len(volumes))
                volume = volumes[volume_num - 1]
                volume_zone = volume.zone
                volume_id = volume.id

                # Get all instances
                instances = EC2Instance.find_instances_running_zone(conn_ec2, volume_zone)

                if instances:
                    # Show and ask for the instance
                    print "Instances available:"
                    for index, instance in enumerate(instances, 1):
                        print '\t', index, 'Id:', instance.id, 'Zone', instance.placement, 'State:', instance.state

                    print "\nType the number of the Instance to attach the Volume:", volume_id
                    instance_num = self.ask_option(len(instances))
                    instance_id = instances[instance_num - 1].id

                    # Attach and notify
                    success = Volumes.attach_volume(conn_ec2, volume_id, instance_id)
                    if success:
                        print self.app_strings['attached']
                else:
                    print "\nYou need running instances in the zone:\n", volume_zone, \
                          "to perform the attach operation"
            else:
                print "\nYou need running volumes\n" \
                      "to perform the attach operation"

        # AWS - Detach a volume from an instance
        elif action == 117:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

            # Get all volumes
            volumes = Volumes.list_volumes(conn_ec2)

            if volumes:
                # Show and ask for the volume
                print "Volumes available"
                for index, volume in enumerate(volumes, 1):
                    print '\t', index, 'Id:', volume.id, 'Status:', volume.status

                print "\nType the number of the Volume to detach:"
                volume_num = self.ask_option(len(volumes))
                volume_id = volumes[volume_num-1].id

                # Detach and notify
                success = Volumes.detach_volume(conn_ec2, volume_id)
                if success:
                    print self.app_strings['detached']

            else:
                print "There are no detachable volumes"

        # AWS - Launch a new instance - Windows instance / Linux instance
        elif action == 1181 or action == 1182:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

            so = "windows" if action == 1181 else "linux"

            # Stop the running instance
            EC2Instance.create_instance_with_so(conn_ec2, so)

            print self.app_strings['created']

        # OS - List all running instances
        elif action == 121:

            # List All
            nodes = EC2InstanceOS.find_instances_running()

            if not nodes:
                print self.app_strings['no_running']
            else:
                # Format and print the requested information
                print "\nRunning AWS EC2 nodes"
                for index, node in enumerate(nodes):
                    self.print_node(index, node)

        # AWS - List all buckets
        elif action == 211:
            # Start a S3 connection
            conn_s3 = Connection.s3_connection()

            buckets = S3Bucket.list_buckets(conn_s3)
            if buckets:
                print "Current AWS S3 Buckets:"
                for b in buckets:
                    print "\n\t", b.name
            else:
                print self.app_strings['no_found']

        # AWS - List all objects in a bucket - Choose from list
        elif action == 2121:
            # Start a S3 connection
            conn_s3 = Connection.s3_connection()

            buckets = S3Bucket.list_buckets(conn_s3)
            if buckets:
                # Show and ask for the bucket
                print "Current AWS S3 Buckets:"
                for index, bucket in enumerate(buckets, 1):
                    print '\t', str(index) + ":", bucket.name

                print "\nType the number of the Bucket"
                bucket_num = self.ask_option(len(buckets))

                bucket_objects = buckets[bucket_num - 1].list()
                if bucket_objects:
                    for bucket_object in bucket_objects:
                        print '\t' + str(bucket_object.key)
                else:
                    print self.app_strings['no_found']
            else:
                print self.app_strings['no_found']

        # AWS - List all objects in a bucket - Enter a bucket name
        elif action == 2122:
            # Start a S3 connection
            conn_s3 = Connection.s3_connection()

            buckets = S3Bucket.list_buckets(conn_s3)
            if buckets:
                # Ask for the bucket name
                print "\nType the name of the Bucket"
                bucket_name = self.ask_custom_string("Type the name: ")

                success = False
                for bucket in buckets:
                    if bucket.name == bucket_name:
                        success = True
                        bucket_objects = bucket.list()
                        for bucket_object in bucket_objects:
                            print '\t' + str(bucket_object.key)

                        # If there are no files, warn the user
                        if not bucket_objects:
                            print self.app_strings['no_found']

                # If there is no bucket with that name, warn the user
                if not success:
                    print self.app_strings['no_found']
            else:
                print self.app_strings['no_found']

        # AWS - Upload / Download / Delete an object
        elif action == 213 or action == 214 or action == 215:
            # Start a S3 connection
            conn_s3 = Connection.s3_connection()

            buckets = S3Bucket.list_buckets(conn_s3)
            if buckets:
                # Show and ask for the bucket
                print "Current AWS S3 Buckets:"
                for index, bucket in enumerate(buckets, 1):
                    print '\t', str(index) + ":", bucket.name

                print "\nType the number of the Bucket"
                bucket_num = self.ask_option(len(buckets))

                bucket = buckets[bucket_num - 1]

                print "Type the identifier of the file"
                file_title = self.ask_string()

                if action == 213:
                    print "Type the location of the file (e.g. res/test.txt"
                    file_location = self.ask_custom_string("Type location: ")

                    S3Bucket.store_in_bucket(bucket, file_title, file_location)
                    print self.app_strings['stored']

                elif action == 214:
                    for key in bucket.list():
                        if key.name == file_title:
                            print "Downloading to res/\n"
                            key.get_contents_to_filename('res/' + key.name)
                            print self.app_strings['downloaded']

                else:
                    S3Bucket.delete_from_bucket(bucket, file_title)

                    print self.app_strings['removed']
            else:
                print self.app_strings['no_found']

        # OS - List all buckets
        elif action == 221:

            buckets = S3BucketOS.list_buckets()

            if buckets:
                print "Current OS S3 Buckets:"
                for b in buckets:
                    print "\n\t", b.name
            else:
                print self.app_strings['no_found']

        # OS - List all objects in a bucket - Choose from list
        elif action == 2221:

            buckets = S3BucketOS.list_buckets()

            if buckets:
                # Show and ask for the bucket
                print "\nCurrent OS S3 Buckets:"
                for index, bucket in enumerate(buckets, 1):
                    print '\t', str(index) + ":", bucket.name

                print "\nType the number of the Bucket"
                bucket_num = self.ask_option(len(buckets))

                bucket_objects = buckets[bucket_num - 1].list_objects()

                if bucket_objects:
                    for bucket_object in bucket_objects:
                        print '\t' + bucket_object.name
                else:
                    print self.app_strings['no_found']
            else:
                print self.app_strings['no_found']

        # OS - List all objects in a bucket - Enter a bucket name
        elif action == 2222:

            buckets = S3BucketOS.list_buckets()

            if buckets:
                # Ask for the bucket name
                print "\nType the name of the Bucket"
                bucket_name = self.ask_custom_string("Type the name: ")

                success = False
                for bucket in buckets:
                    if bucket.name == bucket_name:
                        success = True
                        bucket_objects = bucket.list_objects()
                        for bucket_object in bucket_objects:
                            print '\t' + bucket_object.name

                        # If there are no files, warn the user
                        if not bucket_objects:
                            print self.app_strings['no_found']

                # If there is no bucket with that name, warn the user
                if not success:
                    print self.app_strings['no_found']
            else:
                print self.app_strings['no_found']

        # OS - Upload / Download / Delete an object
        elif action == 223 or action == 224 or action == 225:

            buckets = S3BucketOS.list_buckets()
            if buckets:
                # Show and ask for the bucket
                print "Current OS S3 Buckets:"
                for index, bucket in enumerate(buckets, 1):
                    print '\t', str(index) + ":", bucket.name

                print "\nType the number of the Bucket"
                bucket_num = self.ask_option(len(buckets))

                bucket = buckets[bucket_num - 1]

                print "Type the identifier of the file"
                file_title = self.ask_string()

                if action == 223:
                    print "Type the location of the file"
                    file_location = self.ask_custom_string("Type location: ")

                    S3BucketOS.store_in_bucket(bucket, file_title, file_location)
                    print self.app_strings['stored']

                elif action == 224:
                    for key in bucket.list_objects():
                        if key.name == file_title:
                            print "Downloading to res/\n"
                            key.download('res/' + key.name)
                            print self.app_strings['downloaded']

                else:
                    for key in bucket.list_objects():
                        if key.name == file_title:
                            key.delete()
                            print self.app_strings['removed']
            else:
                print self.app_strings['no_found']

        # Performance metrics for a EC2 instance - Activate monitoring
        elif action == 311 or action == 312 or action == 32:
            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

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
                print "\nType the number of the id"
                index = self.ask_option(len(instances))

                instance = instances[index-1]

                if action == 311:
                    CloudWatch.enable_cw_on_instance(conn_ec2, str(instance.id))
                elif action == 312:
                    # New CW connection
                    conn_cw = Connection.cw_connection()

                    CloudWatch.query_cw_by_instance_id(str(instance.id), conn_cw)
                else:
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

                    # Create the alarm
                    print self.app_strings['creating_alarm']
                    success = CloudWatch.create_cw_alarm(instance.id, alarm_name, email_address, metric_name,
                                                         comparison, threshold, period, eval_periods, statistics)
                    if success:
                        print self.app_strings['created_alarm']
                    else:
                        print self.app_strings['failure_alarm']

        # AWS - List all Glacier Vaults
        elif action == 411:
            conn_glacier = Connection.glacier_connection()

            vaults = GlacierVaults.list_vaults(conn_glacier)

            if vaults:
                print "Active Vaults:"
                for index, vault in enumerate(vaults, 1):
                    print '\t' + str(index) + ':', 'Name:', vault.name, 'Size:', vault.size,\
                        'Created in:', vault.creation_date
            else:
                print self.app_strings['no_found']

        # AWS - Create / Delete a Glacier Vault
        elif action == 412 or action == 413:
            conn_glacier = Connection.glacier_connection()

            name = self.ask_custom_string("Type vault name: ")

            if action == 412:
                GlacierVaults.create_vault(conn_glacier, name)
                print self.app_strings['created_glacier']
            else:
                GlacierVaults.delete_vault(conn_glacier, name)
                print self.app_strings['deleted_glacier']

        # AWS - Auto Scale - Test connection
        elif action == 421:
            print "Testing connection:"

            print '\n\t', Connection.as_connection()

        # AWS - Auto Scale - Create Auto Scaling Group
        elif action == 422:
            conn_as = Connection.as_connection()

            launch_config_name = self.ask_custom_string("Type Launch Configuration name: ")
            as_group_name = self.ask_custom_string("Type Auto Scaling group name: ")

            min_inst = self.ask_custom_int("Type min instances (min 0, max 20)", 0, 20)
            max_inst = self.ask_custom_int("Type max instances (min " + str(min_inst) + " max 40)", min_inst, 40)

            success = AutoScale.create_as_group(conn_as, launch_config_name, as_group_name, min_inst, max_inst)
            if success:
                print self.app_strings['created_group']

        # AWS - Auto Scale - Delete Auto Scaling Group
        elif action == 423:

            conn_as = Connection.as_connection()
            launch_config_name = self.ask_custom_string("Type Launch Configuration name: ")
            as_group_name = self.ask_custom_string("Type Auto Scaling group name: ")

            success = AutoScale.delete_as_group(conn_as, as_group_name, launch_config_name)
            if success:
                print self.app_strings['deleted_group']

        # AWS - Auto Scale - Create policies
        elif action == 424:
            conn_as = Connection.as_connection()

            as_group_name = self.ask_custom_string("Type Auto Scaling group name: ")
            AutoScale.create_scale_policies(conn_as, as_group_name)

            print 'Policies', 'scale_up', 'and', 'scale_down', 'created'

        # AWS - Auto Scale - Create alarm
        elif action == 425:
            conn_as = Connection.as_connection()
            conn_cw = Connection.cw_connection()

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

            print self.app_strings['creating_alarm']
            success = AutoScale.create_scale_alarm(conn_as, conn_cw, as_group_name, alarm_name, scaling_policy_name,
                                                   metric_name, comparison, threshold, period, eval_periods, statistics)
            if success:
                print self.app_strings['created_alarm']

        # AWS - Exit -> Terminate all
        elif action == 43:
            print self.app_strings['terminating']

            # Start a EC2 connection
            conn_ec2 = Connection.ec2_connection()

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
            conn_glacier = Connection.glacier_connection()
            GlacierVaults.terminate_all_vaults(conn_glacier)
            print "\tTerminated"

            # Terminate all groups, launch configuration and policies
            print "\nTerminating groups, launch configuration and policies:\n"
            conn_as = Connection.as_connection()
            AutoScale.delete_everything(conn_as)
            print "\tTerminated"

            # Redirect to check, just in case
            print "\nRedirecting to amazon in 5 seconds, check manually!"
            sleep(5)
            webbrowser.open('https://eu-west-1.console.aws.amazon.com/ec2/v2/home?region=eu-west-1#')
            webbrowser.open('https://console.aws.amazon.com/s3/home?region=eu-west-1')
            webbrowser.open('https://eu-west-1.console.aws.amazon.com/glacier/home?region=eu-west-1')
            webbrowser.open(
                'https://eu-west-1.console.aws.amazon.com/ec2/autoscaling/home?region=eu-west-1#LaunchConfigurations:')
            webbrowser.open(
                'eu-west-1.console.aws.amazon.com/ec2/autoscaling/home?region=eu-west-1#AutoScalingGroups:view=details')

        # The action has been completed
        print self.app_strings['completed']

        # Restart the interface unless you are terminating all AWS instances/volumes/etc
        if action != 42:
            print self.app_strings['restart']
            self.process_selection(action // 10)
        else:
            print self.app_strings['terminated']

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
    def ask_custom_string(question):
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

    @staticmethod
    def print_node(index, node):
        result = "\t" + ("" if index == -1 else str(index) + ':')

        # Amazon Web Services
        # print result, node.id, '-', node.extra['instance_type'], '<' + node.extra['availability'] + \
        #                                                          '>: <Running since:', node.extra['launch_time'] + '>'

        # OpenStack

        # Calculate the machine type based on the flavorId
        flavours = {'1': "tiny", '2': "small", '3': "medium", '4': "large", '5': "x-large"}
        instance_type = "m1." + str(flavours[node.extra['flavorId']])

        print result, node.id, '-', instance_type, '<' + node.extra['availability_zone'] + '>: <Running since:', \
            node.extra['created'] + '>'
