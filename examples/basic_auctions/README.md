# mTree Basic Auction Tutorial - Step 8

In this Step you'll be working on improving the agents bidding procedure. In the current implementation the agents simply bid the value they are presented. You'll want to consider different bidding strategies that could range from randomly selecting a value to remembering bid history to always bidding as low as possible. The project here will follow the same steps as you did with modifying the institution. You'll copy hte agent file and then you'll modify the make_bid method to whatever you like. Finally, you'll modify the configuration file. 

You might want to create several copies of your configuration file. In you're configuration file you'll be able to add multiple agent types and numbers to your simulation and see how they perform against each other or other types of agents.

Specifically, you'll modify this line of your configuration: `"agents": [{"agent_name": "basic_auction_agent.AuctionAgent", "number": 5}]`. Inside the list, you can add more dictionaries with the agent name of your new agent and how many you would like to participate in the simulation. You might try different combinations of agents to see what results you get.

Now you should be able to run your new MES. 

Since you also have different institutions, you might also consider varying your agent and institutions to see what overall effects things have.

