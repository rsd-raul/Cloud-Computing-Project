# Cloud Computing Project w. Python

Description:

    This project objective is to learn how to control and manage Cloud Computing platforms such as Amazon
    Web Services or OpenStack based ones with Python. By using pre-developed scripts, administrator menus
    and automating processes we can precisely control and take advantage of the power of the cloud and
    the versatility and scalability it offers.

    As this is a education-oriented project, code will be explained for better comprehension.

Libraries:

    Boto to automate Amazon Web Services
    LibCloud to automate both OpenStack and Amazon Web Services (Driver based)

Setup:

    Download and install python:     https://www.python.org/downloads/

    Download boto:       https://github.com/boto/boto
    Download libcloud:   https://libcloud.apache.org/downloads.html
        *Follow the instructions or cd into both folders using cmd and execute "python setup.py install"

    Setup a boto.config file with exactly this variables (substitute when necessary):
            [Credentials]
            aws_access_key_id = <YOUR KEY ID>
            aws_secret_access_key = <YOUR ACCESS KEY>
            key_name = rsd_raul_cit_aws_key
            region = eu-west-1

            [Boto]
            cloudwatch_region_name = eu-west-1
            cloudwatch_region_endpoint = monitoring.eu-west-1.amazonaws.com
            autoscale_endpoint = autoscaling.eu-west-1.amazonaws.com
            sns_endpoint = sns.eu-west-1.amazonaws.com

            [LibCloud]
            username = <YOUR USERNAME>
            secret_key = <YOUR SECRET KEY>
            auth_url = http://128.136.179.2:5000

    Enter cmd, cd into the project folder and execute "python main.py"
        * A quick test will be shown to make sure boto.config is correctly setup

    Optionally:
        Import the project in you IDE of choice (Ideally PyCharm by JetBrains)
        Execute main.py (right click - Run)

Menus & actions:

    1	Compute
        1	AWS
            1	List all running instances
            2	List some of the running instances
                1 	Choose from list
                2 	Enter an instance ID
            3	Start a new instance based on an existing AMI
            4	Stop all instances
            5	Stop a specific instance
            6	Attach an existing volume to an instance
            7	Detach a volume from an instance
            8	Launch a new instance
                1 	Windows instance
                2 	Linux instance
            9	Create volume
        2	OpenStack
            1	List all running instances

    2	Storage
        1	AWS
            1	List all buckets
            2	List all objects in a bucket
                1 	Choose from list
                2 	Enter a bucket name
            3	Upload an object
            4	Download an object
            5	Delete an object
        2	OpenStack
            1	List all buckets
            2	List all objects in a bucket
                1 	Choose from list
                2 	Enter a bucket name
            3	Upload an object
            4	Download an object
            5	Delete an object

    3	Monitoring
        1 	Performance metrics for a EC2 instance
            1   Activate monitoring
            2   Get metrics
        2 	Set an alarm

    4  Extras
        1  Glacier Vaults Interface
            1   List Vaults
            2   Create Vault
            3   Delete Vault
        2   AutoScaling Interface
            1   Testing connection
            2   Create AutoScaling Group
            3   Delete AutoScaling Group
            4   Create Scaling policies (up and down)
            5   Create Alarm
        3   Terminate *warning

Disclaimer:

    To maintain the method count as small as possible and at the same time to avoid code duplication, the
    method apply_action will not be split down in small parts, while I understand the elevated number of
    lines, I think it will be much worse to isolate each and every one of the methods in its of function.

    This project is based and tested against AWS eu-west-1 regions, while other regions are very likely
    to behave correctly, this is not warranted or directly supported by the developer.

    The "Terminate" method located under "Extras" shuts down any instances, volumes, vaults, auto scale
    groups, launch configurations and policies associated with the active AWS account and cannot be
    undone.