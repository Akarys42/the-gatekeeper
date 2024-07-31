import logging
import sys
from typing import Any

from disnake import AllowedMentions, Intents
from disnake.ext.commands import Context, InteractionBot

from app.constants import ACI
from app.exceptions import InDmsError

logger = logging.getLogger(__name__)


class VerificationBot(InteractionBot):
    """Our main bot class."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_app_command_check(self.__is_in_dms_check, slash_commands=True)

    async def __is_in_dms_check(self, ctx_or_inter: Context | ACI) -> bool:
        """Raises InDmsError if the command is used in DMs."""
        if ctx_or_inter.guild is None:
            raise InDmsError()
        return True

    async def on_error(self, event_method: str, *args: Any, **kwargs: Any) -> None:
        """Log errors using the logging system."""
        # If it happened in DMs, we don't want to log the error
        exception = sys.exc_info()[1]
        if isinstance(exception, InDmsError):
            return

        logger.exception(f"Error in {event_method!r}. Args: {args}, kwargs: {kwargs}")

    @classmethod
    def new(cls) -> "VerificationBot":
        """Generate a populated VerificationBot instance."""
        intents = Intents.none()
        intents.guilds = True
        intents.messages = True

        return cls(
            intents=intents,
            allowed_mentions=AllowedMentions(everyone=False, roles=False, users=False),
        )
