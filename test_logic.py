"""
Test suite for the Logic Engine (Knowledge Base and Forward Chaining)

Run these tests to validate the inference engine before integration.
"""

from logic_engine import KnowledgeBase


def test_forward_chaining():
    """
    Test the forward chaining algorithm with safety rules for the grid game.
    """
    kb = KnowledgeBase()
    
    # Add Domain Rules
    kb.tell_rule(['TargetVisible', 'HasDust'], 'SafeToEngage')
    kb.tell_rule(['SafeToEngage', 'BloodseekerMissing'], 'Retreat')
    
    # Test Case 1: Safe Engagement
    print("Running Test Case 1: Safe Engagement...")
    kb.clear_facts()
    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')
    kb.forward_chain()
    assert 'SafeToEngage' in kb.facts, "Test 1 Failed: Should deduce SafeToEngage"
    assert 'Retreat' not in kb.facts, "Test 1 Failed: Should NOT deduce Retreat"
    print("✓ Test 1 Passed: SafeToEngage deduced, Retreat not deduced")
    
    # Test Case 2: Unsafe Engagement (Bloodseeker Missing)
    print("Running Test Case 2: Unsafe Engagement (Bloodseeker Missing)...")
    kb.clear_facts()
    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')
    kb.tell_fact('BloodseekerMissing')
    kb.forward_chain()
    assert 'SafeToEngage' in kb.facts, "Test 2 Failed: Should deduce SafeToEngage"
    assert 'Retreat' in kb.facts, "Test 2 Failed: Should deduce Retreat to override search"
    print("✓ Test 2 Passed: Both SafeToEngage and Retreat deduced")
    
    # Test Case 3: No rules triggered (missing premises)
    print("Running Test Case 3: No rules triggered...")
    kb.clear_facts()
    kb.tell_fact('TargetVisible')
    # HasDust is missing, so SafeToEngage should NOT be deduced
    kb.forward_chain()
    assert 'SafeToEngage' not in kb.facts, "Test 3 Failed: Should NOT deduce SafeToEngage"
    assert 'Retreat' not in kb.facts, "Test 3 Failed: Should NOT deduce Retreat"
    print("✓ Test 3 Passed: No conclusions deduced with incomplete premises")
    
    # Test Case 4: Multiple rule chaining
    print("Running Test Case 4: Multiple rule chaining...")
    kb2 = KnowledgeBase()
    kb2.tell_rule(['A'], 'B')
    kb2.tell_rule(['B'], 'C')
    kb2.tell_rule(['C'], 'D')
    kb2.tell_fact('A')
    kb2.forward_chain()
    assert 'B' in kb2.facts, "Test 4 Failed: B should be deduced"
    assert 'C' in kb2.facts, "Test 4 Failed: C should be deduced"
    assert 'D' in kb2.facts, "Test 4 Failed: D should be deduced through chaining"
    print("✓ Test 4 Passed: Chained deductions work correctly")
    
    print("\n✅ All Logic Engine Test Cases Passed!")


if __name__ == "__main__":
    test_forward_chaining()
