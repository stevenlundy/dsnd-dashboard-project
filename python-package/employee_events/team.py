from .query_base import QueryBase


class Team(QueryBase):
    """
    This class is a subclass of QueryBase
    It contains methods for querying the employee_events database
    for team data
    """

    name = "team"

    def names(self):
        """
        This method returns a list of tuples
        containing the team name and team_id
        for all teams in the database
        """

        sql = """
                SELECT team_name, team_id
                FROM team
              """

        return self.query(sql)

    def username(self, id: int):
        """
        This method returns a list of tuples
        containing the team name of the team
        with the given id
        """

        sql = f"""
                SELECT team_name
                FROM team
                WHERE team_id = {id}
                """

        return self.query(sql)

    def model_data(self, id):
        """
        This method returns a pandas dataframe
        with the number of positive and negative events
        for the team with the given id
        """

        sql = f"""
                SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
                """

        return self.pandas_query(sql)
