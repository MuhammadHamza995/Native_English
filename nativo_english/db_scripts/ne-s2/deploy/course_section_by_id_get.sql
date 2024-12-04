/*****************************************************
Author: Hadiya Kashif
Ticket: https://app.clickup.com/t/868axzz4x
Description: This function will return course section details by section ID

Params: section_id
*****************************************************/

-- Drop the function if it already exists
DROP FUNCTION IF EXISTS course_section_detail_by_id_get(INT);

-- Create or replace the function to return course section details
CREATE OR REPLACE FUNCTION course_section_detail_by_id_get(p_section_id INT)
RETURNS TABLE(
    section_id BIGINT,
    section_title VARCHAR,
    section_description TEXT,
    fk_course_id BIGINT
) AS
$$
BEGIN
    RETURN QUERY
    SELECT 
        sec.id AS section_id,
        sec.section_title,
        sec.section_description,
        sec.fk_course_id
    FROM "course_coursesection" sec
    WHERE sec.id = p_section_id;
END;
$$ LANGUAGE plpgsql;
