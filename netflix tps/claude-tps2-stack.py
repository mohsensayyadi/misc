

# "Netflix's UI lets a user navigate through titles as they browse — clicking into a show's detail page, 
# then into a related title, then back, etc. Design a BrowsingHistory class that supports:

# visit(title_id) — user navigates to a new title (this clears any 'forward' history, like a real browser)
# back(steps) — go back up to steps pages, return the title landed on
# forward(steps) — go forward up to steps pages, return the title landed on

# Given a sequence of these calls in order, return the results of each back/forward call."

# A few things worth thinking about out loud before you code, the way you'd do in the actual interview:

# Clarify: What happens if back/forward steps overshoot the available history — clamp to the boundary, or error?
# Data structure choice: this is the classic two-stack pattern — one stack for "history" (pages you can go back to) and one for "forward" (pages you can redo into). visit pushes onto history and clears forward. back pops from history onto forward (or vice versa depending on how you define current position).
# Alternative: some people solve this with a single array + a pointer index instead of two stacks — both are valid, but the interviewer will likely want you to at least mention the array+pointer variant and discuss tradeoffs (stacks avoid needing to know the full array size upfront; array+pointer gives O(1) direct indexing).


class BrowsingHistory:
    def __init__(self, k=0, win=0):
        self.b_st = []
        self.f_st = []


    def visit(self, mov):
        self.b_st.append(mov)
    
    def back(self, step):
        if len(self.b_st) ==0 or len(self.b_st)  < step:
            return None
        i = 1
        while i <= step:
            old_mov = self.b_st.pop()
            self.f_st.append(old_mov)
            i +=1
        
        return old_mov

    
    def forward(self, step):
        if len(self.f_st) ==0 or len(self.f_st)  < step:
            return None
        i = 1
        while i <= step:
            old_mov = self.f_st.pop()
            self.b_st.append(old_mov)
            i +=1
        
        return old_mov




history = BrowsingHistory()

history.visit("A")
history.visit("B")
history.visit("C")
print("Backward history:", history.b_st)  

back1 = history.back(1)  # should return "B"
back2 = history.back(1)  # should return "A"
back3 = history.back(1)  # should return None, since we're at the beginning of history



print("back1:", back1)  # Output: B
print("back2:", back2)  # Output: A
print("back3:", back3)  # Output: None

print("Backward history:", history.b_st)  # Output: ['A']

print("Forward history:", history.f_st)  # Output: ['C', 'B']

print("Now forward:")

forward1 = history.forward(1)  # should return "B"
forward2 = history.forward(1)  # should return "C"

print("forward1:", forward1)  # Output: B
print("forward2:", forward2)  # Output: C


print("Backward history:", history.b_st)  

print("Forward history:", history.f_st)  