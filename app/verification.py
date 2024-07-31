import logging

from disnake import ButtonStyle, MessageInteraction, ModalInteraction
from disnake.ext.commands import Cog
from disnake.ui import Button
from thefuzz import fuzz

from app.bot import VerificationBot
from app.constants import ECHO_SENTENCE
from app.modals import VerificationModal

logger = logging.getLogger(__name__)


class Verification(Cog):
    """Cog providing verification functionality."""

    def __init__(self, bot: VerificationBot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        """Verify buttons are properly set up."""
        for guild in self.bot.guilds:
            channel = None

            for channel_ in guild.text_channels:
                if channel_.name == "\U0001f534-gain-access":
                    channel = channel_
                    break

            if channel is None:
                logger.warning(f"Could not find verification channel in {guild.name}")
                continue

            async for message in channel.history(limit=1):
                if message.author == self.bot.user:
                    logging.info(f"Found verification message in {guild.name}")
                    break
            else:
                logging.info(f"Creating verification message in {guild.name}")
                await channel.send(
                    "Click the button below to gain access to the server.",
                    components=[
                        Button(
                            label="Gain access",
                            style=ButtonStyle.blurple,
                            custom_id="start_self_verification",
                        )
                    ],
                )

    @Cog.listener("on_button_click")
    async def process_button_click(self, inter: MessageInteraction) -> None:
        """Process a button click."""
        if not inter.component.custom_id == "start_self_verification":
            return

        if any(role.name == "Server Access" for role in inter.author.roles):
            await inter.response.send_message(":x: You are already verified!", ephemeral=True)
            return

        await inter.response.send_modal(VerificationModal(self.process_answer))

    @staticmethod
    async def process_answer(inter: ModalInteraction) -> None:
        """Process the answer from the user."""
        answer = inter.text_values["echo"].strip().lower()
        ratio = fuzz.ratio(answer, ECHO_SENTENCE.lower())

        logging.debug(f"Answer: {answer!r} from {inter.author}, ratio: {ratio}")

        if ratio < 85:
            await inter.response.send_message(
                f":x: You are required to enter '{ECHO_SENTENCE}' to gain access to the rest of the server.",
                ephemeral=True,
            )
            return
        else:
            role = next(role for role in inter.guild.roles if role.name == "Server Access")

            if role is None:
                logger.error(f"Could not find 'Server Access' role in {inter.guild.name}")
                await inter.response.send_message(
                    ":x: An error occurred while trying to verify you. Please contact the server staff.",
                    ephemeral=True,
                )
                return

            await inter.author.add_roles(role)
            await inter.response.send_message(
                ":white_check_mark: You have been verified!", ephemeral=True
            )


def setup(bot: VerificationBot) -> None:
    """Set up the verification cog."""
    logger.info("Loading verification extension")
    bot.add_cog(Verification(bot))
