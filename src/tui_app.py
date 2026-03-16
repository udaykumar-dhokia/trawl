from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

import httpx
from .core.config import API_BASE
from textual import on, work
from rich.markup import escape

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.reactive import reactive
from textual.widgets import (
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Markdown,
    Static,
    Button
)

STREAM_ENDPOINT = f"{API_BASE}/chat"
CHATS_ENDPOINT = f"{API_BASE}/chats"
RESPONSES_ENDPOINT = f"{API_BASE}/responses"

def fmt_time(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso)
        return dt.strftime("%b %d, %H:%M")
    except Exception:
        return iso

class StatusBar(Static):
    """Thin status strip shown inside the chat panel."""

    DEFAULT_CSS = """
    StatusBar {
        height: 1;
        background: $surface;
        color: $text-muted;
        padding: 0 2;
        text-style: italic;
    }
    """

    status: reactive[str] = reactive("")

    def render(self) -> str:
        return f"⟳  {escape(self.status)}" if self.status else ""

class ImageItem(Static):
    """Clickable image URL item with thumbnail placeholder."""

    DEFAULT_CSS = """
    ImageItem {
        height: auto;
        padding: 0 1;
        margin-bottom: 1;
        border-left: thick $warning;
        color: $text;
        background: $surface;
    }
    ImageItem:hover {
        background: $boost;
    }
    """

    def __init__(self, index: int, url: str) -> None:
        super().__init__()
        self._index = index
        self._url = url

    def render(self) -> str:
        domain = escape(self._url.split("/")[2] if "//" in self._url else self._url)
        short_url = self._url[:55] + ("…" if len(self._url) > 55 else "")
        safe_short = escape(short_url)

        return (
            f"[{self._index}] 🖼  {domain}\n"
            f"[dim][link='{self._url}']{safe_short}[/link][/dim]"
        )

    def on_click(self) -> None:
        import webbrowser
        webbrowser.open(self._url)

class SourceItem(Static):
    """Single source link in the right sidebar."""

    DEFAULT_CSS = """
    SourceItem {
        height: auto;
        padding: 0 1;
        margin-bottom: 1;
        border-left: thick $accent;
        color: $text;
        background: $surface;
    }
    SourceItem:hover {
        background: $boost;
    }
    """

    def __init__(self, index: int, url: str) -> None:
        super().__init__()
        self._index = index
        self._url = url

    def render(self) -> str:
        domain = escape(self._url.split("/")[2] if "//" in self._url else self._url)
        short_url = self._url[:60] + ("…" if len(self._url) > 60 else "")
        safe_short = escape(short_url)

        return f"[{self._index}] {domain}\n[dim][link='{self._url}']{safe_short}[/link][/dim]"


class ChatBubble(Static):
    """A single query + response block in the chat history."""

    DEFAULT_CSS = """
    ChatBubble {
        height: auto;
        margin-bottom: 2;
        padding: 1 2;
        background: $surface;
        border: round $primary-darken-2;
    }
    ChatBubble .query {
        color: $accent;
        text-style: bold;
        margin-bottom: 1;
    }
    ChatBubble .response {
        color: $text;
    }
    """

    def __init__(self, query: str, response: str) -> None:
        super().__init__()
        self._query = query
        self._response = response

    def compose(self) -> ComposeResult:
        yield Label(f"You: {escape(self._query)}", classes="query")
        yield Markdown(self._response, classes="response")


