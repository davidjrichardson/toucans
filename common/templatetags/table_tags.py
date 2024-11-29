from functools import reduce

from django import template

from common.models import ThreeLegStanding

register = template.Library()


def rank_leg(scores):
    points = {}
    ranked = sorted(scores, key=lambda x: x[1], reverse=True)

    for i in range(0, len(ranked)):
        if ranked[i][1] != (0, 0, 0):
            points[ranked[i][0]] = (
                len(ranked) - i,
                ranked[i][1][0],
                ranked[i][1][1],
                ranked[i][1][2],
            )
        else:
            # If the team has no hits/points/golds, they get 0 points
            points[ranked[i][0]] = (
                0,
                ranked[i][1][0],
                ranked[i][1][1],
                ranked[i][1][2],
            )

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


def generate_3leg_table(standings: list[ThreeLegStanding]):
    # Check if all of the standings provided are empty
    standings_are_empty = reduce(
        lambda x, y: x and y, map(lambda x: x.is_empty, standings)
    )
    if standings_are_empty:
        standings_sorted = sorted(map(lambda x: (x.team_name, x.results), standings))
        # The per-leg column of if there are results: True means 0-points will be displayed, otherwise a dash (-)
        # will be shown instead
        standings_has_results = [False, False, False, False, False]
        standings_aggregate = [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)]
    else:
        # Rank each leg individually
        leg_1 = rank_leg(list(map(lambda x: (x.team_name, x.leg_1), standings)))
        leg_2 = rank_leg(list(map(lambda x: (x.team_name, x.leg_2), standings)))
        leg_3 = rank_leg(list(map(lambda x: (x.team_name, x.leg_3), standings)))
        champs = rank_leg(list(map(lambda x: (x.team_name, x.champs), standings)))
        pts_combined = leg_1 + leg_2 + leg_3 + champs
        pts_dict = {}

        for team, rank in pts_combined:
            if pts_dict.get(team):
                pts_dict.get(team).append(rank)
            else:
                pts_dict[team] = [rank]

        # Collapse the list of results per-team into a 4-tuple: (points, agg. score, agg. hits, agg. golds)
        # And sort by that
        standings_sorted = sorted(
            pts_dict.items(),
            key=lambda x: reduce(
                lambda z, y: (z[0] + y[0], z[1] + y[1], z[2] + y[2], z[3] + y[3]), x[1]
            ),
            reverse=True,
        )
        reduce(lambda x, y: x or y, list(map(lambda x: x[1] != (0, 0, 0, 0), leg_1)))
        # The per-leg column of if there are results: True means 0-points will be displayed, otherwise a dash (-)
        # will be shown instead
        standings_has_results = [
            reduce(
                lambda x, y: x or y, list(map(lambda x: x[1] != (0, 0, 0, 0), leg_1))
            ),
            reduce(
                lambda x, y: x or y, list(map(lambda x: x[1] != (0, 0, 0, 0), leg_2))
            ),
            reduce(
                lambda x, y: x or y, list(map(lambda x: x[1] != (0, 0, 0, 0), leg_3))
            ),
            reduce(
                lambda x, y: x or y, list(map(lambda x: x[1] != (0, 0, 0, 0), champs))
            ),
        ]
        standings_aggregate = list(
            map(
                lambda x: reduce(
                    lambda z, y: (z[0] + y[0], z[1] + y[1], z[2] + y[2], z[3] + y[3]),
                    x[1],
                ),
                standings_sorted,
            )
        )

    return standings_sorted, standings_aggregate, standings_has_results


@register.inclusion_tag("home/tags/3leg_results_table.html", takes_context=True)
def overall_3leg_standings(context, standings):
    standings_sorted, standings_aggregate, standings_has_results = generate_3leg_table(
        standings
    )

    return {
        "request": context,
        "standings": standings_sorted,
        "standings_agg": standings_aggregate,
        "results_mask": standings_has_results,
        # Results empty is simply if there are no results through the entire table
        "results_empty": reduce(lambda x, y: x or y, standings_has_results),
    }


