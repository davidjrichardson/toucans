from functools import reduce

from django import template


register = template.Library()


def rank_leg(scores):
    """
    Ranks teams based on their scores.

    Args:
        scores (list of tuples): A list of tuples where each tuple contains a team identifier and a score tuple.
                                 The score tuple consists of three integers representing different score components.

    Returns:
        list of tuples: A list of tuples where each tuple contains a team identifier and a tuple with the following:
                        - Rank of the team (higher score gets a lower rank number, zero score gets rank 0)
                        - First component of the score
                        - Second component of the score
                        - Third component of the score
    """
    ranked = sorted(scores, key=lambda x: x[1], reverse=True)
    points = {
        team[0]: (
            len(ranked) - i if team[1] != (0, 0, 0) else 0,
            team[1][0],
            team[1][1],
            team[1][2],
        )
        for i, team in enumerate(ranked)
    }
    return list(points.items())


def align_results(reference, results):
    """
    Aligns the results based on the order of the reference.

    Args:
        reference (list of tuples): A list of tuples where each tuple contains a team and a value.
                                    The list is already sorted in the desired order.
        results (list of tuples): A list of tuples where each tuple contains a team and a value.
                                  This is typically obtained from a dictionary's items() method.

    Returns:
        list of tuples: A list of tuples where each tuple contains a team and a value,
                        reordered to match the order of the reference.
    """
    # results is the tuple list from a dict (.items())
    results_dict = dict(results)
    reordered = []

    # Reference is already sorted, so simply re-insert in order of the reference
    for team, _ in reference:
        reordered.append((team, results_dict[team]))

    return reordered


@register.filter()
def contract(name):
    """
    Shortens the given university name to its contracted form if available.

    Args:
        name (str): The full name of the university.

    Returns:
        str: The contracted form of the university name if it exists in the predefined dictionary,
             otherwise returns the original name.
    """
    return {"loughborough": "L'boro", "de montfort": "DMU"}.get(name.lower(), name)


@register.filter()
def dashify(val):
    """
    Converts a negative-or-zero number a dash symbol.

    Args:
        val (int or str): The value to be checked and possibly converted.
                          It should be convertible to an integer.

    Returns:
        str: The original value as a string if it is non-negative,
             otherwise a dash symbol ("‒").
    """
    if int(val) >= 0:
        return val
    else:
        return "‒"


def flatten(ll):
    """
    Flattens a list of lists into a single list.

    Args:
        ll (list of lists): A list where each element is a list.

    Returns:
        list: A single list containing all elements from the sublists.
    """
    return [item for sublist in ll for item in sublist]


def aggregate_team_scores(scores):
    """
    Aggregates a list of team scores by summing corresponding elements.

    Args:
        scores (list of tuple): A list of tuples where each tuple contains four numerical values representing team scores.

    Returns:
        tuple: A tuple containing the aggregated scores.
    """
    return reduce(
        lambda z, y: (z[0] + y[0], z[1] + y[1], z[2] + y[2], z[3] + y[3]), scores
    )


