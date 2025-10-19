"""
Control classes for crocodile behavior
Separates movement and state transition logic from the crocodile sprite
"""
import pygame
import random
import config
from entities.pegador import PegadorState


class CrocodileControl:
    """
    Base class for crocodile control behavior.
    Controls movement and state transitions.
    """

    # State transition timing (milliseconds)
    STATE_CHANGE_MIN_TIME = 2000  # minimum time before changing state
    STATE_CHANGE_MAX_TIME = 5000  # maximum time before changing state

    # Vertical movement timing (milliseconds)
    VERTICAL_MOVE_MIN_TIME = 1500  # minimum time before changing vertical direction
    VERTICAL_MOVE_MAX_TIME = 3000  # maximum time before changing vertical direction (3 seconds)

    # Swim direction states
    TO_RIGH = 1
    TO_LEFT = 0

    # Submersion states (0 = most visible, 4 = fully submerged/invisible)
    FULLY_SURFACED = 0
    MOSTLY_SURFACED = 1
    MOSTLY_SUBMERGED = 2
    HEAD_ONLY = 3
    FULLY_SUBMERGED = 4  # Invisible - not drawn or updated

    states_array = [FULLY_SURFACED, MOSTLY_SURFACED, MOSTLY_SUBMERGED, HEAD_ONLY, FULLY_SUBMERGED]

    def __init__(self, crocodile):
        """Initialize the control"""
        self.current_state = random.randint(1, 4)  # Start at random state (0-4)
        self.target_state = self.current_state

        # State transition timing
        self.state_timer = pygame.time.get_ticks()
        self.swim_vert_timer = self.state_timer
        self.next_state_change = random.randint(
            self.STATE_CHANGE_MIN_TIME,
            self.STATE_CHANGE_MAX_TIME
        )

        self.next_swim_vert_change = random.randint(
            self.VERTICAL_MOVE_MIN_TIME,
            self.VERTICAL_MOVE_MAX_TIME
        )

        # Vertical movement velocity
        self.vel_y = random.uniform(-1.5, 1.5)

        # Carrying pegador state
        self.is_carrying = False
        self.carrying_start_time = 0
        self.waiting_at_edge = False
        self.wait_start_time = 0
        self.wait_duration = 1000  # 1 second wait

    def start_carrying(self):
        """Start carrying a pegador"""
        self.is_carrying = True
        self.carrying_start_time = pygame.time.get_ticks()
        self.waiting_at_edge = False
        print("[CONTROL] Started carrying mode")

    def stop_carrying(self):
        """Stop carrying and return to normal behavior"""
        self.is_carrying = False
        self.waiting_at_edge = False
        print("[CONTROL] Stopped carrying mode")

    def update_movement(self, crocodile, min_y, max_y):
        current_time = pygame.time.get_ticks()
        # print('pos: ', crocodile.rect.x, crocodile.rect.y)
        """
        Update crocodile position based on control logic

        Args:
            crocodile: The Crocodile sprite to control
            min_y: Minimum y boundary
            max_y: Maximum y boundary
        """
        # Special behavior when carrying pegador
        if self.is_carrying:
            if self.waiting_at_edge:
                # Waiting at edge for 1 second before returning
                if current_time - self.wait_start_time > self.wait_duration:
                    # Return pegador and crocodile to normal
                    pegador = crocodile.release_pegador()
                    if pegador:
                        pegador.state = PegadorState.IDLE
                        pegador.catching_crocodile = None
                        pegador.image = pegador.image_front
                        pegador.mask = pygame.mask.from_surface(pegador.image)
                        # Reset pegador to margin at horizontal center
                        pegador.rect.centerx = config.SCREEN_WIDTH // 2
                        pegador.rect.top = pegador.margin_y
                        pegador.collision_rect.centerx = pegador.rect.centerx
                        pegador.collision_rect.top = pegador.rect.top
                    self.stop_carrying()
                return  # Don't move while waiting

            # Continue swimming in current direction until off screen
            if crocodile.swim_direction == 1:  # Swimming right
                crocodile.rect.x += 2
                # Check if completely off screen (right edge)
                if crocodile.rect.left > config.SCREEN_WIDTH:
                    self.waiting_at_edge = True
                    self.wait_start_time = current_time
                    print("[CONTROL] Reached right edge, waiting...")
            else:  # Swimming left
                crocodile.rect.x -= 2
                # Check if completely off screen (left edge)
                if crocodile.rect.right < 0:
                    self.waiting_at_edge = True
                    self.wait_start_time = current_time
                    print("[CONTROL] Reached left edge, waiting...")
            return  # Skip normal movement behavior

        # Normal random swim behavior
        if(crocodile.swim_direction):
            crocodile.rect.x += 2
            if(crocodile.rect.x > config.SCREEN_WIDTH + 20):
                crocodile.swim_direction = 0
        else:
            crocodile.rect.x -= 2
            if(crocodile.rect.x < -100):
                crocodile.swim_direction = 1

        # Check if it's time to change vertical direction
        if current_time - self.swim_vert_timer > self.next_swim_vert_change:
            old_vel_y = self.vel_y

            # Pick a new random vertical velocity
            self.vel_y = random.uniform(-1.5, 1.5)

            print(f"[CROC] New vertical velocity: {old_vel_y:.2f} -> {self.vel_y:.2f}")

            # Reset timer for next change
            self.swim_vert_timer = current_time
            self.next_swim_vert_change = random.randint(
                self.VERTICAL_MOVE_MIN_TIME,
                self.VERTICAL_MOVE_MAX_TIME
            )

        # Apply vertical movement with small wobble
        wobble = random.uniform(-0.2, 0.2)
        crocodile.rect.y += self.vel_y + wobble

        # Keep within vertical bounds with bounce
        if crocodile.rect.top < min_y:
            crocodile.rect.top = min_y
            self.vel_y = abs(self.vel_y)  # Force downward movement
        elif crocodile.rect.bottom > max_y:
            crocodile.rect.bottom = max_y
            self.vel_y = -abs(self.vel_y)  # Force upward movement

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
            self.target_state = self._rand_next_state(old_target)

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
    
    def _rand_next_state(self, curr_state):
        if(curr_state == 1):
            return random.randint(1, 2)
        
        if(curr_state == 4):
            return random.randint(3, 4)

        return random.randint(curr_state - 1, curr_state + 1)


class DebugControl(CrocodileControl):
    """
    Debug control that keeps crocodile fixed at one position
    Cycles through states in order for testing animations
    """

    def __init__(self, crocodile):
        """
        Initialize debug control with fixed position

        Args:
            fixed_x (int): Fixed x position
            fixed_y (int): Fixed y position
        """
        super().__init__(crocodile)
        self.fixed_x = 150
        self.fixed_y = crocodile.rect.y
        # Start at state 0 and cycle through in order
        self.current_state = 0
        self.target_state = 1
        self.transitioning_up = True
        print(f"[DEBUG CONTROL] Created with fixed position ({self.fixed_x}, {self.fixed_y})")

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
