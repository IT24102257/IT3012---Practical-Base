"""
Logic Engine for the Grid Game Agent

This module implements a Knowledge Base with Forward Chaining inference
to enable declarative rule-based decision making.
"""


class KnowledgeBase:
    """
    A Knowledge Base that stores facts and rules, with forward chaining inference.
    
    Facts: Simple string propositions (e.g., "TargetVisible")
    Rules: Horn clauses represented as tuples ([premises], conclusion)
    """
    
    def __init__(self):
        """Initialize an empty knowledge base."""
        self.facts = set()  # Store unique string facts
        self.rules = []     # Store rules as tuples: ([premises], conclusion)
    
    def tell_fact(self, fact_string):
        """
        Add a fact to the knowledge base.
        
        Args:
            fact_string (str): The fact to add (e.g., "TargetVisible")
        """
        self.facts.add(fact_string)
    
    def tell_rule(self, premise_list, conclusion_string):
        """
        Add a rule to the knowledge base.
        
        Args:
            premise_list (list): List of premise strings that must all be true
            conclusion_string (str): The conclusion string if all premises are true
        """
        self.rules.append((premise_list, conclusion_string))
    
    def clear_facts(self):
        """Clear all facts from the knowledge base (rules remain)."""
        self.facts.clear()
    
    def forward_chain(self):
        """
        Execute forward chaining inference algorithm.
        
        Iterates through rules repeatedly, applying Modus Ponens until
        no new facts can be deduced (fixed point reached).
        """
        new_facts_added = True
        
        while new_facts_added:
            new_facts_added = False
            
            for premises, conclusion in self.rules:
                # Only process if conclusion is not already known
                if conclusion not in self.facts:
                    # Check if ALL premises are in facts (Modus Ponens)
                    if all(premise in self.facts for premise in premises):
                        # Add the new conclusion
                        self.facts.add(conclusion)
                        new_facts_added = True
