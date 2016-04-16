# Cloud-Computing-Project
Boto/LibCloud to automate AWS related tasks w/ OpenStack

Supported options:

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
2	Storage
	1X	AWS
		1X	List all buckets
		2X	List all objects in a bucket
			1X 	Choose from list 	
			2X 	Enter a bucket name
		3X	Upload an object
		4X	Download an object
		5X	Delete an object
	2	OpenStack
		1X	List all buckets
		2	List all objects in a bucket
			1X 	Choose from list
			2 	Enter a bucket name
		3	Upload an object
		4	Download an object
		5	Delete an object
3	Monitoring
	1 	Performance metrics for a EC2 instance
	2 	Set an alarm
