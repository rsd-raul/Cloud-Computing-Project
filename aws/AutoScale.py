from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.autoscale import ScalingPolicy
from boto.ec2.cloudwatch import MetricAlarm
from boto import config
from boto import exception
from time import sleep


class AutoScale:

    def __init__(self):
        """ AutoScale Instance """

    @staticmethod
    def create_as_group(conn_as, launch_config_name, as_group_name, min_instances, max_instances):
        """ This method is tasked with the creation of both a Launch Configuration and an Auto Scaling Group
        based on the user requested names and features"""

        try:
            # Here we create the Launch configuration (a "how to" for the auto scaling group to start its instances)
            # and select from the constructor the values we need or want to use, in this case, we will hard-code
            # the ami and the instance type with free tier instances, we will retrieve from boto the AWS key_name
            # so anyone can use the interface without having to hard-code it.
            lc = LaunchConfiguration(name=launch_config_name, image_id='ami-c6972fb5', instance_type='t2.micro',
                                     key_name=config.get('Credentials', 'key_name'), security_groups=[])

            # Once created the launch configuration it's time to commit the configuration to AWS
            conn_as.create_launch_configuration(lc)
            print "Launch configuration created"

            # Then we move on to the AutoScaling group creation, group that includes the previously created launch
            # config as this launch configuration will contain the instructions to create new instances for the group.
            # Other than that, we include the availability zones for the group to launch on. Load Balancer along with
            # a number of extra options can be used in the Auto Scaling Group.
            ag = AutoScalingGroup(group_name=as_group_name, availability_zones=['eu-west-1c'], launch_config=lc,
                                  min_size=min_instances, max_size=max_instances, connection=conn_as)
            print "Auto Scaling Group created"

            # Once again, we will commit the created group and as a result, the minimum number of instances requested
            # will start to deploy.
            conn_as.create_auto_scaling_group(ag)
            print "Instances are being deployed"
        except exception.BotoServerError:
            print "The launch configurator name or the group name already exists"

        return True

    @staticmethod
    def create_scale_policies(conn_as, as_group_name):
        """ This method will create the Auto Scale Policies for a certain Auto Scaling Group, in this case we will
        hard-code two predefined policies, policies who will increment or decrement (by 1 or -1) the number of instances
        in the group. This policies are the ones tasked with handling how many and how often the instances will be
        launched, but they will not trigger the scaling, the alarms will handle that bit """

        try:
            # We create both policies (up and down) associated to the group and with a custom cooldown and scaling
            scale_policy_up = ScalingPolicy(name='scale_up', adjustment_type='ChangeInCapacity',
                                            as_name=as_group_name, scaling_adjustment=1, cooldown=180)
            scale_policy_down = ScalingPolicy(name='scale_down', adjustment_type='ChangeInCapacity',
                                              as_name=as_group_name, scaling_adjustment=-1, cooldown=180)

            # Once the alarms are created, we push them to AWS
            conn_as.create_scaling_policy(scale_policy_up)
            conn_as.create_scaling_policy(scale_policy_down)
            print 'Policies', 'scale_up', 'and', 'scale_down', 'submitted for the group:', as_group_name

        # If an exception is raised, notify the user
        except exception.BotoServerError:
            print "The typed AutoScaling Group does not exists"

    @staticmethod
    def create_scale_alarm(conn_as, conn_cw, as_group_name, alarm_name, scaling_policy_name='scale_up',
                           metric_name='CPUUtilization', comparison='>', threshold=70, period=60, eval_periods=2,
                           statistics='Average'):
        """ This method will be the responsible for establishing an alarm, alarm that will trigger one of the predefined
        policies for the Auto Scaling Group when a certain condition is met, all the parameters will be customizable """

        try:
            # Now we create the alarm dimensions, in this case, the alarm will apply the metric over the whole group
            # instead of over each of the instances
            alarm_dimensions = {"AutoScalingGroupName": as_group_name}

            # We recover the scaling policy the user decided to use, and warn the user if a warning was thrown
            scaling_policy = conn_as.get_all_policies(as_group=as_group_name, policy_names=[scaling_policy_name])[0]
            if not scaling_policy:
                print "Scaling policy", scaling_policy_name, "not found"
                return False

            # Now we create the metric based alarm and pass the parameters the user choose in the menu
            scale_up_alarm = MetricAlarm(name=alarm_name, namespace='AWS/EC2', metric=metric_name, statistic=statistics,
                                         comparison=comparison, threshold=threshold, period=period,
                                         evaluation_periods=eval_periods, alarm_actions=[scaling_policy.policy_arn],
                                         dimensions=alarm_dimensions)

            # Once the alarm is created, we push the alarm to AWS for it to work.
            conn_cw.create_alarm(scale_up_alarm)
            print "Alarm created"
            return True

        # If an exception has been thrown, we advice the user to try again.
        except exception.BotoServerError:
            print "One or more of the fields typed are incorrect, \n" \
                  "Have you created the policies?? \n" \
                  "please, try again and follow instructions."
            return False

    @staticmethod
    def delete_as_group(conn_as, as_group_name, launch_config_name):
        """ This is method will be tasked with the responsibility of shutting down all group-associated instances
        and to delete both the launch configuration and the auto scaling group itself """

        try:
            # Here we request the deletion of the group and indicate via a boolean value that all instances associated
            # with this group must be killed, otherwise, AWS cannot let the user delete a Group if any of its instances
            # are running or starting.
            print "Deleting AutoScaling Group\n"
            conn_as.delete_auto_scaling_group(as_group_name, True)

            # We wait a few seconds to ensure the AutoScaling Group is being commanded to shut down, and then
            # terminate the launch configurator previously associated with the group.
            print "Deleting Launch Configurator\n"
            sleep(5)
            conn_as.delete_launch_configuration(launch_config_name)

            # We will also try to delete any auto scale policy associated with the group (in this case up and down)
            try:
                print "Deleting policies"
                conn_as.delete_policy('scale_up', as_group_name)
                conn_as.delete_policy('scale_down', as_group_name)
            # If there are no associated policies, notify the user and continue (not an error)
            except exception.BotoServerError:
                print "\tNo policies to delete"

            return True

        # If the Auto Scaling Group or the Launch Configurator names are incorrect, warn the user
        except exception.BotoServerError:
            print "The required Auto Scaling Group or Launch Configuration doesn't exist"
            return False

    @staticmethod
    def delete_everything(conn_as):
        """ This is a secondary method whose objective is to delete all auto scaling groups and launch configurators """

        # We retrieve and iterate over all the groups, delete it's policies and the group itself
        for group in conn_as.get_all_groups():
            conn_as.delete_policy('scale_up', group.name)
            conn_as.delete_policy('scale_down', group.name)
            group.delete(True)

        # Then we retrieve and once again iterate over the launch configurations in order to delete them
        for launch_config in conn_as.get_all_launch_configurations():
            launch_config.delete()
