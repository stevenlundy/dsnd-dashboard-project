from .sql_execution import QueryMixin


class QueryBase(QueryMixin):
    """
    This class is a base class for the Employee and Team classes.
    It contains methods for querying the employee_events database.
    """

    name = ""  # 'team' or 'employee'

    def names(self):
        return []

    def event_counts(self, id: int):
        """
        This method returns a pandas dataframe
        with the number of positive and negative events
        for each day for a given employee or team.
        """

        sql = f"""
                SELECT event_date,
                       SUM(positive_events) positive_events,
                       SUM(negative_events) negative_events
                FROM employee_events
                WHERE {self.name}_id = {id}
                GROUP BY event_date
                ORDER BY event_date
                """

        return self.pandas_query(sql)

    def notes(self, id: int):
        """
        This method returns a pandas dataframe
        with the notes for a given employee or team.
        """

        sql = f"""
                SELECT note_date, note
                FROM notes
                WHERE {self.name}_id = {id}
                """

        return self.pandas_query(sql)
