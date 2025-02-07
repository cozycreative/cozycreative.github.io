# Game Logic Language Structure

The game uses a text-based, choice-driven system. Locations define places the player can visit, and events represent specific interactions within those locations. Choices within locations and events lead to different outcomes.

## Locations

Locations define places the player can visit.

*   `name`: The name of the location.
*   `description`: A description of the location.
*   `choices`: A list of choices available to the player in this location. Each choice has:
    *   `description`: The text displayed to the player for this choice.
    *   `conditions` (optional): Conditions that must be met for this choice to be available.
    *   `outcomes`: A list of outcomes that occur when the player selects this choice.

## Events

Events represent specific interactions within locations.

*   `name`: The name of the event.
*   `description`: A description of the event.
*   `screens`: A list of screens that make up the event. Each screen has:
    *   `id`: A unique identifier for the screen.
    *   `text`: The text displayed to the player on this screen.
    *   `choices`: A list of choices available to the player on this screen. Each choice has:
        *   `description`: The text displayed to the player for this choice.
        *   `conditions` (optional): Conditions that must be met for this choice to be available.
        *   `next_screen` (optional): The ID of the next screen to display if this choice is selected.
        *   `outcomes`: A list of outcomes that occur when the player selects this choice.

## Outcomes

Outcomes define the consequences of a player's choice.

*   `change_location`: Changes the player's current location.
    *   `destination`: The ID of the location to move the player to.
*   `trigger_event`: Triggers another event.
    *   `event`: The ID of the event to trigger.
*   `update_stat`: Updates a player stat.
    *   `stat`: The name of the stat to update.
    *   `value`: The amount to add to (or subtract from) the stat.
*   `set_condition`: Sets a condition to true or false.
    *   `condition`: The name of the condition to set.
    *   `value`: `true` or `false`.
*   `add_to_inventory` / `remove_from_inventory`: Modifies the player's inventory.
    *   `item`: The ID of the item to add or remove.
    *   `quantity` (optional): The number of items to add or remove. Defaults to 1.
    *   `at_home` (optional): A boolean indicating if the item is at home.
*   `update_time`: Advances the game time.
    *   `minutes`: The number of minutes to advance.
*   `message`: Displays a message to the player.
    *   `text`: The text of the message.
*   `end_event`: Ends the current event.

## Conditions

Conditions determine whether a choice is available to the player.

*   `has_inventory`: Checks if the player has a specific item in their inventory.
    *   `item`: The ID of the item to check for.
    *   `quantity` (optional): The minimum quantity of the item required. Defaults to 1.
*   `time_hour`: Checks if the current time is within a specific hour range.
    *   `time_hour`: A range of hours, e.g., `9-17`.
*   `money`: Checks if the player has at least a certain amount of money.
    *   `money`: The minimum amount of money required.
*   `condition`: Checks the value of a boolean condition.
    *   `condition`: The name of the condition to check.
    *   `value`: `true` or `false`.
*   `event_active`: Checks if an event is currently active.
    *   `event`: The ID of the event to check for.
*   `time_passed`: Checks if a certain amount of time has passed since a specific event.
    *   `minutes`: The amount of time that must have passed.
*   `energy`: Checks if the player has at least a certain amount of energy.
    *   `energy`: The minimum amount of energy required.
*   `bed_made`: Checks if the bed is made.
*   `coat_stored`: Checks if the coat is stored.
*   `light_broken`: Checks if the light is broken.
*   `maintenance_needed`: Checks if maintenance is needed.
*   `modeling_interest`: Checks if the player has a modeling interest.
*   `saw_agency_updates`: Checks if the player saw agency updates.
*   `planning_exercise`: Checks if the player is planning exercise.
*   `laundry_in_progress`: Checks if laundry is in progress.
*   `neighbor_present`: Checks if a neighbor is present.
*   `dryer_available`: Checks if a dryer is available.
*   `machine_available`: Checks if a machine is available.
*   `bath_used`: Checks if a bath has been used.
*   `electronics_deal`: Checks if there is an electronics deal.
*   `tools_deal`: Checks if there is a tools deal.
*   `has_collateral`: Checks if there is collateral.
*   `is_sleeping`: Checks if the player is sleeping.
