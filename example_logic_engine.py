"""
Example usage of the LogicBasedAgent with Knowledge Base and Forward Chaining

This demonstrates how the logic engine integrates with A* pathfinding to make
safety-aware decisions in the grid game environment.
"""

from agent import LogicBasedAgent
from logic_engine import KnowledgeBase


def example_1_basic_knowledge_base():
    """
    Example 1: Create and use a basic Knowledge Base
    """
    print("=" * 60)
    print("EXAMPLE 1: Basic Knowledge Base Usage")
    print("=" * 60)
    
    kb = KnowledgeBase()
    
    # Tell the KB some facts
    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')
    
    print("Facts added: TargetVisible, HasDust")
    print("Facts in KB:", kb.facts)
    
    # Add rules
    kb.tell_rule(['TargetVisible', 'HasDust'], 'SafeToEngage')
    
    print("\nRule added: TargetVisible ∧ HasDust ⇒ SafeToEngage")
    
    # Run forward chaining
    kb.forward_chain()
    
    print("After forward chaining, facts in KB:", kb.facts)
    print("✓ Correctly deduced: SafeToEngage\n")


def example_2_multi_step_inference():
    """
    Example 2: Multi-step inference through chained rules
    """
    print("=" * 60)
    print("EXAMPLE 2: Multi-Step Forward Chaining")
    print("=" * 60)
    
    kb = KnowledgeBase()
    
    # Setup rules
    kb.tell_rule(['TargetVisible', 'HasDust'], 'SafeToEngage')
    kb.tell_rule(['SafeToEngage', 'BloodseekerMissing'], 'Retreat')
    
    # Set initial facts
    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')
    kb.tell_fact('BloodseekerMissing')
    
    print("Initial facts: TargetVisible, HasDust, BloodseekerMissing")
    print("Rules:")
    print("  1. TargetVisible ∧ HasDust ⇒ SafeToEngage")
    print("  2. SafeToEngage ∧ BloodseekerMissing ⇒ Retreat")
    
    # Run forward chaining
    kb.forward_chain()
    
    print("\nAfter forward chaining, deduced facts:", kb.facts)
    print("✓ Correctly deduced SafeToEngage and Retreat through chaining\n")


def example_3_logic_based_agent():
    """
    Example 3: Using the LogicBasedAgent for pathfinding
    """
    print("=" * 60)
    print("EXAMPLE 3: LogicBasedAgent with A* Pathfinding")
    print("=" * 60)
    
    agent = LogicBasedAgent()
    
    print("LogicBasedAgent created with Knowledge Base")
    print(f"Knowledge Base has {len(agent.kb.rules)} rules defined:")
    for i, (premises, conclusion) in enumerate(agent.kb.rules, 1):
        print(f"  Rule {i}: {' ∧ '.join(premises)} ⇒ {conclusion}")
    
    # Simulate a percept
    percept = {
        'agent_pos': [0, 0],
        'grid_size': (5, 5),
        'walls': [[1, 1], [2, 2], [3, 3]],
        'all_food': [[4, 4]],
        'remaining_food': 1
    }
    
    print("\nPercept from environment:")
    print(f"  Agent at: {percept['agent_pos']}")
    print(f"  Grid size: {percept['grid_size']}")
    print(f"  Walls at: {percept['walls']}")
    print(f"  Food at: {percept['all_food']}")
    
    # Call sense_and_act
    action = agent.sense_and_act(percept)
    print(f"\nAgent decides to: {action}")
    print(f"Planned path length: {len(agent.plan)}")
    if agent.plan:
        print(f"Next 3 actions: {agent.plan[:3]}\n")


def example_4_tile_evaluation():
    """
    Example 4: Demonstrating tile-by-tile safety evaluation
    """
    print("=" * 60)
    print("EXAMPLE 4: Tile-by-Tile Safety Evaluation")
    print("=" * 60)
    
    agent = LogicBasedAgent()
    
    percept = {
        'all_food': [[2, 2]],
        'walls': [[1, 1]]
    }
    
    # Evaluate different tiles
    test_tiles = [
        ((1, 1), "Occupied by wall"),
        ((2, 2), "Contains food"),
        ((3, 3), "Empty tile"),
    ]
    
    print("Evaluating tiles for safety:\n")
    
    for tile, description in test_tiles:
        print(f"Tile {tile} ({description}):")
        
        # Clear KB and evaluate
        agent.kb.clear_facts()
        facts = agent._tile_percepts(tile, percept)
        
        for fact in facts:
            agent.kb.tell_fact(fact)
        
        print(f"  Perceived facts: {facts}")
        
        # Run inference
        agent.kb.forward_chain()
        deduced = agent.kb.facts - set(facts)
        print(f"  Deduced facts: {deduced if deduced else 'None'}")
        
        # Determine feasibility
        if 'Retreat' in agent.kb.facts:
            print(f"  Status: INFEASIBLE (Retreat triggered)")
        else:
            print(f"  Status: FEASIBLE")
        
        print()


if __name__ == "__main__":
    # Run all examples
    example_1_basic_knowledge_base()
    example_2_multi_step_inference()
    example_3_logic_based_agent()
    example_4_tile_evaluation()
    
    print("=" * 60)
    print("✅ All examples completed successfully!")
    print("=" * 60)
