"""
State Machine Module for Tibia Bot

This module provides state management capabilities for the bot,
allowing it to track current state and manage transitions between
different states like IDLE, COMBAT, HEALING, etc.
"""

import time
import threading
from typing import Optional, Dict, Any, Callable, List
from dataclasses import dataclass
from enum import Enum, auto
import json


class BotState(Enum):
    """Enumeration of possible bot states."""
    IDLE = auto()
    NAVIGATING = auto()
    COMBAT = auto()
    HEALING = auto()
    LOOTING = auto()
    DEPOSITING = auto()
    FISHING = auto()
    CRAFTING = auto()
    TRADING = auto()
    ERROR = auto()


@dataclass
class StateTransition:
    """Configuration for a state transition."""
    from_state: BotState
    to_state: BotState
    condition: Callable[[], bool]
    priority: int = 0
    description: str = ""


class StateMachine:
    """
    State machine for managing bot states and transitions.
    
    This class provides methods to manage the current state of the bot
    and handle transitions between different states based on conditions.
    """
    
    def __init__(self):
        """Initialize the StateMachine."""
        self.current_state = BotState.IDLE
        self.previous_state = BotState.IDLE
        self.state_start_time = time.time()
        self.state_data: Dict[str, Any] = {}
        self.transitions: List[StateTransition] = []
        self.state_handlers: Dict[BotState, Callable] = {}
        self.is_running = False
        self._state_lock = threading.Lock()
        self._transition_thread: Optional[threading.Thread] = None
        
        # Initialize default transitions
        self._init_default_transitions()
    
    def _init_default_transitions(self):
        """Initialize default state transitions."""
        # Combat transitions
        self.add_transition(
            BotState.IDLE, BotState.COMBAT,
            lambda: self.state_data.get('in_combat', False),
            priority=10,
            description="Enemy detected"
        )
        
        self.add_transition(
            BotState.NAVIGATING, BotState.COMBAT,
            lambda: self.state_data.get('in_combat', False),
            priority=10,
            description="Enemy detected while navigating"
        )
        
        # Healing transitions
        self.add_transition(
            BotState.IDLE, BotState.HEALING,
            lambda: self.state_data.get('health_low', False),
            priority=9,
            description="Health is low"
        )
        
        self.add_transition(
            BotState.COMBAT, BotState.HEALING,
            lambda: self.state_data.get('health_critical', False),
            priority=11,
            description="Health is critical during combat"
        )
        
        # Looting transitions
        self.add_transition(
            BotState.COMBAT, BotState.LOOTING,
            lambda: self.state_data.get('combat_finished', False),
            priority=8,
            description="Combat finished, time to loot"
        )
        
        # Navigation transitions
        self.add_transition(
            BotState.IDLE, BotState.NAVIGATING,
            lambda: self.state_data.get('waypoint_available', False),
            priority=5,
            description="Waypoint available for navigation"
        )
        
        self.add_transition(
            BotState.LOOTING, BotState.NAVIGATING,
            lambda: self.state_data.get('looting_finished', False),
            priority=7,
            description="Looting finished, continue navigation"
        )
        
        # Error transitions
        self.add_transition(
            BotState.IDLE, BotState.ERROR,
            lambda: self.state_data.get('error_occurred', False),
            priority=15,
            description="Error occurred"
        )
        
        self.add_transition(
            BotState.NAVIGATING, BotState.ERROR,
            lambda: self.state_data.get('error_occurred', False),
            priority=15,
            description="Error occurred while navigating"
        )
        
        self.add_transition(
            BotState.COMBAT, BotState.ERROR,
            lambda: self.state_data.get('error_occurred', False),
            priority=15,
            description="Error occurred during combat"
        )
        
        self.add_transition(
            BotState.HEALING, BotState.ERROR,
            lambda: self.state_data.get('error_occurred', False),
            priority=15,
            description="Error occurred while healing"
        )
        
        self.add_transition(
            BotState.LOOTING, BotState.ERROR,
            lambda: self.state_data.get('error_occurred', False),
            priority=15,
            description="Error occurred while looting"
        )
        
        # Return to idle
        self.add_transition(
            BotState.HEALING, BotState.IDLE,
            lambda: not self.state_data.get('health_low', False),
            priority=6,
            description="Health restored"
        )
        
        self.add_transition(
            BotState.ERROR, BotState.IDLE,
            lambda: not self.state_data.get('error_occurred', False),
            priority=5,
            description="Error resolved"
        )
    
    def add_transition(self, 
                      from_state: BotState, 
                      to_state: BotState, 
                      condition: Callable[[], bool],
                      priority: int = 0,
                      description: str = ""):
        """
        Add a state transition.
        
        Args:
            from_state: State to transition from
            to_state: State to transition to
            condition: Function that returns True when transition should occur
            priority: Priority of the transition (higher = more important)
            description: Description of the transition
        """
        transition = StateTransition(
            from_state=from_state,
            to_state=to_state,
            condition=condition,
            priority=priority,
            description=description
        )
        
        self.transitions.append(transition)
        # Sort by priority (highest first)
        self.transitions.sort(key=lambda t: t.priority, reverse=True)
    
    def set_state_handler(self, state: BotState, handler: Callable):
        """
        Set a handler function for a specific state.
        
        Args:
            state: The state to set handler for
            handler: Function to call when entering this state
        """
        self.state_handlers[state] = handler
    
    def set_state_data(self, key: str, value: Any):
        """
        Set data for the current state.
        
        Args:
            key: Data key
            value: Data value
        """
        with self._state_lock:
            self.state_data[key] = value
    
    def get_state_data(self, key: str, default: Any = None) -> Any:
        """
        Get data for the current state.
        
        Args:
            key: Data key
            default: Default value if key not found
            
        Returns:
            Data value or default
        """
        with self._state_lock:
            return self.state_data.get(key, default)
    
    def clear_state_data(self, key: str):
        """
        Clear specific state data.
        
        Args:
            key: Data key to clear
        """
        with self._state_lock:
            if key in self.state_data:
                del self.state_data[key]
    
    def clear_all_state_data(self):
        """Clear all state data."""
        with self._state_lock:
            self.state_data.clear()
    
    def get_current_state(self) -> BotState:
        """
        Get the current state.
        
        Returns:
            Current bot state
        """
        with self._state_lock:
            return self.current_state
    
    def get_previous_state(self) -> BotState:
        """
        Get the previous state.
        
        Returns:
            Previous bot state
        """
        with self._state_lock:
            return self.previous_state
    
    def get_state_duration(self) -> float:
        """
        Get how long the bot has been in the current state.
        
        Returns:
            Duration in seconds
        """
        return time.time() - self.state_start_time
    
    def force_state(self, new_state: BotState):
        """
        Force a state change without checking transitions.
        
        Args:
            new_state: New state to set
        """
        with self._state_lock:
            if new_state != self.current_state:
                self.previous_state = self.current_state
                self.current_state = new_state
                self.state_start_time = time.time()
                
                print(f"State changed: {self.previous_state.name} -> {self.current_state.name}")
                
                # Call state handler if exists
                if new_state in self.state_handlers:
                    try:
                        self.state_handlers[new_state]()
                    except Exception as e:
                        print(f"Error in state handler for {new_state.name}: {e}")
    
    def check_transitions(self) -> bool:
        """
        Check for valid state transitions and execute them.
        
        Returns:
            True if a transition occurred, False otherwise
        """
        current_state = self.get_current_state()
        
        for transition in self.transitions:
            # Check if transition is applicable
            if transition.from_state == current_state:
                
                try:
                    if transition.condition():
                        self.force_state(transition.to_state)
                        print(f"Transition: {transition.description}")
                        return True
                except Exception as e:
                    print(f"Error checking transition condition: {e}")
        
        return False
    
    def start(self):
        """Start the state machine."""
        if self.is_running:
            print("State machine already running")
            return
        
        self.is_running = True
        self._transition_thread = threading.Thread(target=self._transition_loop, daemon=True)
        self._transition_thread.start()
        print("State machine started")
    
    def stop(self):
        """Stop the state machine."""
        self.is_running = False
        if self._transition_thread:
            self._transition_thread.join(timeout=2.0)
        print("State machine stopped")
    
    def _transition_loop(self):
        """Internal method for checking transitions continuously."""
        while self.is_running:
            try:
                self.check_transitions()
                time.sleep(0.1)  # Check every 100ms
            except Exception as e:
                print(f"Error in transition loop: {e}")
                time.sleep(0.5)
    
    def is_in_state(self, state: BotState) -> bool:
        """
        Check if the bot is in a specific state.
        
        Args:
            state: State to check for
            
        Returns:
            True if bot is in the specified state, False otherwise
        """
        return self.get_current_state() == state
    
    def is_in_any_state(self, states: List[BotState]) -> bool:
        """
        Check if the bot is in any of the specified states.
        
        Args:
            states: List of states to check for
            
        Returns:
            True if bot is in any of the specified states, False otherwise
        """
        current_state = self.get_current_state()
        return current_state in states
    
    def get_state_info(self) -> Dict[str, Any]:
        """
        Get comprehensive information about the current state.
        
        Returns:
            Dictionary with state information
        """
        with self._state_lock:
            return {
                'current_state': self.current_state.name,
                'previous_state': self.previous_state.name,
                'state_duration': self.get_state_duration(),
                'state_data': self.state_data.copy(),
                'is_running': self.is_running
            }
    
    def save_state(self, filename: str):
        """
        Save current state to a JSON file.
        
        Args:
            filename: Path to save the state file
        """
        try:
            state_info = self.get_state_info()
            
            with open(filename, 'w') as f:
                json.dump(state_info, f, indent=2)
            
            print(f"State saved to {filename}")
            
        except Exception as e:
            print(f"Error saving state: {e}")
    
    def load_state(self, filename: str):
        """
        Load state from a JSON file.
        
        Args:
            filename: Path to load the state file from
        """
        try:
            with open(filename, 'r') as f:
                state_info = json.load(f)
            
            # Restore state data
            self.state_data = state_info.get('state_data', {})
            
            # Note: We don't restore current_state as it should be determined by conditions
            print(f"State data loaded from {filename}")
            
        except Exception as e:
            print(f"Error loading state: {e}")
    
    def print_status(self):
        """Print current state status."""
        info = self.get_state_info()
        print(f"Current State: {info['current_state']}")
        print(f"Previous State: {info['previous_state']}")
        print(f"Duration: {info['state_duration']:.2f} seconds")
        print(f"Running: {info['is_running']}")
        print(f"State Data: {info['state_data']}")
    
    def __del__(self):
        """Cleanup when the object is destroyed."""
        self.stop() 