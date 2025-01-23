def add_strategy_conditional_edges(workflow, from_node, approve_node, refine_node):
    """
    Adds conditional edges to the workflow based on user review instructions.
    
    Parameters:
    - workflow: The workflow object to which the edges will be added.
    - from_node: The node where the condition is evaluated (e.g., "human_editing").
    - approve_node: The node to proceed to if the user approves the strategy.
    - refine_node: The node to proceed to if the user requests refinement.
    """
    def routing_condition(state):
        review_instructions = state.get("review_instructions", "").lower()
        if "approve" in review_instructions:
            return approve_node
        return refine_node
    
    workflow.add_conditional_edges(from_node, routing_condition)