def generate_4leg_table(standings):
    # Check if all of the standings provided are empty
    standings_are_empty = reduce(
        lambda x, y: x and y, map(lambda x: x.is_empty, standings)
    )
    if standings_are_empty:
        standings_sorted = sorted(map(lambda x: (x.team_name, x.results), standings))
        # The per-leg column of if there are results: True means 0-points will be displayed, otherwise a dash (-)
        # will be shown instead
        standings_has_results = [False, False, False, False, False]
        standings_aggregate = [
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
        ]
    else:
        # Rank each leg individually
        leg_1 = rank_leg(list(map(lambda x: (x.team_name, x.leg_1), standings)))
        leg_2 = rank_leg(list(map(lambda x: (x.team_name, x.leg_2), standings)))
        leg_3 = rank_leg(list(map(lambda x: (x.team_name, x.leg_3), standings)))
        leg_4 = rank_leg(list(map(lambda x: (x.team_name, x.leg_4), standings)))
        champs = rank_leg(list(map(lambda x: (x.team_name, x.champs), standings)))
        pts_combined = leg_1 + leg_2 + leg_3 + leg_4 + champs
        pts_dict = {}

        for team, rank in pts_combined:
            if pts_dict.get(team):
                pts_dict.get(team).append(rank)
            else:
                pts_dict[team] = [rank]

        # Collapse the list of results per-team into a 4-tuple: (points, agg. score, agg. hits, agg. golds)
        # And sort by that
        standings_sorted = sorted(
            pts_dict.items(),
            key=lambda x: reduce(
                lambda z, y: (z[0] + y[0], z[1] + y[1], z[2] + y[2], z[3] + y[3]), x[1]
            ),
            reverse=True,
        )
        reduce(lambda x, y: x or y, list(map(lambda x: x[1] != (0, 0, 0, 0), leg_1)))
        # The per-leg column of if there are results: True means 0-points will be displayed, otherwise a dash (-)
        # will be shown instead
        standings_has_results = [
            reduce(
                lambda x, y: x or y, list(map(lambda x: x[1] != (0, 0, 0, 0), leg_1))
            ),
            reduce(
                lambda x, y: x or y, list(map(lambda x: x[1] != (0, 0, 0, 0), leg_2))
            ),
            reduce(
                lambda x, y: x or y, list(map(lambda x: x[1] != (0, 0, 0, 0), leg_3))
            ),
            reduce(
                lambda x, y: x or y, list(map(lambda x: x[1] != (0, 0, 0, 0), leg_4))
            ),
            reduce(
                lambda x, y: x or y, list(map(lambda x: x[1] != (0, 0, 0, 0), champs))
            ),
        ]
        standings_aggregate = list(
            map(
                lambda x: reduce(
                    lambda z, y: (z[0] + y[0], z[1] + y[1], z[2] + y[2], z[3] + y[3]),
                    x[1],
                ),
                standings_sorted,
            )
        )

    return standings_sorted, standings_aggregate, standings_has_results


@register.inclusion_tag("home/tags/aggregate_results_table.html", takes_context=True)
def aggregated_standings(context, results):
    standings = results[0]
    num_legs = results[1]

    if num_legs == 3:
        standings_sorted, standings_aggregate, standings_has_results = (
            generate_3leg_table(standings)
        )
    else:
        standings_sorted, standings_aggregate, standings_has_results = (
            generate_4leg_table(standings)
        )

    return {
        "request": context["request"],
        "standings": standings_sorted,
        "standings_agg": standings_aggregate,
        # Results empty is simply if there are no results through the entire table
        "results_empty": not reduce(lambda x, y: x or y, standings_has_results),
    }


@register.inclusion_tag("home/tags/4leg_results_table.html", takes_context=True)
def overall_4leg_standings(context, standings):
    standings_sorted, standings_aggregate, standings_has_results = generate_4leg_table(
        standings
    )

    return {
        "request": context,
        "standings": standings_sorted,
        "standings_agg": standings_aggregate,
        "results_mask": standings_has_results,
        # Results empty is simply if there are no results through the entire table
        "results_empty": reduce(lambda x, y: x or y, standings_has_results),
    }
