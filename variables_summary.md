# Game Variables Summary

This document lists the variables used in the game, categorized by type.

## Stats

Stats represent the player's attributes and characteristics.

*   `happiness`: Player's overall happiness level.
*   `energy`: Player's energy level.
*   `money`: Player's current amount of money.
*   `stress`: Player's stress level.
*   `health`: Player's health level.
*   `social`: Player's social level.
*   `cooking_skill`: Player's cooking skill level.
*   `appearance`: Player's appearance level.
*   `professionalism`: Player's professionalism level.
*   `style`: Player's style level.
*   `modeling_skill`: Player's modeling skill level.
*   `comfort`: Player's comfort level.
*   `fitness`: Player's fitness level.
*   `hygiene`: Player's hygiene level.
*   `grooming`: Player's grooming level.
*   `dirtiness_level`: Player's dirtiness level.
*   `bladder_urgency`: Player's bladder urgency level.
*   `bowel_urgency`: Player's bowel urgency level.
*   `apartment_cleanliness`: Player's apartment cleanliness level.
*   `hydration_level`: Player's hydration level.
*   `sleepiness`: Player's sleepiness level.
*   `sleep_quality`: Player's sleep quality level.
*   `calories_today`: Player's calorie intake for the day.
*   `lastShowerCycle`: The time since the last shower cycle.

## Conditions

Conditions are boolean flags that represent the game's state.

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
*   `electronics_deal`: Checks if there is a tools deal.
*   `tools_deal`: Checks if there is collateral.
*   `has_collateral`: Checks if there is collateral.
    *   `is_sleeping`: Indicates whether the player is sleeping.

## Inventory Items

Inventory items are objects that the player can possess and use.

*   `basic_ingredients`: Basic cooking ingredients.
*   `fresh_ingredients`: Fresh cooking ingredients.
*   `snack_food`: Snack foods.
*   `microwave_meal`: Microwave meals.
*   `coffee_beans`: Coffee beans.
*   `tea_bags`: Tea bags.
*   `cleaning_supplies`: Cleaning supplies.
*   `light_bulb`: A light bulb.
*   `towel`: A towel.
*   `jewelry`: Jewelry.
*   `professional_clothes`: Professional clothes.
*   `fashionable_clothes`: Fashionable clothes.
*   `sporty_clothes`: Sporty clothes.
*   `skincare_products`: Skincare products.
*   `tools`: Tools.
*   `phone`: A phone.
*   `cigarettes`: Cigarettes.
*   `bath_basic_membership`: A basic bath membership.
*   `bath_premium_membership`: A premium bath membership.
*   `detergent`: Detergent.
*   `fabric_softener`: Fabric softener.
*   `wet_clothes`: Wet clothes.
*   `clean_clothes`: Clean clothes.
*   `dish_soap`: Dish soap.
*   `casual_clothes`: Casual clothes.
*   `dirty_clothes`: Dirty clothes.
*   `sorted_laundry`: Sorted laundry.
*   `resume`: A resume.
