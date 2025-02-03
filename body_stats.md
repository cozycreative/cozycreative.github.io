# Life Simulation Body Stats Engine Manual

This manual documents the simulation engine that models a character’s daily physiological and cosmetic processes. The engine is designed to capture realistic human responses for parameters such as energy, mood, hydration, bodily functions, addiction cravings, hunger, sleep, and cosmetic degradation. The code uses both linear and non-linear scaling to represent thresholds and recovery dynamics, drawing on clinical and experimental research.

## Table of Contents

- [Overview](#overview)
- [Character Attributes](#character-attributes)
- [Attractiveness and Appearance Calculations](#attractiveness-and-appearance-calculations)
- [Physiological Processes](#physiological-processes)
  - [Energy and Mood](#energy-and-mood)
  - [Hydration (Thirst)](#hydration-thirst)
  - [Bodily Functions](#bodily-functions)
    - [Bladder Urgency](#bladder-urgency)
    - [Bowel Urgency](#bowel-urgency)
  - [Addiction Cravings](#addiction-cravings)
  - [Hunger](#hunger)
- [Sleep Process](#sleep-process)
  - [Recovery of Energy and Mood](#recovery-of-energy-and-mood)
  - [Slower Updates During Sleep](#slower-updates-during-sleep)
  - [Cosmetic Effects During Sleep](#cosmetic-effects-during-sleep)
  - [Variable Sleep Duration and Effective Recovery](#variable-sleep-duration-and-effective-recovery)
- [Other Processes](#other-processes)
  - [Cosmetic and Grooming Updates](#cosmetic-and-grooming-updates)
  - [Aging and Body Changes](#aging-and-body-changes)
- [Constants and Rates](#constants-and-rates)
- [Usage and Example](#usage-and-example)
- [Extending the Engine](#extending-the-engine)
- [References](#references)

---

## Overview

This simulation engine models a life-like character that experiences changes in physiological states and appearance. Key factors include:
- **Energy and Mood**: They decay over time, with recovery provided by sleep.
- **Hydration**: Water loss leads to thirst and, eventually, dehydration penalties.
- **Bodily Functions**: Bladder and bowel urgencies accumulate over time.
- **Addiction Cravings**: Cravings for nicotine, alcohol, and drugs increase continuously.
- **Hunger**: Hunger builds over time if the character does not eat.
- **Sleep**: Sleep both restores deficits (energy, mood) and allows other processes to continue, albeit at slower rates.
- **Cosmetic Effects**: Grooming factors (e.g., makeup quality, hair combing) deteriorate during sleep.

The code is structured into modular update methods that can be called over time (e.g., every minute) to simulate the character’s day-to-day life.

---

## Character Attributes

The `Character` class initializes a range of attributes, including:

- **General Attributes**:  
  - `gender` (e.g., "female", "male")  
  - `age`  
  - `baseBeauty`

- **Physical Appearance & Body Shape**:  
  - `breastSize`, `hipSize`, `waistSize`, `height`, `weight`, `bodyFatPercentage`, `buttocksSize`  
  - Facial and hair attributes: `lipSize`, `noseSize`, `eyeSize`, `eyebrowThickness`, `hairLength`, `hairStyle`, `tattooCount`, `piercingCount`  
  - Skin-related: `tanLevel`, `skinCondition`, `absDefinition`, `shoulderWidth`, `armMuscle`, `legMuscle`

- **Health & Fitness**:  
  - `health`, `fitness`, `energyLevel`

- **Personal Grooming & Style**:  
  - `grooming`, `makeupOn`, `makeupQuality`, `hairGroomed`, `pedicureQuality`, `manicureQuality`, `bodyHair`, `clothingStyle`, `recentShower`

- **Vital Signs & Mental State**:  
  - `mood`, `moodDecayRate`, `dirtinessLevel`  
  - Bodily functions: `bladderUrgency`, `bowelUrgency`  
  - Hydration: `hydrationLevel`  
  - Sleepiness

- **Additional Processes**:  
  - `hunger` (scale 0–100)  
  - `attractiveness` (computed overall score)  
  - Sexual/Arousal: `horny`, `orgasmSatisfaction`  
  - Addiction variables: `nicotineCraving`, `alcoholCraving`, `drugCraving`, `heroinLevel`, `alcoholWithdrawalTime`  
  - Sleep Quality: `sleepQuality`  
  - Stress: `stress`  
  - Other derived attributes: `lastShowerCycle`, `wrinkles`, `fatigueRate`

---

## Attractiveness and Appearance Calculations

The `calculate_attractiveness` method combines many factors:
- **Core Factors**:  
  Base beauty, health, fitness, and skin condition.
- **Grooming & Personal Style**:  
  Bonuses from grooming, makeup (with quality adjustments), hair grooming, nail care, and clothing style.
- **Hygiene**:  
  A bonus for low dirtiness, with non-linear penalties using a sigmoid function.
- **Weight and Body Fat**:  
  Penalizes deviations from an ideal weight based on height.
- **Stress**:  
  Non-linear penalty based on the current stress level.
- **Body Proportions & Muscle Tone**:  
  Adjustments for waist-to-hip ratio, abdominal definition, arm/leg muscle (with gender differences), buttocks size, and, for females, breast size.
- **Cosmetic Modifiers**:  
  Small bonuses for a tasteful number of tattoos and piercings; heavy modifications lead to penalties.

---

## Physiological Processes

### Energy and Mood

- **Energy Decay:**  
  Energy decays at a baseline rate (modulated by fitness) during wakefulness. When energy reaches 0, the character is forced to sleep.
- **Mood Decay:**  
  Mood decays over time at a rate affected by stress. If mood falls too low, depression effects are triggered.

### Hydration (Thirst)

- **Update Rate:**  
  Hydration decreases at a rate of 0.10 per minute during wakefulness (about 6 points per hour).  
- **Consequence:**  
  If hydration reaches 0, dehydration penalties are applied. During sleep, the loss rate is reduced (0.05 per minute).

### Bodily Functions

#### Bladder Urgency

- **Awake Rate:**  
  Initially set at 0.28 per minute, but revised to 0.14 per minute during wakefulness.
- **Sleep Rate:**  
  During sleep, the bladder urgency increases at a slower rate (0.07 per minute).
- **Threshold:**  
  If urgency exceeds 50, forced urination is triggered (or the character is woken up).

#### Bowel Urgency

- **Awake Rate:**  
  Initially 0.20 per minute, revised to 0.10 per minute.
- **Sleep Rate:**  
  During sleep, bowel urgency increases at 0.05 per minute.
- **Threshold:**  
  Exceeding 50 triggers forced defecation.

### Addiction Cravings

- **Nicotine Craving:**  
  Increases rapidly at 0.20 per minute during wakefulness. During sleep, this is reduced to 0.05 per minute.
- **Alcohol Craving:**  
  Increases at 0.10 per minute awake and 0.03 per minute during sleep.
- **Drug Craving:**  
  Increases at 0.05 per minute awake and 0.02 per minute during sleep.
- **Overdose Trigger:**  
  If heroin level exceeds a threshold (e.g., 9), an overdose event is triggered.

### Hunger

- **Awake Rate:**  
  Hunger increases at 0.10 per minute awake (resulting in near 100 points over 16 hours).
- **Revised Sleep Rate:**  
  During sleep, hunger increases at a reduced rate of 0.15 per minute awake, later revised to 0.08 per minute in the sleep process to simulate slower metabolism.
- **Threshold:**  
  When hunger reaches 100, starvation events are triggered.

---

## Sleep Process

The sleep process is more complex because many functions continue but at slower rates. Below are the key points:

### Recovery of Energy and Mood

- **Restoration:**  
  Sleep restores energy and mood proportionally to the current deficits.  
- **Effective Sleep Duration:**  
  The simulation adjusts the effective sleep time if the character is extremely depleted (average deficit over energy and mood >50). This “oversleep” factor increases recovery time up to a cap (e.g., 12 hours). Conversely, if the character is almost fully refreshed (deficit <10), extra sleep does not yield extra benefit.
- **Calculation:**  
  A recovery factor is computed based on the effective sleep duration relative to a full 480-minute (8-hour) recovery period and the character's sleep quality.

### Slower Updates During Sleep

During sleep, the following rates are reduced compared to wakefulness:
- **Hydration Loss:** 0.05 per minute.
- **Bladder Urgency:** 0.07 per minute.
- **Bowel Urgency:** 0.05 per minute.
- **Dirtiness:** Accumulates at 0.1/60 per minute.
- **Hunger:** Increases at 0.08 per minute.
- **Addiction Cravings:** Nicotine (0.05/min), Alcohol (0.03/min), Drug (0.02/min).

### Cosmetic Effects During Sleep

- **Makeup:**  
  If makeup is applied, its quality degrades (simulating smearing) by a fixed decrement (0.5 points per sleep session).
- **Hair:**  
  Hair is set to an uncombed state after sleep (i.e., `hairGroomed` is marked `False`).

### Variable Sleep Duration and Effective Recovery

- **Default:**  
  The sleep method defaults to 480 minutes (8 hours) if no duration is provided.
- **Oversleeping:**  
  If the average deficit of energy and mood is high (>50), the effective sleep duration is increased (using a scaling factor) to simulate extra recovery up to a cap (e.g., 720 minutes or 12 hours).
- **Diminishing Returns:**  
  If the deficits are minimal (<10), additional sleep does not provide extra recovery (capped at 480 minutes).

---

## Other Processes

### Cosmetic and Grooming Updates

- **Makeup:**  
  Makeup quality is impacted by both daily activity and sleep. If makeup is applied during wakefulness, it remains effective; however, during sleep, makeup quality degrades, reflecting smearing.
- **Hair:**  
  The hair is assumed to be groomed during the day if maintained but becomes uncombed after sleep.

### Aging and Body Changes

- **Aging Effects:**  
  With each passing year (or a defined time increment), the character’s age increases. Aging impacts skin condition, base beauty, and introduces wrinkles and increased fatigue.

---

## Constants and Rates

Below is a summary of the key rates used in the simulation:

| **Process**                | **Awake Rate**       | **Sleep Rate**         | **Notes**                                          |
|----------------------------|----------------------|------------------------|----------------------------------------------------|
| **Hydration Loss**         | 0.10 per minute      | 0.05 per minute        | ~6 points/hour awake; ~3 points/hour during sleep   |
| **Bladder Urgency**        | 0.14 per minute      | 0.07 per minute        | Threshold at 50 triggers forced urination         |
| **Bowel Urgency**          | 0.10 per minute      | 0.05 per minute        | Threshold at 50 triggers forced defecation         |
| **Nicotine Craving**       | 0.20 per minute      | 0.05 per minute        | Faster buildup awake; slowed during sleep          |
| **Alcohol Craving**        | 0.10 per minute      | 0.03 per minute        |                                                    |
| **Drug Craving**           | 0.05 per minute      | 0.02 per minute        |                                                    |
| **Hunger**                 | 0.10 per minute      | 0.08 per minute        | Adjusted for slower metabolism during sleep        |
| **Dirtiness**              | (varies)             | 0.1/60 per minute      | Accumulates very slowly during sleep               |
| **Sleep Recovery**         | N/A                  | Effective duration based on deficit (default 480 min) | Oversleep factor applied if deficit >50            |
| **Makeup Decay**           | N/A                  | 0.5 quality points per sleep session |                                                    |

---

## Usage and Example

An example usage is provided in the code. The character is created, and then the update functions are called with a specified duration (in minutes). The sleep function is designed to be called with an optional parameter (defaults to 480 minutes if not provided).

```python
if __name__ == "__main__":
    # Create a character
    char = Character()
    print("Initial energy:", char.energyLevel)
    print("Initial mood:", char.mood)
    
    # Simulate sleep for the default duration (8 hours)
    char.sleep()  # defaults to 480 minutes
    print("After sleep:")
    print("Energy:", char.energyLevel)
    print("Mood:", char.mood)
```

---

## Extending the Engine

To further extend this simulation engine, consider:
- **Variable Rates by Context:**  
  Adjust rates based on activity level, weather conditions, or emotional state.
- **Individual Differences:**  
  Allow for customization of thresholds (e.g., bladder capacity, metabolic rate).
- **Additional Cosmetic Effects:**  
  Track other factors such as skin tone, makeup style changes, and clothing cleanliness.
- **Integrative Behaviors:**  
  Link social interactions or environmental cues (e.g., stress at work) with changes in these processes.

---

## References

1. Healthline, Excessive Thirst Articles – [Excessive Thirst](https://www.healthline.com/health/thirst-excessive)
2. NHS Information on Thirst and Dehydration – [NHS Thirst](https://www.nhs.uk/conditions/thirst/)
3. Verywell Health articles on dehydration – [Dehydration with Symptoms](https://www.verywellhealth.com/dehydration-8662174)
4. Research articles on cue reactivity and addiction (e.g., Burton & Tiffany, 1997).
5. Clinical descriptions of human physiology (e.g., Mayo Clinic, Cleveland Clinic).
6. Wikipedia articles on dehydration and cue reactivity.