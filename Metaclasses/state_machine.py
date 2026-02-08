"""
CONCEPT: Declarative state machine using metaclass
LEARN: Finite state machine with automatic transition validation
"""

import functools
from enum import Enum

class Transition:
    """Represents a state transition"""
    def __init__(self, from_state, to_state, action=None):
        self.from_state = from_state
        self.to_state = to_state
        self.action = action

def transition(from_state, to_state):
    """Decorator to mark methods as state transitions"""
    def decorator(func):
        func._transition = Transition(from_state, to_state, func)
        return func
    return decorator

def on_enter(state):
    """Decorator to mark methods to run on entering a state"""
    def decorator(func):
        func._on_enter_state = state
        return func
    return decorator

def on_exit(state):
    """Decorator to mark methods to run on exiting a state"""
    def decorator(func):
        func._on_exit_state = state
        return func
    return decorator

class StateMachineMeta(type):
    """Metaclass for creating state machines"""
    
    def __new__(cls, name, bases, attrs):
        # Find all transitions
        transitions = {}
        on_enter_handlers = {}
        on_exit_handlers = {}
        
        for attr_name, attr_value in attrs.items():
            # Find transition methods
            if hasattr(attr_value, '_transition'):
                trans = attr_value._transition
                key = (trans.from_state, trans.to_state)
                transitions[key] = attr_name
            
            # Find on_enter handlers
            if hasattr(attr_value, '_on_enter_state'):
                state = attr_value._on_enter_state
                if state not in on_enter_handlers:
                    on_enter_handlers[state] = []
                on_enter_handlers[state].append(attr_name)
            
            # Find on_exit handlers
            if hasattr(attr_value, '_on_exit_state'):
                state = attr_value._on_exit_state
                if state not in on_exit_handlers:
                    on_exit_handlers[state] = []
                on_exit_handlers[state].append(attr_name)
        
        attrs['_transitions'] = transitions
        attrs['_on_enter_handlers'] = on_enter_handlers
        attrs['_on_exit_handlers'] = on_exit_handlers
        
        # Override __init__ to set initial state
        original_init = attrs.get('__init__')
        
        def new_init(self, *args, **kwargs):
            if original_init:
                original_init(self, *args, **kwargs)
            
            if not hasattr(self, '_current_state'):
                # Set initial state
                initial_state = getattr(self.__class__, 'initial_state', None)
                if initial_state is None:
                    raise ValueError(f"Class {name} must define 'initial_state'")
                self._current_state = initial_state
                self._state_history = [initial_state]
                
                # Call on_enter handlers for initial state
                self._call_handlers(self._on_enter_handlers, initial_state)
        
        attrs['__init__'] = new_init
        
        # Add state management methods
        def get_current_state(self):
            return self._current_state
        
        def can_transition(self, to_state):
            return (self._current_state, to_state) in self._transitions
        
        def get_available_transitions(self):
            available = []
            for (from_state, to_state), method_name in self._transitions.items():
                if from_state == self._current_state:
                    available.append(to_state)
            return available
        
        def _call_handlers(self, handlers_dict, state):
            if state in handlers_dict:
                for handler_name in handlers_dict[state]:
                    handler = getattr(self, handler_name)
                    handler()
        
        def _perform_transition(self, to_state, method_name):
            # Call on_exit handlers for current state
            self._call_handlers(self._on_exit_handlers, self._current_state)
            
            # Update state
            old_state = self._current_state
            self._current_state = to_state
            self._state_history.append(to_state)
            
            # Call on_enter handlers for new state
            self._call_handlers(self._on_enter_handlers, to_state)
            
            print(f"State transition: {old_state} -> {to_state}")
        
        def get_state_history(self):
            return self._state_history.copy()
        
        attrs['get_current_state'] = get_current_state
        attrs['can_transition'] = can_transition
        attrs['get_available_transitions'] = get_available_transitions
        attrs['_call_handlers'] = _call_handlers
        attrs['_perform_transition'] = _perform_transition
        attrs['get_state_history'] = get_state_history
        
        # Wrap transition methods
        for (from_state, to_state), method_name in transitions.items():
            original_method = attrs[method_name]
            
            def make_wrapper(orig_method, f_state, t_state, m_name):
                @functools.wraps(orig_method)
                def wrapper(self, *args, **kwargs):
                    if self._current_state != f_state:
                        raise ValueError(
                            f"Cannot call {m_name} in state {self._current_state}. "
                            f"Expected state: {f_state}"
                        )
                    
                    # Execute the transition method
                    result = orig_method(self, *args, **kwargs)
                    
                    # Perform state transition
                    self._perform_transition(t_state, m_name)
                    
                    return result
                
                return wrapper
            
            attrs[method_name] = make_wrapper(original_method, from_state, to_state, method_name)
        
        return super().__new__(cls, name, bases, attrs)

