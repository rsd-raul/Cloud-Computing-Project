from Connections import Connection
import datetime


class CloudWatch:

    def __init__(self):
        """ Volumes Constructor """

    @staticmethod
    def enable_cw_all(conn_ec2):
        """Enable CloudWatch monitoring on all running instances."""

        # Get all the reservations
        reservations = conn_ec2.get_all_instances()

        # Retrieve all the instances for all the reservations
        instances = [i for r in reservations for i in r.instances]

        # Iterate over all the instances and save the id of those who are running
        list_inst_ids = []
        for instance in instances:
            if instance.state == u'running':
                list_inst_ids.append(instance.id)

        # If there are instances running, activate monitoring for each one of them by passing the full id list
        if list_inst_ids:
            inst_mon = conn_ec2.monitor_instances(list_inst_ids)
            print "Monitoring the instances: ", inst_mon

        # If there aren't, notify the user
        else:
            print "No instances to monitor"

    @staticmethod
    def enable_cw_on_instance(conn_ec2, instance_id):
        """Enable CloudWatch monitoring on a running instance."""

        found = False

        # Retrieve all the instances for all the reservations and find the desired one by id (must also be running)
        for reservation in conn_ec2.get_all_instances():
            for instance in reservation.instances:
                if instance.id == instance_id and instance.state == u'running':
                    found = True

        # If found, activate the monitoring for the instance
        if found:
            inst_mon = conn_ec2.monitor_instances(instance_id)
            print "Monitoring the instance: ", inst_mon
        # Otherwise, notify the user
        else:
            print "No instances to monitor"

    @staticmethod
    def query_cw_by_instance_id(instance_id, conn_cw):
        """ Query CloudWatch for data about your instance"""

        # Request the metrics for the desired instance
        my_metrics = conn_cw.list_metrics(dimensions={'InstanceId': instance_id})

        print "All this metrics can be obtained:"
        print my_metrics

        # Also, you can request the data with a time frame and for a specific statistic
        print "Some of them are:"
        for stat in ["DiskReadBytes", "DiskWriteBytes", "DiskReadOps", "DiskWriteOps", "CPUUtilization"]:
            print "\n" + stat + ":"
            st = conn_cw.get_metric_statistics(300, datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
                                               datetime.datetime.utcnow(), stat, 'AWS/EC2', 'Average',
                                               dimensions={'InstanceId': [instance_id]})
            print st

    @staticmethod
    def create_cw_alarm(instance_id, alarm_name, email_address, metric_name, comparison, threshold, period,
                        eval_periods, statistics):
        """ Create an alarm to email the user in case the conditions set by him are met """

        print "Starting alarm creation process\n"

        # Create connections to the required services
        conn_ec2 = Connection.ec2_connection()
        conn_sns = Connection.sns_connection()
        conn_cw = Connection.cw_connection()

        # Make sure the instance in question exists and is being monitored with CloudWatch.
        rs = conn_ec2.get_all_instances(instance_id)
        if len(rs) != 1:
            print 'Unable to find instance:', instance_id
            return False

        # As the instance id is unique, the rs list will contain only one instance
        instance = rs[0].instances[0]
        instance.monitor()

        # Build the name and start the topic creation process
        topic_name = 'CWAlarm-%s' % alarm_name
        print 'Creating SNS topic: %s' % topic_name

        # Create the SNS Topic and recover the necessary parameters from the response
        response = conn_sns.create_topic(topic_name)
        topic_arn = response['CreateTopicResponse']['CreateTopicResult']['TopicArn']
        print 'Topic ARN: %s' % topic_arn

        # Subscribe the email addresses to SNS Topic
        print 'Subscribing %s to Topic %s' % (email_address, topic_arn)
        conn_sns.subscribe(topic_arn, 'email', email_address)

        # We find the Metric we want to be notified about
        metric = conn_cw.list_metrics(dimensions={'InstanceId': instance_id}, metric_name=metric_name)[0]
        print 'Found: %s' % metric

        # And then create Alarm for the metric
        print '\nFinalizing creation (hold)'
        alarm = metric.create_alarm(alarm_name, comparison, threshold, period, eval_periods, statistics,
                                    alarm_actions=[topic_arn], ok_actions=[topic_arn])

        # Control the result of the creation for the app to react accordingly
        if alarm:
            return True
        else:
            return False
