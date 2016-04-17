from Connections import Connection


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

    @staticmethod
    def create_cw_alarm(instance_id, alarm_name, email_address, metric_name, comparison, threshold, period,
                        eval_periods, statistics):

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

        instance = rs[0].instances[0]
        instance.monitor()

        # Create the SNS Topic
        topic_name = 'CWAlarm-%s' % alarm_name
        print 'Creating SNS topic: %s' % topic_name

        response = conn_sns.create_topic(topic_name)
        topic_arn = response['CreateTopicResponse']['CreateTopicResult']['TopicArn']
        print 'Topic ARN: %s' % topic_arn

        # Subscribe the email addresses to SNS Topic
        print 'Subscribing %s to Topic %s' % (email_address, topic_arn)
        conn_sns.subscribe(topic_arn, 'email', email_address)

        # Now find the Metric we want to be notified about
        metric = conn_cw.list_metrics(dimensions={'InstanceId': instance_id}, metric_name=metric_name)[0]
        print 'Found: %s' % metric

        # Now create Alarm for the metric
        print '\nFinalizing creation (hold)'
        alarm = metric.create_alarm(alarm_name, comparison, threshold, period, eval_periods, statistics,
                                    alarm_actions=[topic_arn], ok_actions=[topic_arn])
        if alarm:
            return True
        else:
            return False
