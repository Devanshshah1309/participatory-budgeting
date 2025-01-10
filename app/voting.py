def approval_voting_method_of_equal_shares(projects, voters, k, budget):
    """
    Selects k projects using approval voting with the method of equal shares.

    Parameters:
    - projects: A list of tuples where each tuple contains (project_id, cost).
    - voters: A list of sets where each set contains the project_ids approved by a voter.
    - k: The number of projects to select.
    - budget: The total budget available.

    Returns:
    - A list of selected project_ids.
    """
    selected_projects = []
    remaining_budget = budget
    voter_shares = {voter_id: budget / len(voters) for voter_id in range(len(voters))}

    while len(selected_projects) < k and remaining_budget > 0:
        best_project = None
        best_value = 0
        best_contributions = {}

        for project_id, cost in projects:
            if project_id in selected_projects or cost > remaining_budget:
                continue

            total_approval = sum(1 for voter in voters if project_id in voter)
            if total_approval == 0:
                continue

            contributions = {}
            total_contribution = 0

            for voter_id, voter in enumerate(voters):
                if project_id in voter:
                    # TODO: fix logic, i think if someone else has more budget left
                    # then he can compensate for your lack of shares and still meet
                    # the approval criteria
                    contribution = min(voter_shares[voter_id], cost / total_approval)
                    contributions[voter_id] = contribution
                    total_contribution += contribution

            if total_contribution >= cost and total_contribution > best_value:
                best_project = project_id
                best_value = total_contribution
                best_contributions = contributions

        if best_project is None:
            break

        selected_projects.append(best_project)
        remaining_budget -= best_value

        for voter_id, contribution in best_contributions.items():
            voter_shares[voter_id] -= contribution

    return selected_projects