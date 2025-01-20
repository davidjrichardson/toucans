from functools import reduce

from django import template


register = template.Library()


def rank_leg(scores):
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
    # results is the tuple list from a dict (.items())
    results_dict = dict(results)
    reordered = []

    # Reference is already sorted, so simply re-insert in order of the reference
    for team, _ in reference:
        reordered.append((team, results_dict[team]))

    return reordered


@register.filter()
def contract(name):
    return {"loughborough": "L'boro", "de montfort": "DMU"}.get(name.lower(), name)


@register.filter()
def dashify(val):
    if int(val) >= 0:
        return val
    else:
        return "‒"


def flatten(ll):
    return [item for sublist in ll for item in sublist]


def aggregate_team_scores(scores):
    return reduce(
        lambda z, y: (z[0] + y[0], z[1] + y[1], z[2] + y[2], z[3] + y[3]), scores
    )


def generate_table(standings):
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
    standings = results[0]

    standings_sorted, standings_aggregate, standings_has_results = generate_table(
        standings
    )

    return {
        "request": context["request"],
        "standings": standings_sorted,
        "standings_agg": standings_aggregate,
        # Results empty is simply if there are no results through the entire table
        "standings_have_results": any(standings_has_results),
    }
