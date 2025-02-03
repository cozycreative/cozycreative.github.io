import random
import math

def sigmoid(x):
    """A basic sigmoid function for non–linear scaling."""
    return 1 / (1 + math.exp(-x))

def ideal_bonus(value, ideal, tolerance, max_bonus):
    """
    Returns a bonus that peaks when value == ideal and then drops off.
    Within tolerance, a positive bonus is awarded; beyond tolerance, a penalty is applied.
    """
    deviation = abs(value - ideal)
    if deviation <= tolerance:
        # linearly decrease bonus from max_bonus to 0 as deviation increases
        return max_bonus * (1 - deviation / tolerance)
    else:
        # beyond tolerance, penalize proportionally
        return -max_bonus * ((deviation - tolerance) / tolerance)

class Character:
    def __init__(self):
        # -----------------------------------
        # Character Stats (General)
        # -----------------------------------
        self.gender = 'female'  # can be 'female' or 'male'
        self.age = 20
        self.baseBeauty = 50  # Intrinsic beauty

        # -----------------------------------
        # Physical Appearance & Body Shape
        # -----------------------------------
        self.breastSize = 35       # For females: moderate size (arbitrary units)
        self.hipSize = 90          # Hip size in cm
        self.waistSize = 70        # Waist size in cm
        self.height = 170          # Height in cm
        self.weight = 70           # Weight in kg
        self.bodyFatPercentage = 20.0  # Body fat percentage
        self.buttocksSize = 50     # Buttocks size on scale 0-100 (average ~50)

        self.lipSize = 0
        self.noseSize = 0
        self.eyeSize = 0
        self.eyebrowThickness = 0
        self.hairLength = 0
        self.hairStyle = "short"
        self.tattooCount = 0
        self.piercingCount = 0
        self.tanLevel = 0
        self.skinCondition = 100

        # New Body Parts & Shape Attributes
        self.absDefinition = 0
        self.shoulderWidth = 40
        self.armMuscle = 50
        self.legMuscle = 50

        # -----------------------------------
        # Health and Fitness Factors
        # -----------------------------------
        self.health = 100
        self.fitness = 50
        self.energyLevel = 100

        # -----------------------------------
        # Personal Grooming & Style
        # -----------------------------------
        self.grooming = 50
        self.makeupOn = False
        self.makeupQuality = 0
        self.hairGroomed = True
        self.pedicureQuality = 0
        self.manicureQuality = 0
        self.bodyHair = 1  # Lower value means minimal body hair
        self.clothingStyle = 50
        self.recentShower = True

        # -----------------------------------
        # Vital Signs & Mental State
        # -----------------------------------
        self.mood = 100
        self.moodDecayRate = 1
        self.dirtinessLevel = 0

        # For bodily functions:
        self.bladderUrgency = 0  # scale 0-100; threshold >50 triggers forced urination
        self.bowelUrgency = 0    # similar scale; threshold >50 triggers forced defecation

        # Hydration:
        self.hydrationLevel = 100  # scale 0-100; 0 triggers dehydration penalties

        # Sleep:
        self.sleepiness = 0

        # -----------------------------------
        # Additional Physiological/Behavioral Attributes
        # -----------------------------------
        self.hunger = 0  # 0 (not hungry) to 100 (starving)
        self.attractiveness = 50  # Overall attractiveness score (computed)
        
        # Sexual and Arousal:
        self.horny = 0
        self.orgasmSatisfaction = 0

        # -----------------------------------
        # Addictions (Cigarettes, Alcohol, Drugs)
        # -----------------------------------
        self.nicotineCraving = 0    # Craving level for cigarettes
        self.alcoholCraving = 0     # Craving level for alcohol
        self.drugCraving = 0        # For general narcotics
        self.heroinLevel = 0        # Level of heroin in bloodstream
        self.alcoholWithdrawalTime = 0

        # -----------------------------------
        # Sleep Quality & Stress
        # -----------------------------------
        self.sleepQuality = 100  # Sleep quality 0-100
        self.stress = 0

        # -----------------------------------
        # Additional Attributes (Derived)
        # -----------------------------------
        self.lastShowerCycle = 0

        # For aging:
        self.wrinkles = 0
        self.fatigueRate = 1.0

    # ========================================================
    # Attractiveness & Appearance Calculations
    # ========================================================
    def calculate_attractiveness(self):
        """
        Calculates overall attractiveness based on various factors:
        Base beauty, health, fitness, skin condition, grooming, and detailed body proportions.
        Uses non-linear functions for hygiene, weight, and stress, and applies gender-specific bonuses.
        """
        # Core components:
        attractiveness = (
            self.baseBeauty +
            0.3 * self.health +
            0.3 * self.fitness +
            0.2 * self.skinCondition
        )

        # Personal Grooming & Style Bonus:
        groomingBonus = 0.2 * self.grooming
        if self.makeupOn:
            if self.makeupQuality >= 1:
                groomingBonus += 5
            elif self.makeupQuality > 0:
                groomingBonus += 2
            else:
                groomingBonus -= 2
        groomingBonus += (3 if self.hairGroomed else -3)
        groomingBonus += self.pedicureQuality * 3
        groomingBonus += self.manicureQuality * 3
        groomingBonus += 5 * (1 / self.bodyHair)
        clothingBonus = (self.clothingStyle - 50) / 5
        groomingBonus += clothingBonus
        if self.recentShower:
            groomingBonus += 3
        attractiveness += groomingBonus

        # Hygiene & Dirtiness Effects:
        if self.dirtinessLevel < 3:
            hygieneBonus = (3 - self.dirtinessLevel) * 1
        else:
            hygieneBonus = 0
        attractiveness += hygieneBonus
        dirtinessPenalty = 10 * sigmoid(self.dirtinessLevel - 3)
        attractiveness -= dirtinessPenalty

        # Weight Penalty: Using ideal BMI (e.g., 22) based on height
        ideal_weight = 22 * (self.height / 100) ** 2
        weight_deviation = self.weight - ideal_weight
        weight_penalty = 5 * math.tanh(abs(weight_deviation) / 5)
        attractiveness -= weight_penalty

        # Stress Penalty:
        stressPenalty = 8 * sigmoid((self.stress - 50) / 10)
        attractiveness -= stressPenalty

        # Body Shape & Muscle Bonuses:
        # Waist-to-Hip Ratio:
        if self.hipSize > self.waistSize:
            ratioBonus = (self.hipSize - self.waistSize) * 0.2
        else:
            ratioBonus = -abs(self.hipSize - self.waistSize) * 0.2
        attractiveness += ratioBonus

        # Abs definition bonus:
        attractiveness += self.absDefinition / 10

        # Muscle Tone:
        if self.gender == 'female':
            arm_adjustment = ideal_bonus(self.armMuscle, ideal=40, tolerance=10, max_bonus=3)
            leg_adjustment = ideal_bonus(self.legMuscle, ideal=40, tolerance=10, max_bonus=3)
        else:
            arm_adjustment = ideal_bonus(self.armMuscle, ideal=80, tolerance=20, max_bonus=3)
            leg_adjustment = ideal_bonus(self.legMuscle, ideal=80, tolerance=20, max_bonus=3)
        attractiveness += (arm_adjustment + leg_adjustment)

        # Buttocks Size Bonus using ideal function:
        butt_bonus = ideal_bonus(self.buttocksSize, ideal=55, tolerance=10, max_bonus=5)
        attractiveness += butt_bonus

        # Breast Size Bonus for females:
        if self.gender == 'female':
            breast_bonus = ideal_bonus(self.breastSize, ideal=35, tolerance=10, max_bonus=5)
            attractiveness += breast_bonus

        # Tattoos & Piercings:
        if self.tattooCount <= 2:
            attractiveness += self.tattooCount * 1.5
        elif self.tattooCount > 4:
            attractiveness -= (self.tattooCount - 4) * 2
        if self.piercingCount <= 2:
            attractiveness += self.piercingCount * 0.5
        elif self.piercingCount > 3:
            attractiveness -= (self.piercingCount - 3) * 1.0

        self.attractiveness = attractiveness

    # ========================================================
    # Basic Body Functions
    # ========================================================
    def update_energy(self, duration_minutes=1):
        """
        Energy decays at a fixed rate per minute,
        modulated by fitness. If energy drops to 0, force sleep.
        """
        energy_loss_rate = 0.05  # baseline energy loss per minute
        fitness_modifier = 1 - (self.fitness / 200)
        self.energyLevel -= energy_loss_rate * duration_minutes * fitness_modifier
        if self.energyLevel <= 0:
            self.force_sleep()

    def update_mood(self, duration_minutes=1):
        """
        Mood decays over time, further amplified by stress.
        """
        mood_loss = (self.moodDecayRate / 60) * duration_minutes
        stress_modifier = 1 + (self.stress / 100)
        self.mood -= mood_loss * stress_modifier
        if self.mood <= 10:
            self.apply_depression_effects()

    # ========================================================
    # Revised Hydration System (Thirst)
    # ========================================================
    def update_hydration(self, duration_minutes=1):
        """
        Hydration now decays faster to mimic realistic fluid loss.
        Using 0.10 points per minute results in roughly 6 points lost per hour.
        Extreme thirst (and dehydration penalties) occur when hydrationLevel reaches 0.
        """
        hydration_loss_rate = 0.10  # revised: ~0.10 per minute
        self.hydrationLevel -= hydration_loss_rate * duration_minutes
        if self.hydrationLevel <= 0:
            self.apply_dehydration_penalties()

    # ========================================================
    # Revised Bodily Functions (Urination & Defecation)
    # ========================================================
    def update_bodily_functions(self, duration_minutes=1):
        """
        Updates bladder and bowel urgencies.
        Revised rates: bladder urgency increases by ~0.14 per minute (≈50 in 360 minutes),
        and bowel urgency increases by ~0.10 per minute.
        """
        bladder_increase_rate = 0.14  # now accumulates to ~50 in 6 hours
        bowel_increase_rate = 0.10    # similarly, slower accumulation
        self.bladderUrgency += bladder_increase_rate * duration_minutes
        self.bowelUrgency += bowel_increase_rate * duration_minutes
        if self.bladderUrgency > 50:
            self.trigger_forced_urination()
        if self.bowelUrgency > 50:
            self.trigger_forced_defecation()

    # ========================================================
    # Revised Addiction Updates (Cravings)
    # ========================================================
    def update_addictions(self, duration_minutes=1):
        """
        Addiction cravings increase over time.
        Nicotine craving increases at 0.20 per minute (faster buildup),
        while alcohol craving increases at 0.10 per minute.
        Drug craving remains lower.
        """
        self.nicotineCraving += 0.20 * duration_minutes  # faster buildup for cigarettes
        self.alcoholCraving += 0.10 * duration_minutes     # moderate rate for alcohol
        self.drugCraving += 0.05 * duration_minutes
        if self.heroinLevel > 9:
            self.trigger_overdose()

    # ========================================================
    # Revised Hunger System
    # ========================================================
    def update_hunger(self, duration_minutes=1):
        """
        Hunger increases over time. Revised rate of 0.15 per minute,
        so that noticeable hunger builds in a few hours.
        """
        self.hunger += 0.15 * duration_minutes
        if self.hunger > 100:
            self.hunger = 100
            self.trigger_starvation()

    # ========================================================
    # Sleep Mechanics (Including Withdrawal & Depression Effects)
    # ========================================================
    def sleep(self, sleep_minutes=480):
        """
        Sleep restores energy and mood and updates other processes—but at reduced rates.
        
        If sleep_minutes is not provided, it defaults to 480 (8 hours).
        The method calculates an effective sleep duration for recovery of energy and mood:
        - If the average deficit (across energy and mood) is very high (>50), the character “oversleeps”
            (i.e. the effective sleep duration is increased by a scaling factor, up to a cap, to simulate extra recovery).
        - If the character is nearly fully refreshed (average deficit <10), extra sleep does not yield extra recovery.
        
        Other functions (hydration loss, bladder and bowel urgency, hunger, addiction cravings,
        and cosmetic deterioration) continue during sleep at slower rates.
        """
        # --- Determine Recovery Deficits ---
        energy_deficit = 100 - self.energyLevel
        mood_deficit = 100 - self.mood
        avg_deficit = (energy_deficit + mood_deficit) / 2.0

        # --- Compute Effective Sleep Duration for Recovery ---
        # Default sleep_minutes is used if provided.
        if avg_deficit > 50:
            # For each 10 points above 50, add 25% more effective sleep time.
            # For example, if avg_deficit = 70, that's 20 points above 50,
            # so oversleep_factor = 1 + (20/40) = 1.5.
            oversleep_factor = 1 + ((avg_deficit - 50) / 40.0)
            effective_sleep = sleep_minutes * oversleep_factor
            # Cap effective sleep (e.g., maximum of 720 minutes, 12 hours)
            effective_sleep = min(effective_sleep, 720)
        elif avg_deficit < 10:
            # If nearly refreshed, extra sleep does not boost recovery.
            effective_sleep = min(sleep_minutes, 480)
        else:
            effective_sleep = sleep_minutes

        # --- Energy and Mood Recovery ---
        # Recovery is proportional: 480 minutes of sleep at perfect sleepQuality (100) fully restores deficits.
        recovery_factor = (effective_sleep / 480) * (self.sleepQuality / 100)
        energy_gain = energy_deficit * recovery_factor
        mood_gain = mood_deficit * recovery_factor
        self.energyLevel += energy_gain
        self.mood += mood_gain
        # Ensure values do not exceed 100
        if self.energyLevel > 100:
            self.energyLevel = 100
        if self.mood > 100:
            self.mood = 100

        # --- Update Other Physiological Processes Using the Actual Sleep Duration ---
        # Hydration: loss rate during sleep is slower (0.05 per minute).
        hydration_loss_rate = 0.05
        self.hydrationLevel -= hydration_loss_rate * sleep_minutes
        if self.hydrationLevel <= 0:
            self.apply_dehydration_penalties()

        # Bladder Urgency: increases at 0.07 per minute during sleep.
        self.bladderUrgency += 0.07 * sleep_minutes
        if self.bladderUrgency > 50:
            self.wake_up_early()
        
        # Bowel Urgency: increases at 0.05 per minute during sleep.
        self.bowelUrgency += 0.05 * sleep_minutes
        if self.bowelUrgency > 50:
            self.trigger_forced_defecation()

        # Dirtiness (hygiene degradation): accumulates more slowly during sleep.
        self.dirtinessLevel += (0.1 / 60) * sleep_minutes

        # Hunger: builds at 0.08 per minute during sleep.
        self.hunger += 0.08 * sleep_minutes
        if self.hunger > 100:
            self.hunger = 100
            self.trigger_starvation()

        # Addiction Cravings: increased at reduced rates during sleep.
        self.nicotineCraving += 0.05 * sleep_minutes
        self.alcoholCraving += 0.03 * sleep_minutes
        self.drugCraving += 0.02 * sleep_minutes
        if self.heroinLevel > 9:
            self.trigger_overdose()

        # --- Cosmetic Effects During Sleep ---
        # Makeup: if applied, its quality degrades (smeared) by a fixed amount per sleep episode.
        if self.makeupOn:
            self.makeupQuality = max(0, self.makeupQuality - 0.5)
        # Hair: is no longer considered groomed after sleep.
        self.hairGroomed = False

    # ========================================================
    # Arousal & Sexual Mechanics
    # ========================================================
    def update_arousal(self):
        """
        Arousal increases with time. Lubrication is computed based on current arousal.
        """
        self.horny += random.randint(1, 5)
        self.lubrication = min(self.horny / 10, 14)
        if self.horny >= 30:
            print("Character feels minor excitement.")
        if self.horny >= 50:
            print("Character is visibly aroused.")
        if self.horny >= 65:
            print("Character is experiencing strong desire.")

    def achieve_orgasm(self):
        """
        If arousal is high enough, character experiences orgasm and satisfaction,
        and the arousal resets.
        """
        if self.horny >= 50:
            self.orgasmSatisfaction += random.randint(2, 4)
            self.horny = 0
            print("Character experiences orgasm and satisfaction.")

    # ========================================================
    # Aging & Body Changes
    # ========================================================
    def age_up(self):
        """
        Increase age by one year and apply aging penalties:
        reduced skin condition, baseBeauty, and increased wrinkles/fatigue.
        """
        self.age += 1
        self.skinCondition -= 1
        self.baseBeauty -= 0.5
        if self.age >= 40:
            self.wrinkles += 1
            self.fatigueRate += 0.5
            print("Aging effects intensify.")

    # ========================================================
    # Skin & Tanning System
    # ========================================================
    def update_tan(self, sun_exposure):
        """
        Increases tanLevel based on sun exposure.
        """
        self.tanLevel += sun_exposure * 0.1
        print(f"Character's tan level increased to {self.tanLevel}")

    def fade_tan(self):
        """
        Tan fades over time.
        """
        self.tanLevel = max(0, self.tanLevel - 0.5)
        print("Tan is fading over time.")

    def update_skin_health(self, skincare_routine):
        """
        Improves skin condition based on skincare routine.
        """
        self.skinCondition += skincare_routine * 0.5
        self.skinCondition = min(self.skinCondition, 100)
        print("Skin condition improves with care.")

    # ========================================================
    # Placeholder Methods for Triggered Events
    # ========================================================
    def force_sleep(self):
        print("Character is exhausted and falls asleep automatically.")

    def apply_depression_effects(self):
        print("Character is becoming depressed due to low mood.")

    def apply_dehydration_penalties(self):
        print("Character suffers dehydration penalties!")

    def trigger_forced_urination(self):
        print("Character can no longer hold it and must urinate!")

    def trigger_forced_defecation(self):
        print("Character loses control and defecates!")

    def trigger_overdose(self):
        print("Character overdoses on heroin!")

    def trigger_starvation(self):
        print("Character is starving due to extreme hunger!")

    def wake_up_early(self):
        print("Bladder urgency forces the character to wake up early!")