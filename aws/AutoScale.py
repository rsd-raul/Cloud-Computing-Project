from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.cloudwatch import MetricAlarm
from boto import exception
from time import sleep


class AutoScale:

    def __init__(self):
        """ AutoScale Instance """

    @staticmethod
    def create_as_group(conn_as, launch_config_name, as_group_name, min_instances, max_instances):

        lc = LaunchConfiguration(name=launch_config_name, image_id='ami-c6972fb5', instance_type='t2.micro',
                                 key_name='rsd_raul_cit_aws_key',
                                 security_groups=[])

        conn_as.create_launch_configuration(lc)
        print "Launch configuration created"

        ag = AutoScalingGroup(group_name=as_group_name, availability_zones=['eu-west-1c'], launch_config=lc,
                              min_size=min_instances, max_size=max_instances, connection=conn_as)
        print "Auto Scaling Group created"

        conn_as.create_auto_scaling_group(ag)
        print "Instances are being deployed"

        return True

    @staticmethod
    def create_scale_policies(conn_as, as_group_name):
        from boto.ec2.autoscale import ScalingPolicy

        scale_policy_up = ScalingPolicy(name='scale_up', adjustment_type='ChangeInCapacity',
                                        as_name=as_group_name, scaling_adjustment=1, cooldown=180)
        scale_policy_down = ScalingPolicy(name='scale_down', adjustment_type='ChangeInCapacity',
                                          as_name=as_group_name, scaling_adjustment=-1, cooldown=180)

        conn_as.create_scaling_policy(scale_policy_up)
        conn_as.create_scaling_policy(scale_policy_down)

        print "Scale policies submitted"

    @staticmethod
    def create_scale_alarm(conn_as, conn_cw, as_group_name, alarm_name, scaling_policy_name='scale_up',
                           metric_name='CPUUtilization', comparison='>', threshold=70, period=60, eval_periods=2,
                           statistics='Average'):
        alarm_dimensions = {"AutoScalingGroupName": as_group_name}

        scaling_policy = conn_as.get_all_policies(as_group=as_group_name, policy_names=[scaling_policy_name])[0]
        if not scaling_policy:
            print "Scaling policy", scaling_policy_name, "not found"
            return False

        scale_up_alarm = MetricAlarm(name=alarm_name, namespace='AWS/EC2', metric=metric_name, statistic=statistics,
                                     comparison=comparison, threshold=threshold, period=period,
                                     evaluation_periods=eval_periods, alarm_actions=[scaling_policy.policy_arn],
                                     dimensions=alarm_dimensions)
        print "Alarm created"
        conn_cw.create_alarm(scale_up_alarm)

        return True

    @staticmethod
    def delete_as_group(conn_as, as_group_name, launch_config_name):

        try:
            print "Deleting AutoScaling Group"
            conn_as.delete_auto_scaling_group(as_group_name, True)

            print "Deleting Launch Configurator"
            sleep(5)
            conn_as.delete_launch_configuration(launch_config_name)

            return True
        except exception.BotoServerError:
            print "You cannot delete an Auto Scaling Group while there are instances still in the group."
            print "Try again later"
            return False

    @staticmethod
    def delete_everything(conn_as):

        for group in conn_as.get_all_groups():
            conn_as.delete_policy('scale_up', group.name)
            conn_as.delete_policy('scale_down', group.name)
            group.delete(True)

        for launch_config in conn_as.get_all_launch_configurations():
            launch_config.delete()


