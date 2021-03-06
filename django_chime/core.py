# -*- coding: utf-8 -*-

'''
django_chime/core
-----------------

core functions for the django-chime app
'''

import altair as alt
import streamlit as st

from penn_chime.charts import (
    build_admits_chart,
    build_census_chart,
    build_sim_sir_w_date_chart,
    build_table,
)
from penn_chime.parameters import Parameters
from penn_chime.models import SimSirModel


class ShortID(object):
    '''
    short id property
    '''

    @property
    def short_id(self):
        return str(self.id)[-8:]


def is_number(s):
    '''
    returns True if s is a number, False otherwise
    '''

    if s is None:
        return False

    try:
        float(s)
        return True

    except ValueError:
        return False


def get_chime_model(parameters):
    '''
    instantiates and returns CHIME model using parameters
    '''

    if not isinstance(parameters, Parameters):
        t = type(parameters)
        raise TypeError(f'parameters must be a Parameters object not {t}')

    return SimSirModel(parameters)


def build_charts(model, width='container', padding={'right': 50}):
    '''
    builds CHIME charts
    '''

    charts = list()

    for fcn, attr in (
            (build_admits_chart, 'admits_floor_df'),
            (build_census_chart, 'census_floor_df'),
            (build_sim_sir_w_date_chart, 'sim_sir_w_date_floor_df'),
    ):
        charts.append({
            'chart': fcn(
                **{
                    'alt': alt,
                    attr: getattr(model, attr),
                },
            ).properties(
                width=width,
                padding=padding,
            ).to_json(),
        })

    return charts


def build_tables(model, labels):
    '''
    builds CHIME tables
    '''

    tables = list()

    for title, attr in (
            ('New Admissions', 'admits_floor_df'),
            ('Admitted Patients (Census)', 'census_floor_df'),
            ('Susceptible, Infected, and Recovered', 'sim_sir_w_date_floor_df'),
    ):

        df = getattr(model, attr)

        columns = [{'field': c, 'title': c} for c in df.columns]
        data = build_table(df=df, labels=labels)

        tables.append({
            'title': title,
            'id': attr,
            'columns': columns,
            'data': data.to_json(orient='records'),
        })

    return tables
