"""A lot of reminders in Todoist."""

# Standard Library
import os
from typing import Dict, Any

# Todoist
import todoist

# Datetime
from datetime import datetime


class MyTodoist:
    """Todoist api with one token and particular methods to create more reminders."""

    api: todoist.TodoistAPI
    _reminders_by_item: Dict[str, Any]

    def __init__(self):
        """Create api object with token."""
        token = os.environ.get("TODOIST_TOKEN")
        self.api = todoist.TodoistAPI(token)
        self.api.sync()
        self._reminders_by_item = self._get_reminders_by_item()

    def _get_reminders_by_item(self) -> Dict[str, Any]:
        """Get a dict with key item id and value an array of its reminders."""
        all_reminders = self.api.state["reminders"]
        reminders_by_item: Dict[str, Any] = {}
        for reminder in all_reminders:
            item_id = reminder["item_id"]
            reminders_by_item.setdefault(item_id, [])
            reminders_by_item[item_id].append(reminder)
        return reminders_by_item

    def _has_reminder_passed(self, reminder):
        """Return if the reminder has passed."""
        raise NotImplementedError

    def get_active_reminders(self, item: Dict[str, Any]):
        """Get active reminders for an item."""
        for reminder in self._reminders_by_item[item["id"]]:
            pass
        return []

    def create_additional_reminder(self, item: Dict[str, Any]) -> None:
        """Create additional reminder to one item."""
        if self.get_active_reminders(item):
            return
        due_date = datetime.strptime(item["due"], "%Y-%m-%dT%H:%M:%SZ")
        due_has_passed = datetime.now() > due_date
        if due_has_passed:
            pass

    def create_additional_reminders(self) -> None:
        """Create additional reminders to every item."""
        self.api.sync()
        items = self.api.state["items"]
        for item in items:
            self.create_additional_reminder(item)
