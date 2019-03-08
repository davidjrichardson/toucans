from functools import reduce

from django import template

register = template.Library()


def rank_leg(scores):
    points = {}
    ranked = sorted(scores, key=lambda x: x[1], reverse=True)

    for i in range(0, len(ranked)):
        if ranked[i][1] != (0, 0, 0):
            points[ranked[i][0]] = (len(ranked) - i, ranked[i][1][0], ranked[i][1][1], ranked[i][1][2])
        else:
            # If the team has no hits/points/golds, they get 0 points
            points[ranked[i][0]] = (0, ranked[i][1][0], ranked[i][1][1], ranked[i][1][2])

    return list(points.items())


@register.inclusion_tag('home/tags/league_results_table.html', takes_context=True)
def overall_standings(context, standings):
    # Check if all of the standings provided are empty
    standings_are_empty = reduce(lambda x, y: x and y, map(lambda x: x.is_empty, standings))
    if standings_are_empty:
        standings_sorted = sorted(map(lambda x: (x.team_name, x.results), standings), key=lambda x: x.team_name)
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
        standings_sorted = sorted(pts_dict.items(),
                                  key=lambda x: reduce(
                                      lambda z, y: (z[0] + y[0], z[1] + y[1], z[2] + y[2], z[3] + y[3]),
                                      x[1]), reverse=True)

        # TODO: Sort the per-leg results into the order of the overall standings

    print(standings_sorted)

    return {
        'request': context
    }