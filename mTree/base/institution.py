class Institution:
    def __init__(self, environment, name=None):
        self.environment = environment  # environment in which the institution is invoked
        self.recorder = self.environment.recorder
        self.id = None             # id for the institution - what should this be?
        self.name = name           # name for the institution
        self.event_registry = {}   # events registered for the institution
        self.player = None         # for a single-person institution
        self.players = {}          # for a multi-person institution
        self.player_object = None  # the player object used in the institution
        self.open = True           # could possibly be used as a flag for accepting available players

        # self.recorder("INSTITUTION", self.__class__.__name__)

        self.initializer()

    def initializer(self):
        pass

    def set_name(self, name):
        self.name = name  # Normal Form Game, Double Auction, etc.

    def set_player_object(self, player_object):
        self.player_object = player_object

    def set_player(self, player):
        if type(player) is tuple:
            player = player[0]  # correct the tuple passing from set_players()
        self.player = player

    def set_players(self, *players):
        if len(players) == 1:
            self.set_player(players)
        else:
            for player in players:
                self.players[player.id] = player

    def register_event(self, event_id, event_method):
        """
        Used to register events that are triggered on the subject interface
        :param event_id: string of the event id found in the html
        :param event_method: associated event method
        :return:
        """
        self.event_registry[event_id] = event_method

    def receive_event(self, event_id, event_data=None):  # methods must have a default parameter that can be set to None
        if event_id in self.event_registry.keys():
            method = self.event_registry[event_id]
            method(event_data)

    def start(self):  # this might be unnecessary
        self.start_institution()

    def start_institution(self, debug=False):
        if debug: print("WARNING: You have not defined start_institution()")
        pass

    def close_institution(self, debug=False):
        if debug: print("Closing Institution")
        if not self.players:  # single-player institution
            self.player.close()
        elif self.players:    # multi-player institution
            for player in self.players.keys():
                self.players[player].close()
        self.environment.run()
        pass

    def record(self, *args):
        output = ",".join(str(arg) for arg in args)
        self.recorder(self.__class__.__name__, output)
