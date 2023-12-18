import numpy as np
import string

class MarkovChain:
    def __init__(self):
        # Initialize the Markov Chain class
        self.stateNum = 0
        self.states = {}
        self.sequences = {}
        self.transitions = []
        self.Mat = []
        self.nextStates = []
        pass

    def new_state(self, new_state):
        if new_state not in self.states.keys():
            self.states[new_state] = self.stateNum
            self.sequences[self.stateNum] = new_state
            self.stateNum += 1
    
    def add_transition(self, current_state, next_state):
        # Add a transition from the current state to the next state
        self.new_state(current_state)
        self.new_state(next_state)
        trans = (self.states[current_state], self.states[next_state])
        self.transitions.append(trans)

    def compileMatrix(self):
        self.Mat = np.zeros((self.stateNum, self.stateNum))
        for trans in self.transitions:
            self.Mat[trans[0], trans[1]] += 1
        self.nextStates = np.argmax(self.Mat, axis = 1)

    def next_state_word(self, state):
        next_state = self.nextStates[state]
        return (next_state, self.sequences[next_state])
    
    def generate_states(self, initial_state, num_states):
        # Generate a sequence of states starting from the initial state
        state = self.states[initial_state]
        Word = initial_state
        Words = [Word]
        for i in range(num_states):
            state, Word = self.next_state_word(state)
            Words.append(Word)
        return Words
            
    def _get_next_state(self, current_state):
        # Get the next state based on the current state
        next_state = self.nextStates[state]
        return self.sequences[next_state]

# Example usage
translator = str.maketrans('', '', string.punctuation) 

if __name__ == "__main__":
    # Create a Markov Chain instance
    markov_chain = MarkovChain()

    # Add transitions based on the text
    text = "In a land far away, there lived a wise old owl. The owl loved to share stories. These stories were not just any tales; they were reflections of the wisdom the owl had gained over the years. Every evening, creatures from all around the land would gather to listen to the owl's tales. The tales spoke of adventures, lessons, and the mysteries of the land. Among the listeners were a curious rabbit, a brave fox, and a cautious deer. The rabbit, known for its endless curiosity, would always ask questions about the tales. The fox, brave and cunning, would ponder how to use the lessons in life. The deer, cautious and gentle, would reflect on the morals of the stories. Together, they learned much from the wise old owl and looked forward to each new tale with great anticipation."
        
    # Split the text into words and add each pair of consecutive words as a transition
    #I added another layer to this splitting. It will split all the senteces with a fullstop first. Then  apply transitions from those split sentences
    text_split_dot = text.lower().split(".")
    for texts in text_split_dot:
        text_split = texts.translate(translator).split(" ")
        while("" in text_split):
            text_split.remove("")
        #print(text_split)
        for i in range(len(text_split)-1):
            markov_chain.add_transition(text_split[i], text_split[i+1])
    markov_chain.compileMatrix()
    
    # Generate a sequence of states (words)
    initial_state = "adventures"
    num_states = 10  # length of the generated text
    generated_sequence = markov_chain.generate_states(initial_state, num_states)
    print("Generated Text:", " ".join(generated_sequence))
