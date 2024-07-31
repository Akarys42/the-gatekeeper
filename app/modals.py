from typing import Awaitable, Callable

from disnake import ModalInteraction
from disnake.ui import Modal, TextInput

from app.constants import ECHO_SENTENCE


class VerificationModal(Modal):
    """Modal for the verification process."""

    ECHO_TEST = TextInput(
        custom_id="echo",
        label=f"Enter '{ECHO_SENTENCE}'",
        max_length=len(ECHO_SENTENCE) + 3,
        placeholder=ECHO_SENTENCE,
    )

    def __init__(self, callback: Callable[[ModalInteraction], Awaitable[None]]) -> None:
        super().__init__(
            title="Repeat the following sentence",
            custom_id="self_verify",
            components=[self.ECHO_TEST],
        )
        self.__callback = callback

    async def callback(self, interaction: ModalInteraction, /) -> None:
        """Process the answer from the user."""
        await self.__callback(interaction)