def generate_table(standings):
    """
    Generates a table of standings with aggregated results and ranking.

    Args:
        standings (list): A list of standings objects, where each object contains:
            - team_name (str): The name of the team.
            - results (list): A list of tuples representing the results for each leg.

    Returns:
        tuple: A tuple containing:
            - standings_sorted (list): A list of tuples representing the sorted standings,
              where each tuple contains the team name and their results.
            - standings_aggregate (list): A list of tuples representing the aggregated results
              for each team, where each tuple contains the total points, score, hits, and golds.
            - standings_has_results (list): A list of booleans indicating if there are results
              for each leg. True means 0-points will be displayed, otherwise a dash (-) will be shown.
    """
    if not standings:
        return [], [], []

    standings_have_results = any([not x.is_empty for x in standings])
    # Total number of results in the table (num_legs + champs)
    total_num_results = len(standings[0].results)
    empty_result = tuple(0 for _ in range(0, total_num_results))
    if standings_have_results:
        standings_matrix = [
            [
                (x.team_name, x.results[i]) for x in standings
            ]  # The team name and result for each team
            for i in range(0, total_num_results)
        ]

        # Rank each leg individually
        ranked_legs = flatten([rank_leg(leg) for leg in standings_matrix])
        results_per_team = {
            standings.team_name: [
                ranked_result[1]  # The points, score, hits, golds tuple
                for ranked_result in ranked_legs
                if ranked_result[0] == standings.team_name
            ]
            for standings in standings
        }

        # Collapse the list of results per-team into a 4-tuple: (points, agg. score, agg. hits, agg. golds)
        # And sort by that
        standings_sorted = sorted(
            results_per_team.items(),
            # The key is the aggregate points, score, hits and golds per-team
            key=lambda x: reduce(
                lambda z, y: (z[0] + y[0], z[1] + y[1], z[2] + y[2], z[3] + y[3]), x[1]
            ),
            reverse=True,
        )

        standings_aggregate = [
            reduce(
                lambda z, y: (z[0] + y[0], z[1] + y[1], z[2] + y[2], z[3] + y[3]), x[1]
            )
            for x in standings_sorted
        ]

        # The per-leg column of if there are results: True means 0-points will be displayed, otherwise a dash (-)
        # will be shown instead
        standings_has_results = [
            any(x[1] != (0, 0, 0) for x in leg) for leg in standings_matrix
        ]
    else:
        standings_sorted = sorted(map(lambda x: (x.team_name, x.results), standings))
        # The per-leg column of if there are results: True means 0-points will be displayed, otherwise a dash (-)
        # will be shown instead
        standings_has_results = [False for _ in range(0, total_num_results)]
        standings_aggregate = [empty_result for _ in range(0, total_num_results)]

    return standings_sorted, standings_aggregate, standings_has_results


@register.inclusion_tag("common/tags/results_table.html", takes_context=True)
def overall_standings(context, standings):
    """
    Generates the overall standings for a given context and standings data.

    This function sorts the standings, aggregates the standings data, and checks if there are any results.
    It returns a dictionary containing the request context, sorted standings, aggregated standings,
    a mask indicating the presence of results, and a boolean indicating if there are any non-zero results.

    Args:
        context (dict): The request context.
        standings (list): A list of standings data.

    Returns:
        dict: A dictionary containing the following keys:
            - "request": The request context.
            - "standings": The sorted standings.
            - "standings_agg": The aggregated standings.
            - "results_mask": A mask indicating the presence of results.
            - "standings_have_results": A boolean indicating if there are any non-zero results.
    """
    standings_sorted, standings_aggregate, standings_has_results = generate_table(
        standings
    )

    return {
        "request": context,
        "standings": standings_sorted,
        "standings_agg": standings_aggregate,
        "results_mask": standings_has_results,
        # If the table has any non-zero results
        "standings_have_results": any(standings_has_results),
    }


@register.inclusion_tag("home/tags/aggregate_results_table.html", takes_context=True)
def aggregated_standings(context, results):
    """
    Generate aggregated standings from the given results and context.

    Args:
        context (dict): The context dictionary containing request information.
        results (list): A list of results from which standings are generated.

    Returns:
        dict: A dictionary containing:
            - "request": The request information from the context.
            - "standings": The sorted standings.
            - "standings_agg": The aggregated standings.
            - "standings_have_results": A boolean indicating if there are any results in the standings.
    """
    # print(results)
    # if len(results) > 0:
    #     results = results[0]
    # else:
    #     results = []

    standings_sorted, standings_aggregate, standings_has_results = generate_table(
        results
    )

    return {
        "request": context["request"],
        "standings": standings_sorted,
        "standings_agg": standings_aggregate,
        # Results empty is simply if there are no results through the entire table
        "standings_have_results": any(standings_has_results),
    }
