from collections import namedtuple
import pandas


def tidy_responses(wide_responses):
    """Tranform Google Survey responses from wide to long format.
    
    Args:
        wide_responses: pandas.DataFrame of survey responses in wide format,
            with one survey-taker per row, and different questions in different
            columns.
    Returns:
        A pandas.DataFrame of survey responses in long format, with all responses
        in a single column, one response per row, so that a single survey-taker's
        responses are spread over multiple rows.
    """
    wide_responses = wide_responses.copy()

    # Assign a unique identifier to each survey taker
    person_ids = ['p{}'.format(i) for i in list(wide_responses.index)]
    wide_responses.insert(0, 'person', person_ids)

    # Melt the data from wide to long
    response_strs = pandas.melt(wide_responses, 'person', var_name='question',
                                value_name='response_str')

    # Split response strings into one response per row
    long_responses = melt_responses(response_strs)

    return long_responses


def melt_response_strs(response_strs):
    """Melt response strings containing multiple responses.

    An example response str is 'Libraries, Offices'. The resulting DataFrame
    will have two rows, one for each response item, e.g, ['Libraries', 'Offices'].
    """
    Response = namedtuple('Response', 'person question response_n response')

    new_rows = []
    for old_row in response_strs.itertuples():
        response_str = old_row.response_str  # Grab response string
        try:
            # Try split the response string into multiple responses
            responses = [response.strip() for response in response_str.split(',')]
        except AttributeError:
            # If the response can't be split, they probably didn't answer
            # this question, so just put the empty value in a list
            responses = [response_str]

        # Create rows for each response
        rows = [Response(old_row.person, old_row.question, response_n, response)
                for response_n, response in enumerate(responses)]
        new_rows.extend(rows)

    return pandas.DataFrame(new_rows)
