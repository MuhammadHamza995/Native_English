/*****************************************************
Author: Muhammad Hassaan Bashir
Ticket: https://app.clickup.com/t/868axzz4x
Description: This function will return user detail by Id

Params: user_id
*****************************************************/

-- Drop the function if it already exists
DROP FUNCTION IF EXISTS user_detail_by_id_get(INT);

-- Create or replace the function to return user details
CREATE OR REPLACE FUNCTION user_detail_by_id_get(user_id INT)
RETURNS TABLE(
    usr_id BIGINT, 
    username VARCHAR, 
    email VARCHAR,
    first_name VARCHAR,
    last_name VARCHAR,
    is_active BOOLEAN,
    user_role VARCHAR
    ) AS
$$
BEGIN
    RETURN QUERY
    SELECT 
        usr.id, 
        usr.username, 
        usr.email,
        usr.first_name,
        usr.last_name,
        usr.is_active,
        usr.role
    FROM "User_user" usr
    WHERE usr.id = user_id;
END;
$$ LANGUAGE plpgsql;