from dataclasses import dataclass


@dataclass
class StartupPayload:
    startup_payload: dict


@dataclass
class AddressBookPayload:
    address_book_payload: dict


@dataclass
class MESConfigurationPayload:
    mes_configuration_payload: dict
    human_subject_configuration: object = None
    dispatcher: object = None


@dataclass
class LogActorConfigurationPayload:
    log_actor_configuration_payload: dict
