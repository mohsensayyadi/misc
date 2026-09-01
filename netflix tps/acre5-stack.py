# Problem: Implement a Command Executor with execute and undo
# Implement a CommandExecutor that can execute commands in order and undo the most recently executed command.

# Each Command must support:

# apply(): performs the command and mutates the system state
# revert(): undoes the command and restores the state to what it was before apply()
# You must implement:

# execute(command): execute a command and record it in undo history
# undo(): undo the most recent successfully executed and not-yet-undone command
# Requirements
# Define behavior when undo() is called with no history (return False / raise / no-op).
# If execute() fails (e.g., apply() raises), the command must NOT be recorded.
# Provide a small demo: e.g., an integer state with Add(x) commands.
# Constraints
# Over N operations, total overhead should be O(N). Each execute/undo should be amortized O(1) excluding the command logic.
# Example Tests
# input:

# # initial state = 0
# execute Add(5)
# execute Add(3)
# undo
# undo
# undo
# output:

# state=5
# state=8
# state=5
# state=0
# False
# input:

# # initial state = 10
# execute Add(-2)
# undo
# output:

# state=8
# state=10

class CommandExecutor:
    def __init__(self, state):
        self.state = state
        self.history = []

    def execute_add(self, amount):
        # Apply the command
        self.state[0] += amount

        # Store only what is needed to undo it
        self.history.append(-amount)

        return True

    def undo(self):
        if not self.history:
            return False

        # Pop the inverse operation
        inverse = self.history.pop()

        self.state[0] += inverse

        return True