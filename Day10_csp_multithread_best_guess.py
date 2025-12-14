import re

from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod

import concurrent.futures

from concurrent.futures import ProcessPoolExecutor

V = TypeVar('V') # Variable
D = TypeVar('D') # Domain

class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: List[V]):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...

class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]):
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it")
            
    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True
    
    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        if len(assignment) == len(self.variables):
            return assignment
        
        unassigned: List[V] = [v for v in self.variables if v not in assignment]
        first: V = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None
    
class SumGroupsConstraint(Constraint[int, int]):
    def __init__(self, buttons_wiring, jolts):
        super().__init__([i for i in range(len(buttons_wiring))])
        self.buttons_wiring = buttons_wiring
        self.jolts = jolts

        self.jolts_groups = [list() for i in range(len(jolts))]

        self.min_presses = None

        for index, wiring in enumerate(buttons_wiring):
            for wi in wiring:
                self.jolts_groups[wi].append(index)


    def satisfied(self, assignment: Dict[int, int]) -> bool:

        total_presses = sum(assignment.values())
        if self.min_presses and self.min_presses <= total_presses:
            return False
        
        left_for_group = []

        for group, jg in enumerate(self.jolts_groups):
            jolts_needed = self.jolts[group]

            total_jolts = 0
            full_group = True
            for group_member in jg:
                if group_member in assignment:
                    total_jolts += assignment[group_member]
                else:
                    full_group = False
            if full_group and jolts_needed != total_jolts:
                return False
            elif total_jolts > jolts_needed:
                return False
            
            left_for_group.append(jolts_needed - total_jolts)
            
        # # check if possible with unassigned vars
        # for index, wiring in enumerate(self.buttons_wiring):
        #     if index not in assignment:
        #         for w in wiring:
        #             left_for_group[w] -= 1000
        # for left in left_for_group:
        #     if left > 0:
        #         return False
            
        # print("Checking", assignment, end="\r")

        if len(assignment) == len(self.buttons_wiring):
            if not self.min_presses or total_presses < self.min_presses:
                self.min_presses = total_presses

        return True


class JoltsConstraint(Constraint[int, int]):
    def __init__(self, buttons_wiring, jolts):
        super().__init__([i for i in range(len(buttons_wiring))])
        self.buttons_wiring = buttons_wiring
        self.jolts = jolts

    def satisfied(self, assignment: Dict[int, int]) -> bool:
        j = list(jolts)
        for button, presses in assignment.items():
            for wire in self.buttons_wiring[button]:
                j[wire] -= presses
        for ij in j:
            if ij < 0:
                return False
            
        if len(self.buttons_wiring) != len(assignment): return True
            
        for ij in j:
            if ij != 0:
                return False
            
        return True
    


def process_csp(buttons2, jolts, index):

    print("Starting", index)

    presses_indexes = [i for i in range(len(buttons2))]
    max_j = max(jolts)
    possible_presses: Dict[int, List[int]] = {}
    for pr in presses_indexes:
        max_for_wiring = 100000000
        for butt_wire in buttons2[pr]:
            if jolts[butt_wire] < max_for_wiring:
                max_for_wiring = jolts[butt_wire]
        possible_presses[pr] = [i for i in range(max_for_wiring, -1, -1)]
    
    presses_indexes.sort(key = lambda k : len(buttons2[k]), reverse=True)
    csp: CSP[str, int] = CSP(presses_indexes, possible_presses)
    # csp.add_constraint(JoltsConstraint(buttons2, jolts))
    csp.add_constraint(SumGroupsConstraint(buttons2, jolts))
    solution: Optional[Dict[str, int]] = csp.backtracking_search()

    s = sum(solution.values())
    print("Calculated", index, s)

    return s

    
if __name__ == "__main__":

    inputs = []

    with open('inputs/10-blocker.txt', 'r') as file:
        for y, line in enumerate(file):
            match = re.match(r'\[(.*)\] (\(.*\)) {(.*)}', line.rstrip())
            lights = match.groups()[0]
            buttons_str = match.groups()[1]
            jolts_str = match.groups()[2]

            machine_light = int(lights.replace('#', '1').replace('.', '0')[::-1], 2)

            def to_button(button_def):
                bits = button_def.split(',')
                button = 0
                for b in bits:
                    button = button ^ (1 << (int(b)))

                return button
            
            def to_button2(button_def):
                return [int(b) for b in button_def.split(',')]

            def to_jolts(j_str):
                return [int(j) for j in j_str.split(',')]

            buttons = [ to_button(str[1:-1]) for str in buttons_str.split()]
            buttons2 = [ to_button2(str[1:-1]) for str in buttons_str.split()]
            jolts = to_jolts(jolts_str)

            inputs.append((machine_light, buttons, buttons2, jolts))

    presses = 0
    for index, (machine_light, buttons, buttons2, jolts) in enumerate(inputs):
        
        outcomes = dict()
        outcomes[0] = 0
        to_check = [(0, 1, i) for i in range(len(buttons)) ] # from, presses, button index

        while len(to_check) > 0:
            initial_pos, press_count, button = to_check.pop(0)
            press = initial_pos ^ buttons[button]

            if press == machine_light:
                presses += press_count
                break

            if (press in outcomes and outcomes[press] > press_count) or press not in outcomes:
                outcomes[press] = press_count
                for b in range(len(buttons)):
                    to_check.append((press, press_count + 1, b))


    presses_j = 0


    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        for index, (machine_light, buttons, buttons2, jolts) in enumerate(inputs):
            futures.append(executor.submit(process_csp, buttons2, jolts, index))

        for future in concurrent.futures.as_completed(futures):
            presses_j += future.result()


    print(f"Part 1: {presses}")
    print(f"Part 1: {presses_j}")