# Example: Order State Machine
class OrderState(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(metaclass=StateMachineMeta):
    initial_state = OrderState.PENDING
    
    def __init__(self, order_id, items):
        self.order_id = order_id
        self.items = items
        self.tracking_number = None
    
    @transition(OrderState.PENDING, OrderState.CONFIRMED)
    def confirm(self):
        print(f"  Confirming order {self.order_id}")
        return "Order confirmed"
    
    @transition(OrderState.CONFIRMED, OrderState.PROCESSING)
    def start_processing(self):
        print(f"  Starting to process order {self.order_id}")
        return "Processing started"
    
    @transition(OrderState.PROCESSING, OrderState.SHIPPED)
    def ship(self, tracking_number):
        print(f"  Shipping order {self.order_id}")
        self.tracking_number = tracking_number
        return f"Shipped with tracking: {tracking_number}"
    
    @transition(OrderState.SHIPPED, OrderState.DELIVERED)
    def deliver(self):
        print(f"  Delivering order {self.order_id}")
        return "Order delivered"
    
    @transition(OrderState.PENDING, OrderState.CANCELLED)
    @transition(OrderState.CONFIRMED, OrderState.CANCELLED)
    def cancel(self):
        print(f"  Cancelling order {self.order_id}")
        return "Order cancelled"
    
    @on_enter(OrderState.CONFIRMED)
    def on_enter_confirmed(self):
        print(f"  -> Order {self.order_id} is now confirmed")
    
    @on_enter(OrderState.SHIPPED)
    def on_enter_shipped(self):
        print(f"  -> Order {self.order_id} is now shipped")
    
    @on_exit(OrderState.PROCESSING)
    def on_exit_processing(self):
        print(f"  <- Leaving processing state")

# Example: Traffic Light State Machine
class TrafficLightState(Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"

class TrafficLight(metaclass=StateMachineMeta):
    initial_state = TrafficLightState.RED
    
    @transition(TrafficLightState.RED, TrafficLightState.GREEN)
    def go(self):
        print("  Light: RED -> GREEN")
        return "GO"
    
    @transition(TrafficLightState.GREEN, TrafficLightState.YELLOW)
    def slow_down(self):
        print("  Light: GREEN -> YELLOW")
        return "SLOW DOWN"
    
    @transition(TrafficLightState.YELLOW, TrafficLightState.RED)
    def stop(self):
        print("  Light: YELLOW -> RED")
        return "STOP"

if __name__ == "__main__":
    print("=== Order State Machine ===")
    order = Order("ORD-123", ["Item1", "Item2"])
    
    print(f"\nInitial state: {order.get_current_state()}")
    print(f"Available transitions: {order.get_available_transitions()}")
    
    print("\n1. Confirming order:")
    order.confirm()
    
    print(f"\nCurrent state: {order.get_current_state()}")
    print(f"Available transitions: {order.get_available_transitions()}")
    
    print("\n2. Start processing:")
    order.start_processing()
    
    print("\n3. Ship order:")
    order.ship("TRACK-12345")
    
    print("\n4. Deliver order:")
    order.deliver()
    
    print(f"\nFinal state: {order.get_current_state()}")
    print(f"State history: {[s.value for s in order.get_state_history()]}")
    
    # Try invalid transition
    print("\n5. Try to ship delivered order (should fail):")
    try:
        order.ship("TRACK-99999")
    except ValueError as e:
        print(f"  Error: {e}")
    
    print("\n\n=== Traffic Light State Machine ===")
    light = TrafficLight()
    
    print(f"Initial state: {light.get_current_state()}")
    
    for cycle in range(2):
        print(f"\n--- Cycle {cycle + 1} ---")
        light.go()
        light.slow_down()
        light.stop()
    
    print(f"\nState history: {[s.value for s in light.get_state_history()]}")