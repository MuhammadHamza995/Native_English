from django.db import connection

def call_plpgsql_function(function_name, *params):
    """
    Helper function to call a PL/pgSQL function and fetch its results.

    Args:
        function_name (str): Name of the PL/pgSQL function to call.
        *params: Parameters to pass to the function.

    Returns:
        list[dict]: List of dictionaries representing the rows returned by the function.
    """
    with connection.cursor() as cursor:
        # Prepare the parameter placeholders
        param_placeholders = ', '.join(['%s'] * len(params))

        # Construct the SQL query
        query = f"SELECT * FROM {function_name}({param_placeholders})"
        
        # Execute the query
        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Fetch column names
        column_names = [desc[0] for desc in cursor.description]

    # Map rows to dictionaries
    return [dict(zip(column_names, row)) for row in rows]
