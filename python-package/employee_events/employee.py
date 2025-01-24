from .query_base import QueryBase


class Employee(QueryBase):
    """
    This class is a subclass of QueryBase
    It contains methods for querying the employee_events database
    for employee data
    """

    name = "employee"

    def names(self):
        """
        This method returns a list of tuples
        containing the full name and employee_id
        for all employees in the database
        """

        sql = f"""
                SELECT first_name || ' ' || last_name full_name,
                     employee_id
                FROM employee
                """

        return self.query(sql)

    def username(self, id: int):
        """
        This method returns a list of tuples
        containing the full name of the employee
        with the given id
        """

        sql = f"""
                SELECT first_name || ' ' || last_name full_name
                FROM employee
                WHERE employee_id = {id}
                """

        return self.query(sql)

    def model_data(self, id: int):
        """
        This method returns a pandas dataframe
        with the number of positive and negative events
        for the employee with the given id
        """

        sql = f"""
                SELECT SUM(positive_events) positive_events
                        , SUM(negative_events) negative_events
                FROM {self.name}
                JOIN employee_events
                    USING({self.name}_id)
                WHERE {self.name}.{self.name}_id = {id}
                """

        return self.pandas_query(sql)
