# Release Notes

## Reminder

To get a new Docker Image: docker pull mtree/mtree:1.0.11c

## mTree - 1.0.113 - Docker Image

Fixes:
    -Add check_status in mTree_runner to get list of running simulations
    -Fix simulation runner to run total of run number
    -Update logger so that individual runs result in individual log files
    -Include new logging statement for entry and exit of a directive
        -will be configurable eventually
    -Include basic websocket actor to use for ui routing

## Reminder

To get a new Docker Image: docker pull mtree/mtree:1.0.11e

## mTree - 1.0.11d - Docker Image

Fixes:
    -Add check_status in mTree_runner to get list of running simulations
    -Fix simulation runner to run total of run number
    -Update logger so that individual runs result in individual log files
    -Include new logging statement for entry and exit of a directive
        -will be configurable eventually
    -Include basic websocket actor to use for ui routing

## Reminder

To get a new Docker Image: docker pull mtree/mtree:1.0.11d

## mTree - 1.0.11c - Docker Image

Fixes:
    -Add check_status in mTree_runner to get list of running simulations
    -Fix simulation runner to run total of run number
    -Update logger so that individual runs result in individual log files
    -Include new logging statement for entry and exit of a directive
        -will be configurable eventually
    -Include basic websocket actor to use for ui routing

## Reminder

To get a new Docker Image: docker pull mtree/mtree:1.0.11b

## mTree - 1.0.11b - Docker Image

Fixes:
    -Update all packages
    -include sympy in container
    -fix Docker Container launch issue


## Reminder

To get a new Docker Image: docker pull mtree/mtree:1.0.11a

## mTree - 1.0.11a - Docker Image

Fixes:
    -Add check_status in mTree_runner to get list of running simulations
    -Fix simulation runner to run total of run number
    -Update logger so that individual runs result in individual log files
    -Include new logging statement for entry and exit of a directive
        -will be configurable eventually
    -Include basic websocket actor to use for ui routing

## Reminder

To get a new Docker Image: docker pull mtree/mtree:1.0.10

## mTree - 1.0.10 - Docker Image

Fixes:
    -Check reminder for type. Can support either a timedelta or an int representing seconds


## Reminder

To get a new Docker Image: docker pull mtree/mtree:1.0.9

## mTree - 1.0.9 - Docker Image

Fixes:
    -Changes to mTree runner startup. Extraneous messages suppressed now.

Additions:
    -the `mTree_runner` command is now entered by itself and no longer requires specifying a configuration
        You must simply run this command in a directory containing an MES
    -Multi-config running - When you enter the mTree_runner type `run_simulation` as before, but now
        you will be presented with a menu of known config files. You can use the up and down arrow to 
        select which configurations you would like to run. You can run one or many configurations at once
    -New agent sleep capability.
        Previously, the wakeupAfter method was recommended.
        This was confusing to users as people were unaware of whether it put the actor to sleep or not and whether
        or not the actor would continue to receive messages in the interim.
        Now, the recommended way of sending messages that will be executed in the future is the `reminder` method.
        This method can be invoked in an agent, environment, or institution. There are two required parameters and 
        a third optional parameter
            seconds_to_reminder - required - simply specify in how many seconds you want the agent to recive this message
            message - required - This will be the message delivered to the directive specified
            addresses - optional - This paramter can include a list of other agents, environments, or institutions that 
                have a reminder. Note, when invoked this will send a reminder to only those actors mentioned in the addresses list.
                Thus, the actor originating the reminder will not have remidner sent to itself.
        To be clear, when this method is invoked it will simply send a message to itself at the time specified. The actor should
        continue to operate as usualy. The only difference is that when the time comes, the reminder message will be sent and received.
    -Log file name output changes
        Previously, the log file names simply included the timestamp of when the simulation ran and what type of log file it was.
        In this version, log files will have the config file that is used to run the MES that is producing the log. Thus, if you config 
        file is "basic_agent_cva_auction.json" the log file associated with running that MES will be 
        "basic_agent_cva_auction-2021_08_24-10_05_31_PM-experiment.log".
    -Backend improvements
        There are several backend improvements meant to be used for intercommunication with external processes using websockets as well

## Reminder

To get a new Docker Image: docker pull mtree/mtree:1.0.8

## mTree - 1.0.8 - Docker Image

Fixes:
    -Display error type and error info along with new output

Additions:
    -AddressBook allows for lookup of address information from the thespian address
        use the AddressBook's get_from_address method
            This will return None, if no such address is stored
        agent_short_name = self.address_book.get_from_address(address)
    -Added environment directive to shutdown mes
        Send a message with the directive shutdown_mes to the environment
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("shutdown_mes")  # Set the directive
        self.send(self.environment_address, new_message)

## Reminder

To get a new Docker Image: docker pull mtree/mtree:1.0.7

## mTree - 1.0.7 - Docker Image

Fixes:
    -Server issues related to directory targets

## Reminder

To get a new Docker Image: docker pull mtree/mtree:1.0.6

## mTree - 1.0.6 - Docker Image

Fixes:
    -Display error type and error info along with new output

Additions:
    -Added broadcast_message_to_group
        Use like address_book.broadcast_message_to_group(group, message)

## Reminder

To get a new Docker Image: docker pull mtree/mtree:1.0.5

## mTree - 1.0.5 - Docker Image

Fixes:
    -Updates to fix bug in select_addresses in the address book

Additions:
    -improved stack trace information in logs
    -Addition of get_agents, get_institutions, num_agents, num_institutions in the address book

## Reminder

To get a new Docker Image: docker pull mtree/mtree:1.0.4

## mTree - 1.0.4 - Docker Image

Fixes:
    -Broadcast to one or multiple addresses should  be fixed now
    -Allow for MES or mes as the directory name containing code.

Additions:
    -mTree allows for multiple institutions
        -To use multiple insititutions modify your configuration to include something like the following:
        "institutions": [{"institution": "institution_1.Institution1"},{"institution": "institution_2.Institution2"}] ,
        -You will need to think about how your institutions are activated in your start_environment directive handler
    -You can identify the shortname of agents and institutions by looking at the self.short_name property
    -Logs start with a printout of the applicable configuration file


## Reminder

To get a new Docker Image: `docker pull mtree/mtree:1.0.3`

## mTree - 1.0.3- Docker Image

Fixes:
    -mTree runner should allow for multiple runs
        -There is an additional issue we are looking at as well that might still crop up
    -changes to group information in the address book to support trust games better

Additions:
    -Improved exception logging. Should provide additional detail and also include details previously omitted.

## mTree - 1.0.2 - Docker Image

Fixes:
    -Fixes issues with WakeupMessages not being delivered to mTree MES Components

Additions:
    -Provided additional methods to AddressBook to allow for group creation, member addition/removal, and group reset
    -Provided mechanisms to access simulation properties in all mTree MES Components
    -Provided mechanism to allow for having log_data to produce json lines output
        In order to write json data logs, ensure that you add the following to you json configuration file:
            `"data_logging": "json"`
        This will allow you to submit python dictionaries to your log_data method and it will be written out as a json line
        If you don't provide a dictionary, it will write the message to a json object with the message in the content field
        All json output will include a timestamp field that contains the timestamp from log message creation