class LiveResponseWidget(Vertical):
    """Streaming response area — shows status, then streams markdown tokens."""

    DEFAULT_CSS = """
    LiveResponseWidget {
        height: auto;
        padding: 1 2;
        margin-bottom: 2;
        background: $surface;
        border: round $accent;
    }
    LiveResponseWidget #live-query {
        color: $accent;
        text-style: bold;
        margin-bottom: 1;
    }
    LiveResponseWidget #live-status {
        color: $warning;
        text-style: italic;
        height: 1;
    }
    LiveResponseWidget #live-md {
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("", id="live-query")
        yield Label("", id="live-status")
        yield Markdown("", id="live-md")

    def set_query(self, query: str) -> None:
        self.query_one("#live-query", Label).update(f"You: {escape(query)}")

    def set_status(self, msg: str) -> None:
        self.query_one("#live-status", Label).update(f"⟳  {escape(msg)}")

    def clear_status(self) -> None:
        self.query_one("#live-status", Label).update("")

    def append_token(self, token: str) -> None:
        md: Markdown = self.query_one("#live-md", Markdown)
        current = getattr(md, "_markdown", "") or ""
        current += token
        md._markdown = current
        md.update(current)

    def get_content(self) -> str:
        md: Markdown = self.query_one("#live-md", Markdown)
        return getattr(md, "_markdown", "") or ""


class SearchXApp(App):
    """SearchX TUI."""

    TITLE = "SearchX"
    SUB_TITLE = "AI Powered Knowledge Assistant"

    CSS = """
    /* ── Layout ── */
    #root {
        layout: horizontal;
        height: 1fr;
    }

    /* ── Left sidebar: chat list ── */
    #sidebar-left {
        width: 24;
        min-width: 20;
        background: $panel;
        border-right: tall $primary-darken-3;
        height: 1fr;
    }
    #sidebar-left-title {
        background: $primary-darken-2;
        color: $text;
        text-style: bold;
        padding: 0 2;
        height: 3;
        content-align: left middle;
    }
    #chat-list {
        height: 1fr;
        scrollbar-size: 1 1;
    }
    #chat-list > ListItem {
        padding: 1 2;
        background: $panel;
        border-bottom: solid $primary-darken-3;
        height: auto;
    }
    #chat-list > ListItem.--highlight {
        background: $boost;
    }
    #chat-list > ListItem:focus {
        background: $accent-darken-2;
    }
    #new-chat-btn {
        dock: bottom;
        height: 3;
        background: $accent;
        color: $text;
        text-style: bold;
        content-align: center middle;
        border-top: tall $accent-lighten-1;
    }
    #new-chat-btn:hover {
        background: $accent-lighten-1;
    }

    /* ── Centre: chat interface ── */
    #chat-panel {
        width: 1fr;
        height: 1fr;
        background: $background;
        border-right: tall $primary-darken-3;
    }
    #chat-panel-title {
        background: $primary-darken-2;
        color: $text;
        text-style: bold;
        padding: 0 2;
        height: 3;
        content-align: left middle;
    }
    #messages {
        height: 1fr;
        padding: 1 2;
        scrollbar-size: 1 1;
    }
    #input-row {
        dock: bottom;
        height: 5;
        padding: 1 2;
        background: $panel;
        border-top: tall $primary-darken-3;
        layout: horizontal;
    }
    #query-input {
        width: 1fr;
        height: 3;
    }
    #send-btn {
        width: 10;
        height: 3;
        margin-left: 1;
        background: $accent;
        color: $text;
        text-style: bold;
        content-align: center middle;
        border: tall $accent-lighten-1;
    }
    #send-btn:hover {
        background: $accent-lighten-1;
    }

    /* ── Right sidebar: sources ── */
    #sidebar-right {
        width: 28;
        min-width: 22;
        background: $panel;
        height: 1fr;
    }
    #sidebar-right-title {
        background: $primary-darken-2;
        color: $text;
        text-style: bold;
        padding: 0 2;
        height: 3;
        content-align: left middle;
    }
    #sources-scroll {
        height: 1fr;
        padding: 1 1;
        scrollbar-size: 1 1;
    }
    #no-sources {
        color: $text-muted;
        text-style: italic;
        padding: 1 2;
    }

    #sidebar-right-images-title {
    background: $primary-darken-2;
    color: $text;
    text-style: bold;
    padding: 0 2;
    height: 3;
    content-align: left middle;
    }
    #images-scroll {
        height: 1fr;
        padding: 1 1;
        scrollbar-size: 1 1;
        border-bottom: tall $primary-darken-3;
    }
    #sources-scroll {
        height: 1fr;
        padding: 1 1;
        scrollbar-size: 1 1;
    }

    /* ── Empty state ── */
    #empty-state {
        height: 1fr;
        content-align: center middle;
        color: $text-muted;
        text-style: italic;
    }
    """

    BINDINGS = [
        Binding("ctrl+n", "new_chat", "New Chat"),
        Binding("ctrl+r", "refresh_chats", "Refresh"),
        Binding("escape", "blur_input", "Blur"),
        Binding("ctrl+c", "quit", "Quit"),
    ]

    current_chat_id: Optional[str] = None
    _streaming: bool = False

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="root"):

            # Left sidebar
            with Vertical(id="sidebar-left"):
                yield Label("💬  Chats", id="sidebar-left-title")
                yield ListView(id="chat-list")
                yield Button("＋  New Chat", id="new-chat-btn", variant="success")

            # Centre chat panel
            with Vertical(id="chat-panel"):
                yield Label("SearchX", id="chat-panel-title")
                with ScrollableContainer(id="messages"):
                    yield Static(
                        "Select a chat or start a new one  ↙",
                        id="empty-state",
                    )
                with Horizontal(id="input-row"):
                    yield Input(placeholder="Ask anything…", id="query-input")
                    yield Button("Send ↵", id="send-btn", variant="primary")

            # Right sidebar
            with Vertical(id="sidebar-right"):
                yield Label("🖼️  Images", id="sidebar-right-images-title")
                with ScrollableContainer(id="images-scroll"):
                    yield Static("No images yet.")
                yield Label("🔗  Sources", id="sidebar-right-title")
                with ScrollableContainer(id="sources-scroll"):
                    yield Static("No sources yet.")

        yield Footer()

    def on_mount(self) -> None:
        self.load_chats()

    @work(thread=True)
    def load_chats(self) -> None:
        """Fetch chat list from API and populate sidebar."""
        try:
            r = httpx.get(CHATS_ENDPOINT, timeout=5)
            chats = r.json()
        except Exception:
            chats = []

        self.call_from_thread(self._populate_chat_list, chats)

    def _populate_chat_list(self, chats: list[dict]) -> None:
        lv: ListView = self.query_one("#chat-list", ListView)
        lv.clear()
        for chat in chats:
            title = chat.get("title") or "Untitled"
            ts = fmt_time(chat.get("created_at", ""))
            item = ListItem(
                Label(f"{escape(title)}\n[dim]{escape(ts)}[/dim]"),
            )
            item.data = chat
            lv.append(item)

    @on(ListView.Selected, "#chat-list")
    def on_chat_selected(self, event: ListView.Selected) -> None:
        chat = getattr(event.item, "data", None)
        if chat:
            self.current_chat_id = str(chat["id"])
            self.load_chat_history(self.current_chat_id)
            title = chat.get("title") or "Untitled"
            self.query_one("#chat-panel-title", Label).update(f"💬  {title}")

    @work(thread=True)
    def load_chat_history(self, chat_id: str) -> None:
        """Load all responses for a chat from the API."""
        try:
            r = httpx.get(RESPONSES_ENDPOINT, params={"chat_id": chat_id}, timeout=5)
            responses = r.json()
        except Exception:
            responses = []
        self.call_from_thread(self._render_history, responses)

    def _render_history(self, responses: list[dict]) -> None:
        messages = self.query_one("#messages", ScrollableContainer)
        messages.remove_children()

        if not responses:
            messages.mount(Static("No messages yet."))
            return

        all_sources: list[str] = []
        all_images: list[str] = []

        for resp in responses:
            query = resp.get("query", "")
            content = resp.get("response", "")
            sources = resp.get("sources") or []
            images = resp.get("image_urls") or []
            all_sources.extend(sources)
            all_images.extend(images)
            messages.mount(ChatBubble(query, content))

        messages.scroll_end(animate=False)
        self._update_sources(all_sources)
        self._update_images(all_images)

    def _update_images(self, urls: list[str]) -> None:
        scroll = self.query_one("#images-scroll", ScrollableContainer)
        scroll.remove_children()
        if not urls:
            scroll.mount(Static("No images yet."))
            return
        for i, url in enumerate(urls, 1):
            scroll.mount(ImageItem(i, url))


    def _update_sources(self, urls: list[str]) -> None:
        scroll = self.query_one("#sources-scroll", ScrollableContainer)
        scroll.remove_children()
        if not urls:
            scroll.mount(Static("No sources yet."))
            return
        for i, url in enumerate(urls, 1):
            scroll.mount(SourceItem(i, url))

    @on(Input.Submitted, "#query-input")
    def on_input_submitted(self, event: Input.Submitted) -> None:
        self._send_query(event.value)

    @on(Button.Pressed, "#send-btn")
    def on_send_clicked(self) -> None:
        inp = self.query_one("#query-input", Input)
        self._send_query(inp.value)

    def _send_query(self, query: str) -> None:
        query = query.strip()
        if not query or self._streaming:
            return
        inp = self.query_one("#query-input", Input)
        inp.value = ""
        inp.disabled = True
        self._streaming = True
        self.stream_response(query)

    @work(exclusive=True)
    async def stream_response(self, query: str) -> None:
        """Stream SSE events from the API and update the UI live."""

        messages = self.query_one("#messages", ScrollableContainer)

        for w in messages.query("Static"):
            await w.remove()

        live = LiveResponseWidget()
        await messages.mount(live)
        live.set_query(query)
        messages.scroll_end(animate=True)

        current_sources: list[str] = []
        payload = {"query": query}
        if self.current_chat_id:
            payload["chat_id"] = self.current_chat_id

        try:
            async with httpx.AsyncClient(timeout=120) as client:
                async with client.stream(
                    "POST",
                    STREAM_ENDPOINT,
                    json=payload,
                    headers={"Accept": "text/event-stream"},
                ) as resp:

                    async for line in resp.aiter_lines():
                        if not line.startswith("data:"):
                            continue
                        raw = line[5:].strip()
                        if not raw:
                            continue

                        try:
                            data = json.loads(raw)
                        except json.JSONDecodeError:
                            continue

                        event_type = data.get("type")

                        if event_type == "status":
                            live.set_status(data.get("message", ""))

                        elif event_type == "enhanced_query":
                            live.set_status(f"Searching: {data.get('text', '')}")

                        elif event_type == "urls":
                            current_sources = data.get("urls", [])
                            self._update_sources(current_sources)

                        elif event_type == "content":
                            live.clear_status()
                            live.append_token(data.get("text", ""))
                            messages.scroll_end(animate=False)

                        elif event_type == "title":
                            title_text = data.get("text", query[:40])
                            self.query_one("#chat-panel-title", Label).update(
                                f"💬  {title_text}"
                            )
                        
                        elif event_type == "image_urls":
                            self._update_images(data.get("image_urls", []))

                        elif event_type == "done":
                            chat_id = data.get("chat_id")
                            if chat_id:
                                self.current_chat_id = chat_id
                            live.clear_status()
                            self.load_chats()

        except Exception as e:
            live.set_status(f"Error: {e}")

        finally:
            self._streaming = False
            inp = self.query_one("#query-input", Input)
            inp.disabled = False
            inp.focus()


    def action_new_chat(self) -> None:
        self.current_chat_id = None
        messages = self.query_one("#messages", ScrollableContainer)
        messages.remove_children()
        messages.mount(Static("Start a new conversation ↓"))
        self._update_sources([])
        self._update_images([])
        self.query_one("#chat-panel-title", Label).update("SearchX")
        self.query_one("#query-input", Input).focus()

    def action_refresh_chats(self) -> None:
        self.load_chats()

    def action_blur_input(self) -> None:
        self.query_one("#query-input", Input).blur()

    @on(Button.Pressed, "#new-chat-btn")
    def on_new_chat_clicked(self) -> None:
        self.action_new_chat()


def run_tui() -> None:
    SearchXApp().run()

if __name__ == "__main__":
    run_tui()