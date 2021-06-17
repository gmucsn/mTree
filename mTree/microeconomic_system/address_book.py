from mTree.microeconomic_system.message import Message
import uuid

class AddressBook:
    def __init__(self, base_component):
        self.base_component = base_component
        self.addresses = {}
        self.address_groups = {}
        self.addresses_to_groups = {}


    def get_addresses(self):
        return self.addresses
        
    def reset_address_groups(self):
        self.address_groups = {}
        self.addresses_to_groups = {}
        
    def create_address_group(self, name=None):
        if name is None:
            name = str(uuid.uuid4())
        
        self.address_groups[name] = []
        
        return name

    def add_address_to_group(self, groupname, address, role=None):
        if groupname not in self.address_groups.keys():
            raise Exception("Groupname must be created before adding addresses")
        self.address_groups[groupname].append(address)
        self.addresses_to_groups[address["address"]] = groupname
    
    def remove_address_from_group(self, groupname, address):
        if groupname not in self.address_groups.keys():
            raise Exception("Groupname must be created before removing addresses")
        if address not in self.address_groups[groupnames]:
            raise Exception("Address must be in group before removing it")
        address_index = self.address_groups[groupname].index(address)
        self.address_groups[groupname].pop(address_index)
        self.addresses_to_groups.pop(address["address"])
    

    def get_all_groups(self):
        return self.address_groups.items()


    def add_address(self, address, additional_information=None):
        address_str = str(address)
        self.addresses[address_str] = additional_information

    def select_addresses(self, selector):
        address = []
        if "short_name" in selector.keys():
            address = [entry for entry in self.addresses.values() if entry["short_name"] == selector["short_name"]]
        elif "address_type" in selector.keys():
            address = [entry for entry in self.addresses.values() if entry["address_type"] == selector["address_type"]]
        
        if len(address) == 1:
            return address[0]["address"]
        return address

    def update_addresses(self, addresses):
        self.addresses = addresses

    def merge_addresses(self, addresses):
        self.addresses = addresses
        

    def delete_address(self, address):
        pass

    def label_address(self, address, label):
        pass

    def remove_label(self, address, label):
        pass

    def add_information(self, address, information):
        pass

    def broadcast_message(self, selector, message):
        addresses = self.select_addresses(selector)
        for address in addresses:
            self.base_component.send(address["address"], message)  


    def add_address_group(self, group_name, addresses):
        pass

    def remove_address_group(self, group_name, addresses):
        pass

    def forward_address_book(self, address):
        new_message = Message()
        new_message.set_sender(self.base_component.myAddress)
        new_message.set_directive("address_book_update")
        new_message.set_payload(self.addresses)
        #address = self.select_addresses(selector)
        self.base_component.send(address, new_message)  

    def forward_address_book_message(self, selector=None):
        new_message = Message()
        new_message.set_sender(self.base_component.myAddress)
        new_message.set_directive("address_book_update")
        new_message.set_payload(self.addresses)
        return new_message
        #address = self.select_addresses(selector)
        #self.base_component.send(address, new_message)  
