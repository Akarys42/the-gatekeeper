from disnake.ext.commands import CommandError


class InDmsError(CommandError):
    """Raised when a command is being executed in a DM."""
