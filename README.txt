# Cloud-Computing-Project

Boto to automate Amazon Web Services
LibCloud to automate OpenStack and Amazon Web Services (Driver based)

Supported options (X means Active and Tested):

1X	Compute
	1X	AWS
		1X	List all running instances
		2X	List some of the running instances
			1X 	Choose from list
			2X 	Enter an instance ID
		3X	Start a new instance based on an existing AMI
		4X	Stop all instances
		5X	Stop a specific instance
		6X	Attach an existing volume to an instance
		7X	Detach a volume from an instance
		8X	Launch a new instance
			1X 	Windows instance
			2X 	Linux instance
		9X	Create volume
	2X	OpenStack
		1X	List all running instances
2X	Storage
	1X	AWS
		1X	List all buckets
		2X	List all objects in a bucket
			1X 	Choose from list 	
			2X 	Enter a bucket name
		3X	Upload an object
		4X	Download an object
		5X	Delete an object
	2X	OpenStack
		1X	List all buckets
		2X	List all objects in a bucket
			1X 	Choose from list
			2X 	Enter a bucket name
		3X	Upload an object
		4X	Download an object
		5X	Delete an object
3X	Monitoring
	1X 	Performance metrics for a EC2 instance
	    1X   Activate monitoring
   	    2X   Get metrics
	2X 	Set an alarm

4  Extras
    1   Create Glacier Vault
    2   Terminate *warning

*Terminate shuts down any instances and any volumes associated with the account (key, access), it cannot be undone.