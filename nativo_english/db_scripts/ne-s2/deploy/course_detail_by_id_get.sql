/*****************************************************
Author: Hadiya Kashif
Ticket: https://app.clickup.com/t/868axzz4x
Description: This function will return course details by course ID

Params: course_id
*****************************************************/

-- Drop the function if it already exists
DROP FUNCTION IF EXISTS course_detail_by_id_get(INT);

-- Create or replace the function to return course details
CREATE OR REPLACE FUNCTION course_detail_by_id_get(p_course_id INT)
RETURNS TABLE(
    course_id BIGINT,
    title VARCHAR,
    description TEXT,
    is_paid BOOLEAN,
    price FLOAT,
    mode VARCHAR,
    avg_rating FLOAT,
    is_active BOOLEAN
) AS
$$
BEGIN
    RETURN QUERY
    SELECT 
        crs.id AS course_id,
        crs.title,
        crs.description,
        crs.is_paid,
        crs.price,
        crs.mode,
        crs.avg_rating,
        crs.is_active
    FROM "course_course" crs
    WHERE crs.id = p_course_id;
END;
$$ LANGUAGE plpgsql;
