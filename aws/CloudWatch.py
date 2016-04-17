import datetime


class CloudWatch:

    def __init__(self):
        """ Volumes Constructor """

    @staticmethod
    def enable_cw_all(conn_ec2):
        """Enable CloudWatch monitoring on all running instances."""

        list_inst_ids = []                                          # Create list of instance IDs
        reservations = conn_ec2.get_all_instances()                 # Get information on currently running instances
        instances = [i for r in reservations for i in r.instances]  # Create list of instances
        for instance in instances:                                  # For loop checks for instance in list of instances
            if instance.state == u'running':                        # If instance state is equals to running
                list_inst_ids.append(instance.id)                   # Append instance ID to the list of instance IDs

        if list_inst_ids:
            inst_mon = conn_ec2.monitor_instances(list_inst_ids)
            print "Monitoring the instances: ", inst_mon
        else:
            print "No instances to monitor"

    @staticmethod
    def enable_cw_on_instance(conn_ec2, instance_id):
        """Enable CloudWatch monitoring a running instance."""

        found = False
        # reservations = conn.get_all_instances()                     # Get information on currently running instances
        # instances = [i for r in reservations for i in r.instances]  # Create list of instances
        for reservation in conn_ec2.get_all_instances():
            for instance in reservation.instances:
                if instance.id == instance_id and instance.state == u'running':
                    found = True

        if found:
            inst_mon = conn_ec2.monitor_instances(instance_id)
            print "Monitoring the instance: ", inst_mon
        else:
            print "No instances to monitor"

    @staticmethod
    def query_cw_by_instance(instance, conn_cw):
        """ Query CloudWatch for data about your instance"""
        metrics = conn_cw.list_metrics()
        my_metrics = []
        for metric in metrics:
            if 'InstanceID' in metric.dimensions:
                if instance.id in metric.dimensions['InstanceId']:
                    my_metrics.append(metric)

        print my_metrics

    @staticmethod
    def query_cw_by_instance_id(instance_id, conn_cw):
        """ Query CloudWatch for data about your instance"""
        # metrics = conn_cw.list_metrics()
        # my_metrics = []
        # for metric in metrics:
        #     if u'InstanceID' in metric.dimensions:
        #         if instance_id in metric.dimensions['InstanceId']:
        #             print "Instance metric found"
        #             my_metrics.append(metric)

        my_metrics = conn_cw.list_metrics(dimensions={'InstanceId': instance_id})

        print my_metrics

    # @staticmethod
    # def cw_alarm(instance):
    #     """ Setup a CW alarm to send a notification - Assume you have CW enabled, you want to be notified when certain conditions
    #     arise. This make use of the Simple Notification Service (SNS) to send an email of CW events using alarms"""
    #     sns = boto.connect_sns()
    #     sns.create_topic


def get_metric(date, metrics):
    """
    Get the statistics for 1 or more metrics at a given moment.
    The metric will request the statistics from 18 hours before
    the date argument until the date argument. (18h is to make
    sure at least 1 datapoint is returned).
    Return: a dict with the metric name as key and the value.
    """
    stats = {}
    start = date - datetime.timedelta(hours=18)
    # print 'Retrieving statistics from %s to %s.\n' % (start, date)
    for metric in metrics:
        if u'ServiceName' in metric.dimensions:
            datapoints = metric.query(start, date, 'Maximum')
            datapoints = sorted(datapoints, key=lambda datapoint: datapoint[u'Timestamp'], reverse=True)
            stats[metric.dimensions[u'ServiceName'][0]] = (datapoints[0])[u'Maximum']
    return stats