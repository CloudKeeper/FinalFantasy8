"""
Details

This defines the Room mixin and commands to implement room detials - non-object
information stored on the room which a player can look at to recieve a more
detailed description.

NOTES:
Allow objects other than the room to have details?

"""

from evennia import utils, DefaultRoom, CmdSet, default_cmds
from django.conf import settings
_SEARCH_AT_RESULT = utils.object_from_module(settings.SEARCH_AT_RESULT)


# Mixin with Default Room

class DetailRoom():
    """
    This is a mixin that provides object functionality for details.
    """

    def return_detail(self, detailkey):
        """
        This looks for an Attribute "obj_details" and possibly
        returns the value of it.

        Args:
            detailkey (str): The detail being looked at. This is
                case-insensitive.

        """
        details = self.db.details
        if details:
            return details.get(detailkey.lower(), None)


# Give to Character Command Set

class CmdDetailLook(default_cmds.CmdLook):
    """
    Looks at the room and on details

    Usage:
        look
        look <obj>
        look <room detail>
        look *<account>

    Observes your location, details at your location or objects
    in your vicinity.
    """

    def func(self):
        """
        Handle the looking. This is a copy of the default look
        code except for adding in the details.
        """
        caller = self.caller
        args = self.args
        
        # No arguement given, use room instead.
        if not args:
            target = [caller.location]
            # If no room, give error.
            if not target:
                caller.msg("You have no location to look at!")
                return
        else:
            target = caller.search(self.args, use_nicks=True, quiet=True)
        
        # If no target found, check for details.
        if not target:
            # Search for details.
            detail = caller.location.return_detail(args)
            if detail:
                self.msg((detail, {"type": "look"}), options=None)
                return
            # If no targets, default behaviour.
            _SEARCH_AT_RESULT(target, caller, args)
            return

        # If multiple targets, default behaviour.
        if len(target) > 1:
            _SEARCH_AT_RESULT(target, caller, args)
            return
        
        # If one target, return appearance.
        if target:
            self.msg((caller.at_look(target[0]), {"type": "look"}), options=None)