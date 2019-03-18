"""
Module that formats charts to being accepted by server.
Some charts returned from agent may contain not proper information:
1. len(series[i].data) != len(indicator.data) i.e. x axis is not comparable with all series
2. For Line and Bar charts if new series are added to chart we have to send them in separate request
Check:
Element files, thumbnails and previews section in docs/APIDescription.md
"""

import copy
from typing import Dict, Tuple, List
from collections import deque

from agents_platform.own_adapter.constants import BAR_CHART_TYPE, LINE_CHART_TYPE, VALUE_KEY, TOOLTIP_KEY, \
    RADAR_CHART_TYPE, X_AXIS_KEY, DATA_KEY, SERIES_KEY, NAME_KEY, OWN_ADAPTER_NAME, INDICATOR_KEY

default_point_values = {LINE_CHART_TYPE: {VALUE_KEY: 0, TOOLTIP_KEY: {}},
                        BAR_CHART_TYPE: 0,
                        RADAR_CHART_TYPE: 0}


def format_chart_data(chart_type: str = '', data: Dict = None, old_chart_data: Dict = None) -> Tuple:
    """
    Formats chart data to make it valid for sending to server
    :param chart_type: LINE, BAR, PIE, SCATTER, RADAR
    :param data: dictionary with chart data to add to chart
    :param old_chart_data: dictionary with data that was in chart before
    :return: separated dicts for new series and existed series
    """
    if old_chart_data is None:
        old_chart_data = {}
    if data is None:
        data = {}
    if chart_type in [LINE_CHART_TYPE, BAR_CHART_TYPE]:
        new_series_data, existing_series_data = format_line_and_bar_charts(chart_type, data, old_chart_data)
        return new_series_data, existing_series_data
    elif chart_type == RADAR_CHART_TYPE:
        chart_data = format_radar_chart(data)
        return [], chart_data


def format_line_and_bar_charts(chart_type: str = '', data: Dict = None, old_chart_data: Dict = None) -> Tuple[Dict, Dict]:
    """
    Formats chart data so that size(series[i].data)==size(indicator.data)
     and separates existed series (aka lines or bars) from newly added series(not presented in chart)
    :param chart_type: LINE or BAR
    :param data: chart data
    :param old_chart_data: data that was in chart before
    :return: dictionary with new series and dictionary with previously existing series
    """
    if old_chart_data is None:
        old_chart_data = {}
    if data is None:
        data = {}

    x_axis_values = data.get(X_AXIS_KEY, {}).get(DATA_KEY, [])
    x_axis_size = len(x_axis_values)
    series = data.get(SERIES_KEY, [])
    old_data = old_chart_data.get(DATA_KEY, {})
    old_series = old_data.get(SERIES_KEY, [])
    series_status = {existing.get(NAME_KEY): False for existing in old_series}  # set of existing series names
    new_series_names = []

    # all existing series should be mentioned in data and track if new are added
    for item in series:
        name = item.get(NAME_KEY, '')
        if name in series_status:
            series_status[name] = True  # mark if present
        else:
            new_series_names.append(name)  # track new series that were added

    # get names of series that were not mentioned (series_status[series_name] = False)
    unmentioned_series = list(filter(lambda x: not series_status[x], series_status))
    # fill unmentioned series with empty data
    series.extend([{NAME_KEY: name, DATA_KEY: []} for name in unmentioned_series])

    # update series info
    for item in series:
        _data = item.get(DATA_KEY, [])  # internal data for single line or bar

        if len(_data) < x_axis_size:  # then we extend data to size of indicator (axis data)
            append_default_points_to_data(x_axis_size - len(_data), _data, chart_type=chart_type)
            item[DATA_KEY] = _data  # set updated value of data in series

    data[SERIES_KEY] = series  # update data info

    new_series_data = {}
    if new_series_names:
        # some series were added, we have to divide data on two requests
        new_series_data = copy.deepcopy(data)
        # new series will contain zero data for previous axis points
        old_x_axis_data = old_data.get(X_AXIS_KEY, {}).get(DATA_KEY, [])
        new_series_data[X_AXIS_KEY][DATA_KEY] = old_x_axis_data + x_axis_values
        old_series = []
        new_series = []
        for item in series:
            if item.get(NAME_KEY, '') in new_series_names:
                # fill with points for previous axis values
                item[DATA_KEY] = prepend_default_points_to_data(len(old_x_axis_data), item.get(DATA_KEY, []),
                                                                chart_type=chart_type)
                new_series.append(item)
            else:
                old_series.append(item)

        new_series_data[SERIES_KEY] = new_series
        data[SERIES_KEY] = old_series
    return new_series_data, data


def format_radar_chart(data: Dict = {}) -> Dict:
    """
    Formats chart data so that size(data.indicator)==size(series[i].data.value)
    :param data: unformatted data
    :return: formatted data
    """
    x_axis_data = data.get(INDICATOR_KEY, [])
    x_axis_size = len(x_axis_data)
    chart_data = data.get(DATA_KEY, {})
    series = data.get(SERIES_KEY, [])
    for item in series:
        series_data = item.get(DATA_KEY, [])
        for data_item in series_data:
            if len(data_item) < x_axis_size:
                radar_values = data_item.get(VALUE_KEY, [])
                updated_values = append_default_points_to_data(x_axis_size - len(data_item),
                                                               radar_values, chart_type=RADAR_CHART_TYPE)
                data_item[VALUE_KEY] = updated_values
    chart_data[SERIES_KEY] = series
    data[DATA_KEY] = chart_data
    return data

def append_default_points_to_data(number_of_points: int, existing_points: List,
                                  chart_type: str = BAR_CHART_TYPE) -> List:
    """
    Appends extra points to list of ponits for specific chart types: LINE, BAR and RADAR
    Check https://github.com/own-dev/own-agent-open/blob/master/docs/APIDescription.md#patch-boardsboardidelementselementidfilesfileid
    :param number_of_points: how many points to add
    :param existing_points: existing points in line/bar or other possible chart items
    :param append: True to append, False to prepend to existing points
    :param chart_type: type of a chart to extend
    :return: new points list
    """
    default_point_value = default_point_values.get(chart_type, -1)
    if default_point_value == -1:
        return existing_points

    points_to_add = [default_point_value for i in range(number_of_points)]
    new_points = deque(existing_points)
    new_points.extend(points_to_add)
    return list(new_points)

def prepend_default_points_to_data(number_of_points: int, existing_points: List,
                                  chart_type: str = BAR_CHART_TYPE) -> List:
    """
    Prepends extra points to list of ponits for specific chart types: LINE, BAR and RADAR
    Check https://github.com/own-dev/own-agent-open/blob/master/docs/APIDescription.md#patch-boardsboardidelementselementidfilesfileid
    :param number_of_points: how many points to add
    :param existing_points: existing points in line/bar or other possible chart items
    :param chart_type: type of a chart to extend
    :return: new points list
    """
    default_point_value = default_point_values.get(chart_type, -1)
    if default_point_value == -1:
        return existing_points

    points_to_add = [default_point_value for i in range(number_of_points)]
    new_points = deque(existing_points)
    new_points.extendleft(reversed(points_to_add))
    return list(new_points)


