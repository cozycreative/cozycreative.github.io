### **Internal Game Language Documentation**

This document explains how to read and write the internal game language for locations and events in the game system. It covers the structure, components, and purpose of each file type with examples. All files are YAML text files in current folder in Location and Events subfolders.

---

### **File Types**

#### **1. Locations**
- Represent static, persistent places the player can visit.
- Contain:
  - A description of the location.
  - Choices available to the player, which may lead to:
    - Another location.
    - An event.
    - A stat change or message.

#### **2. Events**
- Represent transient interactions triggered by player actions.
- Contain:
  - A title and description.
  - Choices leading to:
    - Outcomes (e.g., stat changes).
    - Transitions to other screens (for multi-screen events).
    - The end of the event.

---

### **File Structure**

#### **Locations**
**Structure**:
```
name: [Location Name]
description: [Description of the location.]

choices:
  - description: [What the player sees for this choice.]
    conditions: [Optional conditions to make the choice available.]
    outcomes: [Results of the choice.]
```

**Example: Downtown**
```
name: Downtown
description: Downtown is alive with energy, skyscrapers towering above bustling sidewalks. A mix of businesspeople, tourists, and street performers fills the streets. Opportunities abound, if you know where to look.

choices:
  - description: Visit the Cinema.
    outcomes:
      - type: change_location
        destination: cinema

  - description: Visit the Luxury Hotel.
    outcomes:
      - type: change_location
        destination: hotel
```

---

#### **Events**
**Structure**:
1. **Simple Events**:
   - Title, description, and choices.
   - Ends after the first set of choices.
2. **Multi-Screen Events**:
   - Contain multiple screens, each identified by an `id`.
   - Each screen contains:
     - Text displayed to the player.
     - Choices leading to outcomes, other screens, or the end of the event.

**Simple Event Example: Hotel No Money**
```
title: No Money, No Room
description: The receptionist looks at you politely but firmly. "Our rooms start at $500 per night," she says. Seeing your hesitation, she adds, "Perhaps you'd like to return when you're better prepared."

choices:
  - description: Leave the hotel lobby.
    outcomes:
      - type: end_event
```

**Multi-Screen Event Example: Insurance Phone Call**
```
title: Unexpected Phone Call
description: Your phone rings unexpectedly. The screen shows an unknown number.

screens:
  - id: start
    text: "Your phone rings. Who could it be?"
    choices:
      - description: "Answer the phone."
        next_screen: answer
      - description: "Ignore it."
        outcomes:
          - type: update_stat
            stat: stress
            value: +5
          - type: end_event

  - id: answer
    text: "You answer the phone. A voice on the other end says, 'Hello, do you have a moment to talk about your car's extended warranty?'"
    choices:
      - description: "Hang up immediately."
        outcomes:
          - type: end_event
      - description: "Let them continue."
        next_screen: continue_warranty

  - id: continue_warranty
    text: "The person drones on about coverage options. You struggle to stay polite."
    choices:
      - description: "Politely decline and hang up."
        outcomes:
          - type: update_stat
            stat: politeness
            value: +5
          - type: end_event
      - description: "Interrupt them and end the call."
        outcomes:
          - type: update_stat
            stat: assertiveness
            value: +5
          - type: end_event
```

---

### **Components**

#### **Choices**
- Allow players to act within a location or event.
- Each choice has:
  - `description`: Text shown to the player.
  - `conditions`: (Optional) Criteria for the choice to be available.
  - `outcomes`: Results of the choice.

#### **Conditions**
- Control when choices are available.
- Common conditions:
  - `money`: Required amount of money.
  - `energy`: Required energy level.
  - `time_hour`: Time of day (e.g., "9-17" for 9 AM to 5 PM).
  - `has_inventory`: Check for items in inventory.
    - Single item: `has_inventory: tool`
    - Multiple items (any): `has_inventory: electronics or jewelry or tools`
    - Multiple items (all): `has_inventory: tool and key`

#### **Outcomes**
- Define what happens when a choice is made.
- Each outcome must be ONE of these mutually exclusive types:
  - `change_location`: Move to a new location.
  - `trigger_event`: Start a specific event.
  - `message`: Display a message to the player.
  - `end_event`: End the current event and return to previous location.
- Additional outcomes that can be combined with any of the above:
  - `update_stat`: Change a player stat.
  - `update_inventory`: Add/remove items.
  - `update_time`: Advance game time.
  - `set_condition`: Set a game condition.

Example of mutually exclusive outcomes:
```yaml
# Valid - single outcome type with optional updates
outcomes:
  - type: update_stat
    stat: money
    value: -10
  - type: update_time
    minutes: 15
  - type: message
    text: "You spend some money and time."

# Invalid - cannot combine message/location/event/end
outcomes:
  - type: message
    text: "You buy something."
  - type: change_location
    destination: shop
```

---

### **File Placement**
1. **Locations**: `/locations/`
   - Example: `/locations/downtown.txt`, `/locations/hotel.txt`
2. **Events**: `/events/`
   - Example: `/events/hotel_no_money.txt`, `/events/insurance_phone_call.txt`

---

### **Guidelines for Writing**
1. **Keep It Simple**:
   - Avoid overly complex conditions or branching unless necessary.
2. **Use Multi-Screen Events for Conversations**:
   - Reserve multi-screen events for scenarios requiring multiple steps or dialogue exchanges.
3. **Avoid Dead Ends**:
   - Always provide a way for the player to return to a location or resolve the event.
4. **Be Specific with Event Names**:
   - Use descriptive names that include the location (e.g., sell_items_pawnshop instead of just sell_items).
5. **Choose Appropriate Outcome Types**:
   - Use message for simple feedback that keeps player in same location.
   - Use trigger_event for complex interactions requiring multiple steps.
   - Use change_location for moving between locations.
   - Use end_event to return from events.
