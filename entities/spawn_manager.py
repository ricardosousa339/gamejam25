"""
Spawn Manager - Controls the spawning of trash objects over time
"""
import random
import pygame
from config import *


class SpawnManager:
    """
    Manages the spawning of trash objects with progressive difficulty:
    - Warm-up period before spawning starts
    - Gradual acceleration of spawn rate over time
    - Random waves/bursts of increased spawn rate
    """

    def __init__(self):
        """
        Initialize the spawn manager
        """
        # Timing
        self.game_start_time = pygame.time.get_ticks()
        self.last_spawn_time = self.game_start_time
        self.last_acceleration_time = self.game_start_time

        # Spawn rate control
        self.current_spawn_rate = SPAWN_INITIAL_RATE
        self.warmup_complete = False

        # Wave/burst system
        self.in_wave = False
        self.wave_start_time = 0
        self.next_wave_time = self.game_start_time + random.randint(WAVE_INTERVAL_MIN, WAVE_INTERVAL_MAX)

        print(f"[SPAWN MANAGER] Initialized - Warmup: {SPAWN_WARMUP_TIME}ms, Initial rate: {SPAWN_INITIAL_RATE}ms")
        print(f"[SPAWN MANAGER] First wave scheduled at: {self.next_wave_time - self.game_start_time}ms")

    def update(self, current_time):
        """
        Update spawn manager state

        Args:
            current_time (int): Current game time in milliseconds

        Returns:
            bool: True if should spawn a new object, False otherwise
        """
        # Check if warmup period is complete
        if not self.warmup_complete:
            if current_time - self.game_start_time >= SPAWN_WARMUP_TIME:
                self.warmup_complete = True
                print("[SPAWN MANAGER] Warmup complete - spawning enabled")
            else:
                return False  # Don't spawn during warmup

        # Update spawn rate acceleration (gradually speed up over time)
        if current_time - self.last_acceleration_time >= SPAWN_ACCELERATION_INTERVAL:
            self.last_acceleration_time = current_time
            old_rate = self.current_spawn_rate
            self.current_spawn_rate = max(SPAWN_MIN_RATE, self.current_spawn_rate - SPAWN_ACCELERATION_AMOUNT)

            if old_rate != self.current_spawn_rate:
                print(f"[SPAWN MANAGER] Spawn rate accelerated: {old_rate}ms -> {self.current_spawn_rate}ms")

        # Check for wave/burst activation
        if not self.in_wave and current_time >= self.next_wave_time:
            self._start_wave(current_time)

        # Check if current wave should end
        if self.in_wave and current_time - self.wave_start_time >= WAVE_DURATION:
            self._end_wave(current_time)

        # Determine if we should spawn based on current rate
        effective_spawn_rate = WAVE_SPAWN_RATE if self.in_wave else self.current_spawn_rate

        if current_time - self.last_spawn_time >= effective_spawn_rate:
            self.last_spawn_time = current_time
            return True

        return False

    def _start_wave(self, current_time):
        """
        Start a trash wave (increased spawn rate)

        Args:
            current_time (int): Current game time in milliseconds
        """
        self.in_wave = True
        self.wave_start_time = current_time
        print(f"[SPAWN MANAGER] WAVE STARTED! Duration: {WAVE_DURATION}ms, Rate: {WAVE_SPAWN_RATE}ms")

    def _end_wave(self, current_time):
        """
        End the current trash wave and schedule next one

        Args:
            current_time (int): Current game time in milliseconds
        """
        self.in_wave = False

        # Schedule next wave
        next_wave_delay = random.randint(WAVE_INTERVAL_MIN, WAVE_INTERVAL_MAX)
        self.next_wave_time = current_time + next_wave_delay

        print(f"[SPAWN MANAGER] Wave ended. Next wave in: {next_wave_delay}ms")

    def is_in_wave(self):
        """
        Check if currently in a wave period

        Returns:
            bool: True if in wave, False otherwise
        """
        return self.in_wave

    def get_current_spawn_rate(self):
        """
        Get the current effective spawn rate

        Returns:
            int: Current spawn rate in milliseconds
        """
        return WAVE_SPAWN_RATE if self.in_wave else self.current_spawn_rate

    def reset(self):
        """
        Reset the spawn manager to initial state
        """
        current_time = pygame.time.get_ticks()
        self.game_start_time = current_time
        self.last_spawn_time = current_time
        self.last_acceleration_time = current_time
        self.current_spawn_rate = SPAWN_INITIAL_RATE
        self.warmup_complete = False
        self.in_wave = False
        self.wave_start_time = 0
        self.next_wave_time = current_time + random.randint(WAVE_INTERVAL_MIN, WAVE_INTERVAL_MAX)

        print("[SPAWN MANAGER] Reset to initial state")
