"""
Control classes for crocodile behavior
Separates movement and state transition logic from the crocodile sprite
"""
import pygame
import random
from config import RIVER_FLOW_SPEED


class CrocodileControl:
    """
    Base class for crocodile control behavior.
    Controls movement and state transitions.
    """

    # State transition timing (milliseconds)
    STATE_CHANGE_MIN_TIME = 2000  # minimum time before changing state
    STATE_CHANGE_MAX_TIME = 5000  # maximum time before changing state

    # Submersion states (0 = most visible, 4 = fully submerged/invisible)
    FULLY_SURFACED = 0
    MOSTLY_SURFACED = 1
    MOSTLY_SUBMERGED = 2
    HEAD_ONLY = 3
    FULLY_SUBMERGED = 4  # Invisible - not drawn or updated

    def __init__(self):
        """Initialize the control"""
        self.current_state = random.randint(0, 4)  # Start at random state (0-4)
        self.target_state = self.current_state

        # State transition timing
        self.state_timer = pygame.time.get_ticks()
        self.next_state_change = random.randint(
            self.STATE_CHANGE_MIN_TIME,
            self.STATE_CHANGE_MAX_TIME
        )

    def update_movement(self, crocodile, min_y, max_y):
        """
        Update crocodile position based on control logic

        Args:
            crocodile: The Crocodile sprite to control
            min_y: Minimum y boundary
            max_y: Maximum y boundary
        """
        # Default behavior: move with river flow and slight vertical wobble
        crocodile.rect.x += RIVER_FLOW_SPEED
        crocodile.rect.y += crocodile.vel_y

        # Keep within vertical bounds with bounce
        if crocodile.rect.top < min_y:
            crocodile.rect.top = min_y
            crocodile.vel_y *= -1
        elif crocodile.rect.bottom > max_y:
            crocodile.rect.bottom = max_y
            crocodile.vel_y *= -1

    def update_state(self):
        """
        Update the state transitions

        Returns:
            int: The new current state
        """
        current_time = pygame.time.get_ticks()

        # Check if it's time to pick a new target state
        if current_time - self.state_timer > self.next_state_change:
            old_target = self.target_state
            # Pick a random target state (0-4, including FULLY_SUBMERGED)
            self.target_state = random.randint(0, 4)

            print(f"[CROC] New target state: {old_target} -> {self.target_state} (current: {self.current_state})")

            # Reset timer for next change
            self.state_timer = current_time
            self.next_state_change = random.randint(
                self.STATE_CHANGE_MIN_TIME,
                self.STATE_CHANGE_MAX_TIME
            )

        # Gradually transition towards target state (one level at a time)
        if self.current_state < self.target_state:
            # Need to submerge more (increase state number)
            old_state = self.current_state
            self.current_state += 1
            print(f"[CROC] Submerging: {old_state} -> {self.current_state} (target: {self.target_state})")
        elif self.current_state > self.target_state:
            # Need to surface more (decrease state number)
            old_state = self.current_state
            self.current_state -= 1
            print(f"[CROC] Surfacing: {old_state} -> {self.current_state} (target: {self.target_state})")

        return self.current_state


class DebugControl(CrocodileControl):
    """
    Debug control that keeps crocodile fixed at one position
    Cycles through states in order for testing animations
    """

    def __init__(self, fixed_x, fixed_y):
        """
        Initialize debug control with fixed position

        Args:
            fixed_x (int): Fixed x position
            fixed_y (int): Fixed y position
        """
        super().__init__()
        self.fixed_x = fixed_x
        self.fixed_y = fixed_y
        # Start at state 0 and cycle through in order
        self.current_state = 0
        self.target_state = 1
        self.transitioning_up = True
        print(f"[DEBUG CONTROL] Created with fixed position ({fixed_x}, {fixed_y})")

    def update_movement(self, crocodile, min_y, max_y):
        """
        Keep crocodile at fixed position

        Args:
            crocodile: The Crocodile sprite to control
            min_y: Minimum y boundary (ignored)
            max_y: Maximum y boundary (ignored)
        """
        # Keep position fixed
        crocodile.rect.x = self.fixed_x
        crocodile.rect.y = self.fixed_y
        # Set velocity to zero
        crocodile.vel_y = 0

    def update_state(self):
        """
        Cycle through states in order (0 -> 1 -> 2 -> 3 -> 4 -> 3 -> 2 -> 1)
        """
        current_time = pygame.time.get_ticks()

        # Check if it's time to transition to next state
        if current_time - self.state_timer > self.next_state_change:
            # Move to target state
            if self.current_state != self.target_state:
                old_state = self.current_state
                self.current_state = self.target_state
                state_names = ["FULLY_SURFACED", "MOSTLY_SURFACED", "MOSTLY_SUBMERGED", "HEAD_ONLY", "FULLY_SUBMERGED"]
                print(f"[DEBUG CROC] State: {old_state} -> {self.current_state} ({state_names[self.current_state]})")

            # Set next target state (cycle through 0, 1, 2, 3, 4)
            if(self.transitioning_up):
                self.target_state = self.current_state + 1
                if(self.target_state > 4):
                    self.target_state = 3
                    self.transitioning_up = False
            else:
                self.target_state = self.current_state - 1
                if(self.target_state < 0):
                    self.target_state = 1
                    self.transitioning_up = True

            # Reset timer for next change
            self.state_timer = current_time
            self.next_state_change = random.randint(
                self.STATE_CHANGE_MIN_TIME,
                self.STATE_CHANGE_MAX_TIME
            )

        return self.current_state
