class CommunicationMixin:
    def send_message(self, directive, receiver, payload=None):
        """Send message
           Constructs and sends a message inside the system """
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive(directive)
        if payload is not None:
            new_message.set_payload(payload)
    
        if isinstance(receiver, list):
            for target_address in receiver:
                self.send(target_address, new_message)
        else:
            receiver_address = self.address_book.select_addresses(
                                {"short_name": receiver})
            logging.info("SHOULD BE GETTING THE ADDRESS")
            logging.info(self.address_book.addresses)
            logging.info("---> " + str(receiver_address))
            self.send(receiver_address, new_message)


    def send(self, targetAddress, message):
        if hasattr(self, 'short_name') and type(message) is Message:
            try:
                message.set_short_name(self.short_name)
            except:
                message.set_short_name(self.__class__.__name__)

        if isinstance(message, Message):
            self.log_message("Institution (" + self.short_name + ") : sending to "  + " directive: " + message.get_directive())
        super().send(targetAddress, message)