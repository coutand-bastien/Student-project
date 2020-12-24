/**
 * \file automaton.cpp
 * \brief Implementation file containing the code for the functions that could not be implemented in "automaton.hpp"
 * \author Matthieu Perrin 
 * \version 1
 * \date 11-16-2020
 */

#include "automaton.hpp"
#include "set.hpp"
#include <vector>
#include <iostream>

using namespace univ_nantes;

/**
 * fn automaton determine() const
 * brief Gets a new deterministic automaton that recognizes the same language
 * @return a deterministic automaton
 */
automaton automaton::determine() const {
    return (!this->is_deterministic()) ? determine2() : *this;
}

/**
 * fn automaton determine2() const
 * apply determinization
 * @return a deterministic automaton
 */
automaton automaton::determine2() const {
    int                   indexNewGroupEtat; // index or state number of the deterministic automaton
    bool                  f_find, f_exist;   // f_find: (flag) if a deterministic state group already exists in the vector; f_exist: (flag) if a transition exists for its symbol
    automaton             afd;               // automaton to return
    std::vector<set<int>> statesOfDeterAuto; // the new states of the deterministic automaton

    // the new states of the deterministic automaton, starts with ...
    // ... the group of initial states which forms 1 initial state, at index 0 ...
    statesOfDeterAuto.push_back(this->initials);
    afd.initials |= 0;

    // ... and if it's also an final state :
    for (int init : this->initials)
        if (this->finals.contains(init))
            afd.finals |= 0;


    // search for new states and transitions :
    for (int k = 0; k < (int)statesOfDeterAuto.size(); k++)
        for (char a : this->get_alphabet()) {
            set<int> newStates; // new states under construction
            f_exist = false;    // initialization to "zero"
            
            for (transition phi : this->transitions) {

                if (statesOfDeterAuto[k].contains(phi.start) && phi.is_epsilon()) 
                    statesOfDeterAuto[k] |= phi.end;

                if (statesOfDeterAuto[k].contains(phi.start) && phi.terminal == a) {
                    newStates |= epsilon_accessible({phi.end}); // take all states which are epsilon accessible
                    f_exist = true;
                }
            }

            if (newStates.size() != 0) {
                // determine the index of the next group of states in the state vector of the new automaton:
                f_find = false;                               // initialization to "zero"
                indexNewGroupEtat = statesOfDeterAuto.size(); // the next index is the size of the vector, if the state group is not found in this one

                for (int i = 0; i < (int)statesOfDeterAuto.size(); i++)
                    if (statesOfDeterAuto[i] == newStates) {
                        indexNewGroupEtat = i;
                        f_find = true;
                        break;
                    }


                // Final states:
                for (int t : newStates)
                    if (this->finals.contains(t))
                        afd.finals |= indexNewGroupEtat;

                // Transitions:
                if (f_exist)
                    afd.transitions |= transition(k, a, indexNewGroupEtat);

                // New states:
                if (!f_find)
                    statesOfDeterAuto.push_back(newStates);
            }
        }

    return afd;
}


/**
 * Gets whether the automaton is deterministic or not
 *
 * An automaton is considered to be deterministic if, and only if, it has exactly one initial state, no epsilon-transition, 
 * and no two transitions starting in the same state and ending in a different states, with a different label.
 */
bool automaton::is_deterministic() const {
  // Check that there is a unique initial state
  if(initials.size() != 1) return false;
  for(transition t1 : transitions) {
    // Check that there is no epsilon transition
    if(t1.is_epsilon()) return false;
    for(transition t2 : transitions) {
      // Check that there are no two transitions starting in the same state, with the same label
      if(t1.start == t2.start && t1.terminal == t2.terminal && t1.end != t2.end) return false;
    }
  }
  return true;
}

/**
 * Gets the set of states accessible from some state in from by following epsilon transitions
 *
 * A state y is included in the returned set if, and only if, there f_exists a state x in from
 * and a sequence of states x0=x, x1, ..., xn = y such that each epsilon-transition xi |--> x(i+1)
 * is contained in transitions.
 *
 * Example : a.epsilon_accessible(a.initials) returns all states accessible in a, through the empty word.
 */
set<int> automaton::epsilon_accessible(set<int> from) const {
  set<int> result = from;
  bool go_on = true;
  while (go_on) {
    go_on = false;
    for(transition t : transitions) {
      if(result.contains(t.start) && t.terminal == '\0' && !result.contains(t.end)) {
	result |= t.end;
	go_on = true;
      }
    }
  }
  return result;
}

/**
 * Gets the set of states accessible from some state in from by following one transition labeled by c 
 *
 * A state y is included in the returned set if, and only if, there f_exists a state x in from 
 * such that x |-c-> y is contained in transitions.
 *
 * Example : a.epsilon_accessible(a.accessible(a.epsilon_accessible({1,2}),'a')) returns all states accessible in a, from states 1 or 2, through the word "a". 
 */
set<int> automaton::accessible(set<int> from, char c) const {
  set<int> result;
  for(transition t : transitions) {
    if(from.contains(t.start) && t.terminal == c)
      result |= t.end;
  }
  return result;
}

/*
 * Returns the set of states of the automaton, including all states accessible from the initial states
 *
 * A state is contained in the set returned if it is contained in initials, finals, or at the start or and of any transition.
 */
set<int> automaton::get_states() const {
  set<int> states = initials | finals;
  for(transition t : transitions)
    states |= {t.start, t.end};
  return states;
}

/*
 * Returns the set of terminal symbols (lower-case letters) that label at least one transition of the automaton
 */
set<char> automaton::get_alphabet() const {
  set<char> alphabet;
  for(transition t : transitions)
    if(!t.is_epsilon())
      alphabet |= {t.terminal};
  return alphabet;
}