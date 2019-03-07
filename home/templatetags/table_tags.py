from django import template

from home.models import StandingsPage, StandingsEntry

register = template.Library()


@register.inclusion_tag('home/tags/league_results_table.html', takes_context=True)
def overall_standings(context, standings):
    return {
        'request': context
    }
