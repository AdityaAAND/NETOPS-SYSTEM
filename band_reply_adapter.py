"""Band adapter that turns a completed LangGraph state into a chat reply."""

from __future__ import annotations

from typing import Any

from band.adapters.langgraph import LangGraphAdapter
from band.core.protocols import AgentToolsProtocol
from band.core.types import PlatformMessage
from langchain_core.messages import HumanMessage


class ReplyingLangGraphAdapter(LangGraphAdapter):
    """Run the NetOps LangGraph workflow and post its final report to Band chat."""

    async def on_message(
        self,
        msg: PlatformMessage,
        tools: AgentToolsProtocol,
        history: list[Any],
        participants_msg: str | None,
        contacts_msg: str | None,
        *,
        is_session_bootstrap: bool,
        room_id: str,
    ) -> None:
        """Handle a Band chat message, invoke LangGraph, then send the reply."""
        graph = self._get_graph()
        graph_input = self._build_graph_input(
            msg=msg,
            history=history,
            participants_msg=participants_msg,
            contacts_msg=contacts_msg,
        )

        # LangGraph keeps room-scoped state under Band's room ID.
        result = await graph.ainvoke(
            graph_input,
            config={
                "configurable": {
                    "thread_id": room_id,
                },
                "recursion_limit": self.recursion_limit,
            },
        )

        reply = self._extract_reply_text(result)
        mentions = await self._mentions_for_sender(msg, tools)

        # This is the SDK call that creates the visible Band chat message.
        await tools.send_message(reply, mentions=mentions)

    def _get_graph(self) -> Any:
        """Return the configured static graph for this project adapter."""
        if self._static_graph is None:
            raise RuntimeError("ReplyingLangGraphAdapter requires a static graph")
        return self._static_graph

    def _build_graph_input(
        self,
        *,
        msg: PlatformMessage,
        history: list[Any],
        participants_msg: str | None,
        contacts_msg: str | None,
    ) -> dict[str, list[Any]]:
        """Build the LangGraph state shape expected by graph.nodes.get_alert."""
        messages: list[Any] = []
        messages.extend(history or [])

        # Participant/contact updates are preserved as context for future growth.
        if participants_msg:
            messages.append(HumanMessage(content=f"[System]: {participants_msg}"))
        if contacts_msg:
            messages.append(HumanMessage(content=f"[System]: {contacts_msg}"))

        messages.append(HumanMessage(content=msg.format_for_llm()))
        return {"messages": messages}

    def _extract_reply_text(self, result: dict[str, Any]) -> str:
        """Extract the user-visible RCA report from the final LangGraph state."""
        messages = result.get("messages") or []
        if messages:
            last_message = messages[-1]
            content = getattr(last_message, "content", None)
            if content:
                return str(content).strip()

        recommendation = result.get("recommendation")
        if recommendation:
            return f"Recommendation:\n{recommendation}".strip()

        raise RuntimeError("LangGraph completed without a message or recommendation")

    async def _mentions_for_sender(
        self,
        msg: PlatformMessage,
        tools: AgentToolsProtocol,
    ) -> list[dict[str, str]]:
        """Resolve the original sender into the mention required by Band chat."""
        participant = self._find_participant(msg.sender_id, tools.participants)
        if participant is None:
            await tools.get_participants()
            participant = self._find_participant(msg.sender_id, tools.participants)

        handle = ""
        if participant is not None:
            handle = str(participant.get("handle") or "")

        # Dict mentions are accepted by the SDK and avoid losing the sender ID.
        return [
            {
                "id": msg.sender_id,
                "handle": handle,
            }
        ]

    def _find_participant(
        self,
        sender_id: str,
        participants: list[Any],
    ) -> dict[str, Any] | None:
        """Find the Band participant record for the incoming message sender."""
        for participant in participants:
            if isinstance(participant, dict) and participant.get("id") == sender_id:
                return participant
        return None
